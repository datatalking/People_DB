import time
import datetime
from src.file_scanner import FileScanner
from src.database_script import ContactDatabase
from src.export_script import SalesforceExporter


class ContactManager:
    def __init__(self):
        self.file_scanner = FileScanner()
        self.database = ContactDatabase()
        self.exporter = SalesforceExporter()

    def daily_process(self):
        """
        Run daily data collection and processing
        """
        start_time = datetime.datetime.now()
        
        # Scan files and extract contacts
        contacts = self.file_scanner.scan_files()
        
        # Add new contacts to database
        for contact in contacts:
            self.database.add_contact(
                name=contact.get('name', 'Unknown'),
                contact_method=contact.get('contact_method'),
                first_met=contact.get('first_met'),
                met_location=contact.get('met_location'),
                opportunity_notes=contact.get('opportunity_notes'),
                campaign_notes=contact.get('campaign_notes')
            )
        
        # Export contacts for Salesforce
        self.exporter.export_todo_contacts()
        
        end_time = datetime.datetime.now()
        total_lapse_time = end_time - start_time
        
        print(f"Daily process completed in {total_lapse_time}")


def run_scheduler():
    """
    start the daily 6am scheduler
    :return:
    """
    contact_manager = ContactManager()
    
    # Schedule daily job at 6 AM
    schedule.every().day.at("06:00").do(contact_manager.daily_process)
    
    print("Scheduler started. Waiting for next scheduled run...")
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_scheduler()
