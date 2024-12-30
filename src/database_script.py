import sqlite3
import os
from datetime import datetime

class ContactDatabase:
    def __init__(self, db_path='data/contacts.db'):
        """Initialize database connection and create tables if not exists"""
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()

    def create_tables(self):
        """Create necessary tables for contact management"""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                salesforce_id TEXT,
                contact_method TEXT,
                first_met TEXT,
                met_location TEXT,
                opportunity_notes TEXT,
                campaign_notes TEXT,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interaction_log (
                id INTEGER PRIMARY KEY,
                contact_id INTEGER,
                interaction_date DATETIME,
                interaction_type TEXT,
                notes TEXT,
                FOREIGN KEY(contact_id) REFERENCES contacts(id)
            )
        ''')
        
        self.conn.commit()

    def add_contact(self, name, salesforce_id=None, contact_method=None, 
                    first_met=None, met_location=None, 
                    opportunity_notes=None, campaign_notes=None):
        """Add a new contact to the database"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO contacts 
            (name, salesforce_id, contact_method, first_met, 
             met_location, opportunity_notes, campaign_notes) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, salesforce_id, contact_method, first_met, 
              met_location, opportunity_notes, campaign_notes))
        self.conn.commit()
        return cursor.lastrowid

    def get_contact(self, name=None, salesforce_id=None):
        """Retrieve contact information"""
        cursor = self.conn.cursor()
        if name:
            cursor.execute('SELECT * FROM contacts WHERE name = ?', (name,))
        elif salesforce_id:
            cursor.execute('SELECT * FROM contacts WHERE salesforce_id = ?', (salesforce_id,))
        return cursor.fetchall()

    def log_interaction(self, contact_id, interaction_type, notes):
        """Log an interaction with a contact"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO interaction_log 
            (contact_id, interaction_date, interaction_type, notes) 
            VALUES (?, ?, ?, ?)
        ''', (contact_id, datetime.now(), interaction_type, notes))
        self.conn.commit()

    def close(self):
        """Close database connection"""
        self.conn.close()
