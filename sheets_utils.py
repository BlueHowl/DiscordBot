import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def get_techtalk_message_if_today(json_keyfile_path, sheet_url):
    # Autorisations Google Sheets
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, scope)
    client = gspread.authorize(creds)

    # Ouverture de la feuille
    sheet = client.open_by_url(sheet_url).sheet1
    
    # Afficher les en-têtes réelles pour identifier le problème
    headers = sheet.row_values(2)  # Utiliser la 2ème ligne pour les en-têtes
    print("Actual Headers in Sheet:", headers)  # Afficher les en-têtes réelles

    # Identifier la position des colonnes spécifiques
    date_idx = headers.index('Date') if 'Date' in headers else -1
    learner_idx = headers.index('Learner') if 'Learner' in headers else -1
    theme_idx = headers.index('Theme') if 'Theme' in headers else -1
    feedback_idx = headers.index('Feedback_') if 'Feedback_' in headers else -1
    
    # Rechercher les colonnes sous Feedback_
    voice_idx = headers.index('Voice') if 'Voice' in headers else -1
    slides_idx = headers.index('Slides') if 'Slides' in headers else -1
    body_lang_idx = headers.index('Body Language') if 'Body Language' in headers else -1

    # Récupération des données sous forme de dictionnaires avec en-têtes spécifiées
    records = sheet.get_all_records(head=2, expected_headers=headers)  # Passer les en-têtes attendus

    # Date du jour au format attendu
    today_str = datetime.today().strftime('%-d/%-m/%y')
    print(f"Today's date: {today_str}")  # Pour déboguer

    messages = []

    for row in records:
        # Accéder aux valeurs par index
        date_value = str(row.get(headers[date_idx], "")).strip() if date_idx != -1 else ""
        learner = row.get(headers[learner_idx], "N/A") if learner_idx != -1 else "N/A"
        theme = row.get(headers[theme_idx], "N/A") if theme_idx != -1 else "N/A"
        voice = row.get(headers[voice_idx], "N/A") if voice_idx != -1 else "N/A"
        slides = row.get(headers[slides_idx], "N/A") if slides_idx != -1 else "N/A"
        body_lang = row.get(headers[body_lang_idx], "N/A") if body_lang_idx != -1 else "N/A"
        
        # Vérifie si la date correspond à aujourd'hui
        if date_value == today_str:
            msg = (
                f"\n🎤 TECH-TALK ALERT 🎤\n"
                f"Learner: {learner}\n"
                f"Theme: {theme}\n"
                f"Voice: {voice}\n"
                f"Slides: {slides}\n"
                f"Body Language: {body_lang}"
            )
            messages.append(msg)
    print(messages)
    return "\n\n".join(messages) if messages else ""


if __name__ == "__main__":
    json_keyfile_path = "discordbot.json"  # Remplacez par votre chemin
    sheet_url = "https://docs.google.com/spreadsheets/d/1FLktNFlFQCHLaEnw_o_0UJDcXnpYxg2ynoZeq_b-iBQ/edit?gid=0#gid=0"  # Remplacez par l'URL de votre feuille Google

    techtalk_message = get_techtalk_message_if_today(json_keyfile_path, sheet_url)
    if techtalk_message:
        print("Tech Talk Message(s) for Today:")
        print(techtalk_message)
    else:
        print("No tech talks scheduled for today.")