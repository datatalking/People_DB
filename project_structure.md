# Personal Contact Management System

## Project Overview
This is a personal contact management system that:
- Tracks contact information
- Integrates with Salesforce
- Automates daily data collection
- Provides export functionality

## Key Features
- SQLite database for contact storage
- Python-based data management
- Automated daily scanning of data folders
- CSV export for Salesforce integration

## Project Structure
```
personal_contact_manager/
│
├── data/                  # Data storage directory
│   └── contacts.db        # SQLite database
│
├── src/                   # Source code directory
│   ├── database.py        # Database connection and operations
│   ├── file_scanner.py    # File scanning and data extraction
│   ├── export.py          # Salesforce export functionality
│   └── scheduler.py       # Daily scheduled tasks
│
├── test/                  # Test scripts directory
│   ├── test_database.py
│   ├── test_file_scanner.py
│   └── test_export.py
│
├── config/                # Configuration files
│   └── config.ini
│
└── README.md              # Project documentation
```

## Setup Instructions
1. Ensure Python 3.10+ is installed
2. Install required dependencies:
   ```
   pip install sqlite3 schedule python-dateutil
   ```
3. Configure paths in `config/config.ini`
4. Run `python src/scheduler.py` to start automated processes
```
