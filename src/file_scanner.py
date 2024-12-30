import os
import re
import csv
from typing import List, Dict


class FileScanner:
    def __init__(self, base_path='~/Users/user_name/sbox/data_test'):
        self.base_path = os.path.expanduser(base_path)
        self.patterns = [
            r'Noun_People\.txt',
            r'Noun_People\.csv',
            r'Noun_Places\.txt',
            r'Noun_Places\.csv',
            r'Noun_Thing\.txt',
            r'Noun_Thing\.csv',
            r'Noun_Idea\.txt',
            r'Noun_Idea\.csv'
        ]

    def scan_files(self) -> List[Dict[str, str]]:
        """
        Scan the specified directory for matching files
        and extract contact information
        """
        contacts = []
        for root, _, files in os.walk(self.base_path):
            for filename in files:
                if any(re.match(pattern, filename) for pattern in self.patterns):
                    file_path = os.path.join(root, filename)
                    contacts.extend(self._parse_file(file_path))
        return contacts

    def _parse_file(self, file_path: str) -> List[Dict[str, str]]:
        """
        Parse individual files based on their extension
        """
        contacts = []
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_ext == '.txt':
                contacts = self._parse_txt(file_path)
            elif file_ext == '.csv':
                contacts = self._parse_csv(file_path)
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
        
        return contacts

    def _parse_txt(self, file_path: str) -> List[Dict[str, str]]:
        """Parse txt files"""
        contacts = []
        with open(file_path, 'r', encoding='utf-8') as f:
            # Implement your txt parsing logic here
            # This is a placeholder implementation
            for line in f:
                contacts.append({
                    'name': line.strip(),
                    'source_file': file_path
                })
        return contacts

    def _parse_csv(self, file_path: str) -> List[Dict[str, str]]:
        """Parse CSV files"""
        contacts = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                contacts.append({
                    **row,
                    'source_file': file_path
                })
        return contacts
