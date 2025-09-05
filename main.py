# main.py
import sys
import os
import pandas as pd

# Ajouter chaque dossier à sys.path
sys.path.append(r"D:\DAH\Data engeneer\seance 4\extract_function")
sys.path.append(r"D:\DAH\Data engeneer\seance 4\transform_function")

# Importer toutes les fonctions de chaque module
from extract_ecommerce import *
from extract_magasin import *
from transform_ecommerce import *
from transform_magasin import *

# Chemin vers le fichier de credentials
credentials_path = r"D:\DAH\Data engeneer\seance 4\service_google\gdrive_credentials.json"
date = "2024-05-02"  # Date spécifique pour le nom du fichier
annee_mois = "2024-05"  # Année et mois pour le nom du fichier


# Test d'extraction de products.csv
folder_id = '1R4J36W2Ijv7eTJxMHBreN2SiD0K237xY'  # ID du dossier spécifique
local_save_path = r"D:\DAH\Data engeneer\seance 4\data_extract\magasin\products"  # Dossier local pour sauvegarde
load_csv_from_drive(folder_id, credentials_path, local_save_path, file_name='products.csv')


# Test d'extraction de clients.csv
folder_id = '1qetyeXKeT9tzZm8wgYd991U3esY_HWxI'  # ID du dossier spécifique
#date = "2024-05-01"  # Date spécifique pour le nom du fichier
local_save_path = r"D:\DAH\Data engeneer\seance 4\data_extract\magasin\clients"  # Dossier local pour sauvegarde
load_csv_from_drive(folder_id, credentials_path, local_save_path, file_name=f'clients_{date}.csv')


# Extraction database .db
folder_id = '1R4J36W2Ijv7eTJxMHBreN2SiD0K237xY'  # ID du dossier Google Drive
local_save_path = r"D:\DAH\Data engeneer\seance 4\data_extract\e-commerce"  # Dossier local pour sauvegarde
db_file_name = 'ecommerce_orders_may2024.db'  # Nom du fichier .db à extraire
load_db_to_csv_from_drive(folder_id, credentials_path, local_save_path, db_file_name)



#                            Calcules des prix unitaires
unit_price()           # Prix unitaire des produits
#                               Pour les magasins

stock_products(date)    # Stocks de produits 
client_magasin(date)    # Clients totaux journalières
ca_magasin(annee_mois)  # Chiffre d' affaire mensuel magasins


#                               Pour site e-commerce

stock_ecommerce(date)    # Stock totale journalière
client_ecommerce(date)    # Clients totaux journalières
ca_ecommerce(annee_mois)  # Chiffre d' affaire mensuel e-commerce