import gspread
from google.oauth2.service_account import Credentials
from typing import List, Dict, Optional
import os
from datetime import datetime
import json


class SpreadsheetTracker:
    """Track LinkedIn outreach in Google Sheets"""
    
    def __init__(self, spreadsheet_name: str = "LinkedIn Outreach Tracker"):
        self.spreadsheet_name = spreadsheet_name
        self.client = None
        self.spreadsheet = None
        self.worksheet = None
        
        # Define the headers for the spreadsheet
        self.headers = [
            "Timestamp",
            "Company Name",
            "Position Applied",
            "Contact Name",
            "Contact Title",
            "Connection Status",
            "Message Sent",
            "Response Status",
            "Notes"
        ]
    
    def authenticate(self, credentials_file: str = "credentials.json"):
        """
        Authenticate with Google Sheets API
        
        Args:
            credentials_file: Path to Google service account credentials JSON
        """
        # Define the scope
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        try:
            if os.path.exists(credentials_file):
                # Use service account credentials
                creds = Credentials.from_service_account_file(credentials_file, scopes=scope)
                self.client = gspread.authorize(creds)
                print("✅ Authenticated with Google Sheets API using service account")
            else:
                print(f"⚠️  Credentials file not found: {credentials_file}")
                print("💡 To use Google Sheets integration:")
                print("   1. Go to https://console.cloud.google.com/")
                print("   2. Create a new project or select existing one")
                print("   3. Enable Google Sheets API and Google Drive API")
                print("   4. Create service account credentials")
                print("   5. Download JSON and save as 'credentials.json'")
                print("   6. Share your spreadsheet with the service account email")
                return False
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
        
        return True
    
    def create_or_open_spreadsheet(self):
        """Create a new spreadsheet or open existing one"""
        if not self.client:
            print("❌ Not authenticated. Call authenticate() first.")
            return False
        
        try:
            # Try to open existing spreadsheet
            self.spreadsheet = self.client.open(self.spreadsheet_name)
            print(f"📊 Opened existing spreadsheet: {self.spreadsheet_name}")
        except gspread.exceptions.SpreadsheetNotFound:
            # Create new spreadsheet
            self.spreadsheet = self.client.create(self.spreadsheet_name)
            print(f"📊 Created new spreadsheet: {self.spreadsheet_name}")
        
        # Get or create the first worksheet
        try:
            self.worksheet = self.spreadsheet.sheet1
        except:
            self.worksheet = self.spreadsheet.add_worksheet(title="Outreach Log", rows=1000, cols=20)
        
        # Set up headers if sheet is empty
        if not self.worksheet.row_values(1):
            self.worksheet.append_row(self.headers)
            self.format_header_row()
            print("✅ Headers added to spreadsheet")
        
        return True
    
    def format_header_row(self):
        """Format the header row to make it stand out"""
        if not self.worksheet:
            return
        
        try:
            # Bold the header row
            self.worksheet.format('A1:I1', {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 0.8, "green": 0.8, "blue": 0.8}
            })
        except Exception as e:
            print(f"⚠️  Could not format headers: {e}")
    
    def add_outreach_record(self, record: Dict[str, str]):
        """
        Add a single outreach record to the spreadsheet
        
        Args:
            record: Dictionary with outreach information
        """
        if not self.worksheet:
            print("❌ Worksheet not initialized. Call create_or_open_spreadsheet() first.")
            return False
        
        try:
            row_data = [
                record.get('timestamp', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                record.get('company', ''),
                record.get('position', ''),
                record.get('name', ''),
                record.get('contact_title', ''),
                record.get('status', 'Pending'),
                record.get('message_sent', 'Yes'),
                record.get('response_status', 'No Response'),
                record.get('notes', '')
            ]
            
            self.worksheet.append_row(row_data)
            print(f"✅ Added record for {record.get('name', 'Unknown')} at {record.get('company', 'Unknown')}")
            return True
            
        except Exception as e:
            print(f"❌ Error adding record: {e}")
            return False
    
    def add_multiple_records(self, records: List[Dict[str, str]]):
        """
        Add multiple outreach records at once
        
        Args:
            records: List of dictionaries with outreach information
        """
        if not self.worksheet:
            print("❌ Worksheet not initialized. Call create_or_open_spreadsheet() first.")
            return False
        
        success_count = 0
        for record in records:
            if self.add_outreach_record(record):
                success_count += 1
        
        print(f"✅ Successfully added {success_count}/{len(records)} records to spreadsheet")
        return success_count == len(records)
    
    def get_spreadsheet_url(self) -> Optional[str]:
        """Get the URL of the spreadsheet"""
        if self.spreadsheet:
            return self.spreadsheet.url
        return None
    
    def update_response_status(self, row_number: int, status: str, notes: str = ""):
        """
        Update the response status for a specific row
        
        Args:
            row_number: The row number to update (2-indexed, as row 1 is headers)
            status: New response status
            notes: Additional notes
        """
        if not self.worksheet:
            return False
        
        try:
            # Update response status column (H) and notes column (I)
            self.worksheet.update_cell(row_number, 8, status)
            if notes:
                self.worksheet.update_cell(row_number, 9, notes)
            print(f"✅ Updated row {row_number} with status: {status}")
            return True
        except Exception as e:
            print(f"❌ Error updating row: {e}")
            return False


class LocalSpreadsheetTracker:
    """Fallback tracker using local CSV file"""
    
    def __init__(self, filename: str = "linkedin_outreach.csv"):
        self.filename = filename
        self.headers = [
            "Timestamp",
            "Company Name",
            "Position Applied",
            "Contact Name",
            "Contact Title",
            "Connection Status",
            "Message Sent",
            "Response Status",
            "Notes"
        ]
        
        # Create file with headers if it doesn't exist
        if not os.path.exists(self.filename):
            import csv
            with open(self.filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.headers)
            print(f"✅ Created local tracking file: {self.filename}")
    
    def add_outreach_record(self, record: Dict[str, str]):
        """Add a single record to the CSV file"""
        import csv
        
        row_data = [
            record.get('timestamp', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            record.get('company', ''),
            record.get('position', ''),
            record.get('name', ''),
            record.get('contact_title', ''),
            record.get('status', 'Pending'),
            record.get('message_sent', 'Yes'),
            record.get('response_status', 'No Response'),
            record.get('notes', '')
        ]
        
        try:
            with open(self.filename, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(row_data)
            print(f"✅ Added record to {self.filename}")
            return True
        except Exception as e:
            print(f"❌ Error writing to CSV: {e}")
            return False
    
    def add_multiple_records(self, records: List[Dict[str, str]]):
        """Add multiple records to the CSV file"""
        success_count = sum(1 for record in records if self.add_outreach_record(record))
        print(f"✅ Added {success_count}/{len(records)} records to {self.filename}")
        return success_count == len(records)


if __name__ == "__main__":
    print("🗂️  Spreadsheet Tracker Module")
    print("\nUsage:")
    print("  - For Google Sheets: Use SpreadsheetTracker()")
    print("  - For local CSV: Use LocalSpreadsheetTracker()")
    
    # Test with local tracker
    local_tracker = LocalSpreadsheetTracker()
    test_record = {
        'company': 'Test Company',
        'position': 'Software Engineer',
        'name': 'John Doe',
        'contact_title': 'Senior Engineer',
        'status': 'Connection Sent',
        'notes': 'Test entry'
    }
    local_tracker.add_outreach_record(test_record)
    print(f"\n✅ Test record added to linkedin_outreach.csv")
