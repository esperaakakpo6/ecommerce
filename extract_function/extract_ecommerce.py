import sqlite3
import pandas as pd
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os
import io

def load_db_to_csv_from_drive(folder_id, credentials_path, local_save_path, db_file_name):
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
    
    # Requête pour trouver le fichier .db spécifique
    query = f"'{folder_id}' in parents and title='{db_file_name}' and trashed=false"
    file_list = drive.ListFile({'q': query}).GetList()
    
    # Vérifier si le fichier a été trouvé
    if not file_list:
        print(f"Aucun fichier nommé {db_file_name} trouvé dans le dossier.")
        return
    
    # Télécharger et traiter le fichier .db
    db_file = file_list[0]
    print(f"Chargement : {db_file['title']} (ID: {db_file['id']})")
    
    # Sauvegarder le fichier .db localement
    local_db_path = os.path.join(local_save_path, db_file['title'])
    db_file.GetContentFile(local_db_path)
    print(f"Fichier .db sauvegardé dans : {local_db_path}")
    
    # Connexion à la base de données SQLite
    conn = sqlite3.connect(local_db_path)
    
    # Lister toutes les tables dans la base de données
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # Convertir chaque table en CSV
    for table_name in tables:
        table_name = table_name[0]
        print(f"Conversion de la table {table_name} en CSV...")
        
        # Lire la table dans un DataFrame
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        
        # Sauvegarder le DataFrame en CSV
        csv_file_name = f"{table_name}.csv"
        local_csv_path = os.path.join(local_save_path, csv_file_name)
        df.to_csv(local_csv_path, index=False, encoding='utf-8')
        print(f"Fichier CSV sauvegardé dans : {local_csv_path}")
    
    # Fermer la connexion à la base de données
    conn.close()
    print("Traitement terminé.")

