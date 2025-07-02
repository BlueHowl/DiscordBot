import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.sheets_service import SheetsService

def test_sheets_service():
    """Test the new SheetsService class."""
    json_keyfile_path = "discordbot.json"
    sheet_url = "https://docs.google.com/spreadsheets/d/1FLktNFlFQCHLaEnw_o_0UJDcXnpYxg2ynoZeq_b-iBQ/edit?gid=0#gid=0"
    
    try:
        # Initialize the service
        sheets_service = SheetsService(json_keyfile_path, sheet_url)
        
        # Test getting today's tech talk
        print("Testing get_techtalk_message_if_today()...")
        techtalk_message = sheets_service.get_techtalk_message_if_today()
        print("Result:", techtalk_message)
        
        # Test getting all tech talks
        print("\nTesting get_all_techtalks()...")
        all_techtalks = sheets_service.get_all_techtalks()
        print(f"Found {len(all_techtalks)} tech talks")
        
        if all_techtalks:
            print("First few tech talks:")
            for i, tt in enumerate(all_techtalks[:3]):
                print(f"  {i+1}. {tt['date']} - {tt['learner']}: {tt['theme']}")
        
        print("\n✅ SheetsService is working correctly!")
        
    except Exception as e:
        print(f"❌ Error testing SheetsService: {e}")

def get_relevant_headers(json_keyfile_path, sheet_url):
    """Legacy function for testing headers - now using SheetsService."""
    try:
        sheets_service = SheetsService(json_keyfile_path, sheet_url)
        headers = sheets_service._get_headers()
        
        # Liste des colonnes qui nous intéressent
        target_columns = ['Learner', 'Theme', 'Voice', 'Slides', 'Body Language']
        
        # Trouver les index des colonnes souhaitées
        selected_indexes = [i for i, h in enumerate(headers) if h in target_columns]
        
        # Get all records and filter
        records = sheets_service.sheet.get_all_records(head=2, expected_headers=headers)
        
        print("Colonnes sélectionnées :", target_columns)
        for row in records[:5]:  # Limit to first 5 rows for testing
            filtered_row = [str(row.get(headers[i], "N/A")) for i in selected_indexes]
            print(filtered_row)
            
    except Exception as e:
        print(f"Error in get_relevant_headers: {e}")

if __name__ == "__main__":
    test_sheets_service()
    print("\n" + "="*50 + "\n")
    json_keyfile_path = "discordbot.json"
    sheet_url = "https://docs.google.com/spreadsheets/d/1FLktNFlFQCHLaEnw_o_0UJDcXnpYxg2ynoZeq_b-iBQ/edit?gid=0#gid=0"
    get_relevant_headers(json_keyfile_path, sheet_url)