import unittest
import os
import tempfile
import shutil
from unittest.mock import patch

# Import your actual modules
from database import ContactDatabase
from src.file_scanner import FileScanner
from export import SalesforceExporter
from src.scheduler import ContactManager

class TestDatabase(unittest.TestCase):
    """
    Unit tests for database operations
    """
    
    def setUp(self):
        """
        Create temporary database for testing
        """
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.db = ContactDatabase(self.temp_db.name)

    def tearDown(self):
        """
        Clean up temporary database
        """
        self.db.close()
        os.unlink(self.temp_db.name)

    def test_add_contact(self):
        """
        Test adding a contact
        """
        contact_id = self.db.add_contact(
            name="John Doe",
            salesforce_id="SF123",
            contact_method="Email",
            first_met="Conference",
            met_location="San Francisco"
        )
        self.assertIsNotNone(contact_id)
        
        # Verify contact was added
        contact = self.db.get_contact(name="John Doe")
        self.assertEqual(len(contact), 1)
        self.assertEqual(contact[0][1], "John Doe")

    def test_log_interaction(self):
        """
        Test logging an interaction
        """
        contact_id = self.db.add_contact(name="Jane Doe")
        self.db.log_interaction(
            contact_id=contact_id,
            interaction_type="Meeting",
            notes="Initial meeting"
        )
        
        # Verify interaction was logged
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT * FROM interaction_log WHERE contact_id = ?', (contact_id,))
        interaction = cursor.fetchone()
        self.assertIsNotNone(interaction)
        self.assertEqual(interaction[2], "Meeting")

class TestFileScanner(unittest.TestCase):
    """
    Unit tests for file scanning functionality
    """
    
    def setUp(self):
        """Create temporary directory with test files"""
        self.temp_dir = tempfile.mkdtemp()
        self.scanner = FileScanner(self.temp_dir)
        
        # Create test files
        self.create_test_files()

    def tearDown(self):
        """
        Clean up temporary directory
        """
        shutil.rmtree(self.temp_dir)

    def create_test_files(self):
        """
        Create sample files for testing
        """
        # Create CSV file
        with open(os.path.join(self.temp_dir, 'Noun_People.csv'), 'w') as f:
            f.write("name,contact_method,first_met\nJohn Doe,Email,Conference\n")
        
        # Create TXT file
        with open(os.path.join(self.temp_dir, 'Noun_Places.txt'), 'w') as f:
            f.write("San Francisco Office\nNew York Office\n")

    def test_scan_files(self):
        """
        Test file scanning functionality
        """
        contacts = self.scanner.scan_files()
        self.assertGreater(len(contacts), 0)
        
        # Verify CSV parsing
        csv_contact = next((c for c in contacts if c.get('name') == 'John Doe'), None)
        self.assertIsNotNone(csv_contact)
        self.assertEqual(csv_contact['contact_method'], 'Email')

class TestExporter(unittest.TestCase):
    """
    Unit tests for export functionality
    """
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_db = os.path.join(self.temp_dir, 'test.db')
        self.exporter = SalesforceExporter(self.temp_db)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_export_format(self):
        """
        Test export file format
        """
        # Add test data
        self.exporter.db.add_contact(
            name="Test Contact",
            contact_method="Phone",
            first_met="Meeting"
        )
        
        # Export
        export_file = self.exporter.export_todo_contacts()
        
        # Verify export file
        self.assertTrue(os.path.exists(export_file))
        with open(export_file, 'r') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 1)  # Header + data
            self.assertTrue('Name' in lines[0])  # Check header

class TestIntegration(unittest.TestCase):
    """
    Integration tests for the entire system
    """
    
    def setUp(self):
        """
        Set up test environment
        """
        self.temp_dir = tempfile.mkdtemp()
        self.test_data_dir = os.path.join(self.temp_dir, 'data_test')
        os.makedirs(self.test_data_dir)
        self.db_path = os.path.join(self.temp_dir, 'test.db')
        
        # Create test files
        self.create_test_data()

    def tearDown(self):
        """
        Clean up test environment
        """
        shutil.rmtree(self.temp_dir)

    def create_test_data(self):
        """
        Create test data files
        """
        # Create sample Noun_People.csv
        with open(os.path.join(self.test_data_dir, 'Noun_People.csv'), 'w') as f:
            f.write("name,contact_method,first_met\nIntegration Test,Email,Conference\n")

    def test_full_workflow(self):
        """
        Test entire workflow from scanning to export
        """
        manager = ContactManager()
        
        # Run daily process
        manager.daily_process()
        
        # Verify database entries
        contacts = manager.database.get_contact(name="Integration Test")
        self.assertGreater(len(contacts), 0)
        
        # Verify export file was created
        export_files = os.listdir(manager.exporter.export_path)
        self.assertGreater(len(export_files), 0)

class TestSmoke(unittest.TestCase):
    """
    Smoke tests to verify basic functionality
    """
    
    @patch('schedule.every')
    def test_scheduler_startup(self, mock_schedule):
        """
        Verify scheduler starts without errors
        """
        try:
            manager = ContactManager()
            manager.daily_process()
        except Exception as e:
            self.fail(f"Scheduler failed to start: {e}")

    def test_basic_operations(self):
        """
        Verify basic operations work
        """
        try:
            # Test database
            db = ContactDatabase(':memory:')
            db.add_contact("Smoke Test")
            
            # Test file scanner
            scanner = FileScanner()
            scanner.scan_files()
            
            # Test exporter
            exporter = SalesforceExporter(':memory:')
            exporter.export_todo_contacts()
            
        except Exception as e:
            self.fail(f"Basic operations failed: {e}")

if __name__ == '__main__':
    unittest.main()
