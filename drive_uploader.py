from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

# Chemin vers ton fichier de clé JSON
SERVICE_ACCOUNT_FILE = 'forensicsuploader-a5808924a525.json'

# Scope pour accéder à Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Créer les identifiants
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Créer le service Drive
service = build('drive', 'v3', credentials=credentials)

# ID du dossier Drive dans lequel stocker les artefacts
FOLDER_ID = '1_IsGiGnEQETy41HCM_XA1SqwlR0PAAYq'

def upload_to_drive(filepath):
    """Upload d'un fichier JSON vers un dossier spécifique de Google Drive"""
    if not os.path.exists(filepath):
        print(f"Le fichier {filepath} n'existe pas.")
        return

    file_metadata = {
        'name': os.path.basename(filepath),
        'parents': [FOLDER_ID]  # dossier cible
    }
    media = MediaFileUpload(filepath, mimetype='application/json')

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    print(f"Fichier téléversé avec succès. ID: {file.get('id')}")
    print(f"Voir : https://drive.google.com/file/d/{file.get('id')}/view")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage : python drive_uploader.py <chemin_du_fichier>")
    else:
        upload_to_drive(sys.argv[1])
