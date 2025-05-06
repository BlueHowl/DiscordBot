import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def get_relevant_headers(json_keyfile_path, sheet_url):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_url(sheet_url).sheet1

    raw_data = sheet.get_all_values()
    header_row1 = raw_data[0]
    header_row2 = raw_data[1]

    # Fusionner les en-têtes
    headers = []
    for h1, h2 in zip(header_row1, header_row2):
        if h2.strip():
            headers.append(h2.strip())
        elif h1.strip():
            headers.append(h1.strip())
        else:
            headers.append("Unknown")

    # Liste des colonnes qui nous intéressent
    target_columns = ['Learner', 'Theme', 'Voice', 'Slides', 'Body Language']

    # Trouver les index des colonnes souhaitées
    selected_indexes = [i for i, h in enumerate(headers) if h in target_columns]

    # Afficher les colonnes filtrées ligne par ligne
    filtered_data = []
    for row in raw_data[2:]:  # Ignorer les 2 premières lignes d'en-tête
        filtered_row = [row[i] if row[i].strip() else "N/A" for i in selected_indexes]  # Remplacer les valeurs vides par "N/A"
        filtered_data.append(filtered_row)

    print("Colonnes sélectionnées :", target_columns)
    for row in filtered_data:
        print(row)

if __name__ == "__main__":
    json_keyfile_path = "discordbot.json"  # Replace with your path
    sheet_url = "https://docs.google.com/spreadsheets/d/1FLktNFlFQCHLaEnw_o_0UJDcXnpYxg2ynoZeq_b-iBQ/edit?gid=0#gid=0"  # Replace with your Google Sheet URL
    get_relevant_headers(json_keyfile_path, sheet_url)