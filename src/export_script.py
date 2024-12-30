import csv
import os
from src.database_script import ContactDatabase
from datetime import datetime


class SalesforceExporter:
    def __init__(self, db_path='data/contacts.db'):
        self.db = ContactDatabase(db_path)
        self.export_path = 'exports'
        
        # Ensure export directory exists
        os.makedirs(self.export_path, exist_ok=True)

    def export_todo_contacts(self):
        """
        Export contacts to a Salesforce-compatible CSV
        Filename includes current timestamp
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.export_path}/TODO_contacts_add_to_salesforce_{timestamp}.csv"
        
        # Query all contacts without Salesforce ID
        cursor = self.db.conn.cursor()
        cursor.execute('''
            SELECT name, contact_method, first_met, 
                   met_location, opportunity_notes, campaign_notes 
            FROM contacts 
            WHERE salesforce_id IS NULL
        ''')
        
        contacts = cursor.fetchall()
        
        # Write to CSV
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'Name', 'Contact Method', 'First Met', 
                'Met Location', 'Opportunity Notes', 'Campaign Notes'
            ])
            
            for contact in contacts:
                writer.writerow(contact)
        
        print(f"Exported {len(contacts)} contacts to {filename}")
        return filename

    def __del__(self):
        self.db.close()
