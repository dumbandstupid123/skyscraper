import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import asyncio
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

class GoogleSheetsIntegration:
    """Handles Google Sheets integration for client needs assessment forms."""
    
    def __init__(self):
        self.service = None
        self.spreadsheet_id = None
        self._initialize_service()
    
    def _initialize_service(self):
        """Initialize Google Sheets API service."""
        try:
            # Check for service account credentials first
            creds_path = os.environ.get('GOOGLE_SERVICE_ACCOUNT_PATH')
            creds_json = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON')
            
            if creds_json:
                # Use JSON credentials from environment variable
                service_account_info = json.loads(creds_json)
                credentials = service_account.Credentials.from_service_account_info(
                    service_account_info,
                    scopes=['https://www.googleapis.com/auth/spreadsheets']
                )
            elif creds_path and os.path.exists(creds_path):
                # Use credentials file
                credentials = service_account.Credentials.from_service_account_file(
                    creds_path,
                    scopes=['https://www.googleapis.com/auth/spreadsheets']
                )
            else:
                logger.warning("No Google Sheets credentials found. Forms integration will be disabled.")
                return
            
            self.service = build('sheets', 'v4', credentials=credentials)
            self.spreadsheet_id = os.environ.get('GOOGLE_SHEETS_ID')
            
            if not self.spreadsheet_id:
                logger.warning("GOOGLE_SHEETS_ID not set. Forms integration will be disabled.")
                return
                
            logger.info("Google Sheets integration initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets integration: {e}")
            self.service = None
    
    async def create_needs_assessment_sheet(self) -> str:
        """Create a new Google Sheet for needs assessment responses."""
        if not self.service:
            raise Exception("Google Sheets service not initialized")
        
        try:
            # Create new spreadsheet
            spreadsheet = {
                'properties': {
                    'title': f'NextStep Client Needs Assessment - {datetime.now().strftime("%Y-%m-%d")}'
                },
                'sheets': [{
                    'properties': {
                        'title': 'Responses',
                        'gridProperties': {
                            'rowCount': 1000,
                            'columnCount': 20
                        }
                    }
                }]
            }
            
            result = self.service.spreadsheets().create(body=spreadsheet).execute()
            spreadsheet_id = result['spreadsheetId']
            
            # Set up header row for simplified form
            headers = [
                'Timestamp', 'Client Email', 'Client Name', 'Phone Number',
                'Housing Needs', 'Housing Priority', 
                'Food Needs', 'Food Priority',
                'Transportation Needs', 'Transportation Type',
                'Top Priority', 'Additional Notes'
            ]
            
            # Insert headers
            body = {
                'values': [headers]
            }
            
            self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range='Responses!A1:T1',
                valueInputOption='RAW',
                body=body
            ).execute()
            
            # Make the sheet publicly viewable (for form responses)
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={
                    'requests': [{
                        'updateSpreadsheetProperties': {
                            'properties': {
                                'title': f'NextStep Client Needs Assessment - {datetime.now().strftime("%Y-%m-%d")}'
                            },
                            'fields': 'title'
                        }
                    }]
                }
            ).execute()
            
            logger.info(f"Created new needs assessment sheet: {spreadsheet_id}")
            return spreadsheet_id
            
        except HttpError as e:
            logger.error(f"Failed to create Google Sheet: {e}")
            raise
    
    async def get_form_responses(self, sheet_id: str = None) -> List[Dict[str, Any]]:
        """Fetch all form responses from the Google Sheet."""
        if not self.service:
            return []
        
        spreadsheet_id = sheet_id or self.spreadsheet_id
        if not spreadsheet_id:
            logger.warning("No spreadsheet ID provided")
            return []
        
        try:
            # First, get the spreadsheet info to find available sheets
            spreadsheet_info = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            sheets = spreadsheet_info.get('sheets', [])
            
            if not sheets:
                logger.warning("No sheets found in the spreadsheet")
                return []
            
            # Find the first sheet (usually the responses sheet)
            sheet_name = sheets[0]['properties']['title']
            logger.info(f"Using sheet: '{sheet_name}'")
            
            # Get all data from the first sheet
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=f"'{sheet_name}'!A:Z"  # Use A:Z to get more columns
            ).execute()
            
            values = result.get('values', [])
            if not values:
                logger.info("No data found in the sheet")
                return []
            
            # First row contains headers
            headers = values[0] if values else []
            responses = []
            
            logger.info(f"Found headers: {headers}")
            
            # Process each response row
            for row in values[1:]:
                if len(row) == 0:  # Skip empty rows
                    continue
                
                # Pad row to match headers length
                while len(row) < len(headers):
                    row.append('')
                
                response = {}
                for i, header in enumerate(headers):
                    response[header] = row[i] if i < len(row) else ''
                
                # Parse and structure the response (SIMPLIFIED VERSION)
                structured_response = {
                    'timestamp': response.get('Timestamp', ''),
                    'client_email': response.get('Email Address', response.get('Client Email', '')),
                    'client_name': response.get('Full Name', response.get('Client Name', '')),
                    'phone_number': response.get('Phone Number', ''),
                    'needs_assessment': {
                        'housing': {
                            'needed': response.get('Do you currently need housing assistance?', response.get('Housing Needs', '')).lower() == 'yes',
                            'priority': self._map_priority(response.get('If yes, how urgent is your housing need?', response.get('Housing Priority', ''))),
                            'details': response.get('If yes, how urgent is your housing need?', response.get('Housing Priority', ''))
                        },
                        'food': {
                            'needed': response.get('Do you need food assistance?', response.get('Food Needs', '')).lower() == 'yes',
                            'priority': self._map_priority(response.get('If yes, how urgent is your food need?', response.get('Food Priority', ''))),
                            'details': response.get('If yes, how urgent is your food need?', response.get('Food Priority', ''))
                        },
                        'transportation': {
                            'needed': response.get('Do you need transportation assistance?', response.get('Transportation Needs', '')).lower() == 'yes',
                            'priority': 'medium',  # Default priority for transportation
                            'details': response.get('If yes, what type of transportation help do you need?', response.get('Transportation Type', ''))
                        }
                    },
                    'top_priority': response.get('Top Priority', ''),
                    'additional_notes': response.get('Additional Notes', ''),
                    'processed': False  # Flag to track if this response has been processed
                }
                
                responses.append(structured_response)
            
            logger.info(f"Retrieved {len(responses)} form responses")
            return responses
            
        except HttpError as e:
            logger.error(f"Failed to get form responses: {e}")
            return []
    
    async def get_new_responses_since(self, last_check: datetime) -> List[Dict[str, Any]]:
        """Get only new responses since the last check."""
        all_responses = await self.get_form_responses()
        new_responses = []
        
        for response in all_responses:
            try:
                # Parse timestamp from Google Forms (format: M/D/YYYY H:MM:SS)
                timestamp_str = response.get('timestamp', '')
                if timestamp_str:
                    # Try different timestamp formats
                    for fmt in ['%m/%d/%Y %H:%M:%S', '%Y-%m-%d %H:%M:%S', '%m/%d/%Y %I:%M:%S %p']:
                        try:
                            response_time = datetime.strptime(timestamp_str, fmt)
                            break
                        except ValueError:
                            continue
                    else:
                        # If no format works, skip this response
                        logger.warning(f"Could not parse timestamp: {timestamp_str}")
                        continue
                    
                    if response_time > last_check:
                        new_responses.append(response)
            except Exception as e:
                logger.error(f"Error processing response timestamp: {e}")
                continue
        
        logger.info(f"Found {len(new_responses)} new responses since {last_check}")
        return new_responses
    
    def _map_priority(self, priority_text):
        """Map priority text from form to standard priority levels."""
        if not priority_text:
            return 'low'
        
        priority_lower = priority_text.lower()
        
        if 'emergency' in priority_lower or 'today' in priority_lower:
            return 'high'
        elif 'urgent' in priority_lower or 'week' in priority_lower:
            return 'high'
        elif 'soon' in priority_lower or 'month' in priority_lower:
            return 'medium'
        elif 'ongoing' in priority_lower or 'planning' in priority_lower:
            return 'low'
        else:
            return 'medium'  # Default to medium priority
    
    def generate_form_url(self, client_email: str = None) -> str:
        """Generate a Google Form URL for client needs assessment."""
        # This would typically be a pre-created Google Form
        # For now, we'll return a template URL that you can customize
        base_form_url = "https://forms.gle/YOUR_FORM_ID"
        
        if client_email:
            # Pre-fill the email field
            return f"{base_form_url}?usp=pp_url&entry.EMAIL_FIELD_ID={client_email}"
        
        return base_form_url 