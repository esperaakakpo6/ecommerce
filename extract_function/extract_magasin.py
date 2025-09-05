from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import pandas as pd
import io
import os

def load_csv_from_drive(folder_id, credentials_path, local_save_path, file_name=None):
    # Créer le dossier local si inexistant
    os.makedirs(local_save_path, exist_ok=True)
    
    # Authentification
    gauth = GoogleAuth()
    gauth.settings['access_type'] = 'offline'
    gauth.LoadCredentialsFile(credentials_path)
    if gauth.credentials is None or gauth.access_token_expired:
        gauth.LocalWebserverAuth()
        gauth.SaveCredentialsFile(credentials_path)
    
    drive = GoogleDrive(gauth)
    
    # Construire la requête pour lister les fichiers CSV dans le dossier spécifié
    query = f"'{folder_id}' in parents and mimeType='text/csv' and trashed=false"
    if file_name:
        query += f" and title='{file_name}'"  # Filtrer par nom de fichier
    
    list_file = drive.ListFile({'q': query}).GetList()
    
    # Vérifier si des fichiers ont été trouvés
    if not list_file:
        print(f"Aucun fichier trouvé pour {file_name or 'tous les CSV'} dans le dossier.")
        return []
    
    # Charger et sauvegarder le fichier CSV
    dataframes = []
    for file in list_file:
        print(f"Chargement et sauvegarde : {file['title']} (ID: {file['id']})")
        file_io = io.BytesIO(file.GetContentString().encode('utf-8'))
        df = pd.read_csv(file_io)
        dataframes.append((file['title'], df))
        # Sauvegarder le fichier localement
        local_file_path = os.path.join(local_save_path, file['title'])
        file.GetContentFile(local_file_path, mimetype='text/csv')
    
    print(f"Fichiers sauvegardés dans : {local_save_path}")
    return dataframes
