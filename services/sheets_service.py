import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

class SheetsService:
    def __init__(self, json_keyfile_path, sheet_url):
        """
        Initialize the SheetsService with credentials and sheet URL.
        
        Args:
            json_keyfile_path (str): Path to the JSON keyfile for authentication
            sheet_url (str): URL of the Google Sheet
        """
        self.json_keyfile_path = json_keyfile_path
        self.sheet_url = sheet_url
        self.client = None
        self.sheet = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Sheets API and open the sheet."""
        try:
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name(self.json_keyfile_path, scope)
            self.client = gspread.authorize(creds)
            self.sheet = self.client.open_by_url(self.sheet_url).sheet1
        except Exception as e:
            print(f"Error authenticating with Google Sheets: {e}")
            raise
    
    def _get_headers(self):
        """Get headers from the sheet (using row 2)."""
        try:
            return self.sheet.row_values(2)
        except Exception as e:
            print(f"Error getting headers: {e}")
            return []
    
    def _find_column_indexes(self, headers):
        """
        Find the column indexes for specific headers.
        
        Args:
            headers (list): List of headers from the sheet
            
        Returns:
            dict: Dictionary mapping column names to their indexes
        """
        column_mapping = {
            'date': headers.index('Date') if 'Date' in headers else -1,
            'learner': headers.index('Learner') if 'Learner' in headers else -1,
            'theme': headers.index('Theme') if 'Theme' in headers else -1,
            'voice': headers.index('Voice') if 'Voice' in headers else -1,
            'slides': headers.index('Slides') if 'Slides' in headers else -1,
            'body_language': headers.index('Body Language') if 'Body Language' in headers else -1
        }
        return column_mapping
    
    def get_techtalk_message_if_today(self):
        """
        Get tech talk message if there's one scheduled for today.
        
        Returns:
            str: Tech talk message or "No tech talk planned for today."
        """
        try:
            # Get headers and column indexes
            headers = self._get_headers()
            print("Actual Headers in Sheet:", headers)  # For debugging
            
            column_indexes = self._find_column_indexes(headers)
            
            # Get all records from the sheet
            records = self.sheet.get_all_records(head=2, expected_headers=headers)
            
            # Get today's date in the expected format
            today = datetime.today()
            today_str = f"{today.day}/{today.month}/{today.strftime('%y')}"
            print(f"Today's date: {today_str}")  # For debugging
            
            # Search for today's tech talk
            for row in records:
                date_value = str(row.get(headers[column_indexes['date']], "")).strip() if column_indexes['date'] != -1 else ""
                
                if date_value == today_str:
                    learner = row.get(headers[column_indexes['learner']], "").strip() if column_indexes['learner'] != -1 else ""
                    theme = row.get(headers[column_indexes['theme']], "").strip() if column_indexes['theme'] != -1 else ""
                    
                    # Check if learner and theme are specified
                    if not learner or not theme:
                        return "No tech talk planned for today."
                    
                    # Get feedback columns
                    voice = row.get(headers[column_indexes['voice']], "N/A") if column_indexes['voice'] != -1 else "N/A"
                    slides = row.get(headers[column_indexes['slides']], "N/A") if column_indexes['slides'] != -1 else "N/A"
                    body_lang = row.get(headers[column_indexes['body_language']], "N/A") if column_indexes['body_language'] != -1 else "N/A"
                    
                    # Format the message
                    msg = (
                        f"\n🎤 TECH-TALK ALERT 🎤\n"
                        f"Learner: {learner}\n"
                        f"Theme: {theme}\n"
                        "\n-----------------------------\n"
                        f"Feedback:\n"
                        f"Voice: {voice}\n"
                        f"Slides: {slides}\n"
                        f"Body Language: {body_lang}"
                    )
                    return msg
            
            return "No tech talk planned for today."
            
        except Exception as e:
            print(f"Error fetching tech talk data: {e}")
            return "No tech talk planned for today."
    
    def get_all_techtalks(self):
        """
        Get all tech talks from the sheet.
        
        Returns:
            list: List of dictionaries containing tech talk data
        """
        try:
            headers = self._get_headers()
            column_indexes = self._find_column_indexes(headers)
            records = self.sheet.get_all_records(head=2, expected_headers=headers)
            
            techtalks = []
            for row in records:
                date_value = str(row.get(headers[column_indexes['date']], "")).strip() if column_indexes['date'] != -1 else ""
                learner = row.get(headers[column_indexes['learner']], "").strip() if column_indexes['learner'] != -1 else ""
                theme = row.get(headers[column_indexes['theme']], "").strip() if column_indexes['theme'] != -1 else ""
                
                # Only include rows with valid data
                if date_value and learner and theme:
                    voice = row.get(headers[column_indexes['voice']], "N/A") if column_indexes['voice'] != -1 else "N/A"
                    slides = row.get(headers[column_indexes['slides']], "N/A") if column_indexes['slides'] != -1 else "N/A"
                    body_lang = row.get(headers[column_indexes['body_language']], "N/A") if column_indexes['body_language'] != -1 else "N/A"
                    
                    techtalks.append({
                        'date': date_value,
                        'learner': learner,
                        'theme': theme,
                        'voice': voice,
                        'slides': slides,
                        'body_language': body_lang
                    })
            
            return techtalks
            
        except Exception as e:
            print(f"Error fetching all tech talks: {e}")
            return []
    
    def refresh_connection(self):
        """Refresh the connection to the Google Sheet."""
        try:
            self._authenticate()
            print("Sheet connection refreshed successfully.")
        except Exception as e:
            print(f"Error refreshing sheet connection: {e}")