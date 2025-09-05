# Pipeline de Traitement des Données E-commerce et Magasin

## Aperçu

Ce projet est un pipeline de traitement de données conçu pour extraire, transformer et analyser les données provenant d'une plateforme de commerce en ligne et de magasins physiques. Il traite les données relatives aux commandes, produits, stocks, clients et chiffre d'affaires pour une période donnée. Le pipeline est développé en Python et utilise des bibliothèques telles que `pandas` pour la manipulation des données et `PyDrive2` pour interagir avec Google Drive afin de récupérer les données brutes.

Le pipeline se compose de deux grandes étapes :

1. **Extraction des données** : Télécharge les données depuis Google Drive (fichiers CSV pour les magasins et base de données SQLite pour l'e-commerce).
2. **Transformation des données** : Nettoie et traite les données pour calculer des indicateurs clés tels que les prix unitaires, le stock total, le nombre de clients et le chiffre d'affaires mensuel.

Les données transformées sont enregistrées sous forme de fichiers CSV dans des répertoires désignés pour une analyse ou un reporting ultérieur.

## Structure du Projet

Le projet est organisé autour des fichiers suivants :

- `main.py` : Point d'entrée du pipeline. Il orchestre les processus d'extraction et de transformation en appelant les fonctions des modules `extract` et `transform`.
- `extract_ecommerce.py` : Extrait les données e-commerce à partir d'une base de données SQLite stockée sur Google Drive et convertit les tables en fichiers CSV.
- `extract_magasin.py` : Télécharge les fichiers CSV liés aux magasins (ex. : `products.csv`, `clients_YYYY-MM-DD.csv`) depuis Google Drive.
- `transform_ecommerce.py` : Traite les données e-commerce pour calculer les prix unitaires, le stock quotidien, le nombre de clients uniques quotidiens et le chiffre d'affaires mensuel.
- `transform_magasin.py` : Traite les données des magasins pour calculer le stock, le nombre de clients et le chiffre d'affaires mensuel, en intégrant les prix unitaires des données e-commerce.

### Structure des Répertoires

```
D:\DAH\Data engeneer\seance 4\
├── data_extract\
│   ├── e-commerce\
│   │   └── ecommerce_orders.csv
│   └── magasin\
│       ├── products\
│       │   └── products.csv
│       └── clients\
│           └── clients_YYYY-MM-DD.csv
├── data_transform\
│   ├── e-commerce\
│   │   ├── unit_price\
│   │   │   └── unit_price.csv
│   │   ├── stock\
│   │   │   └── stock_total_YYYY-MM-DD.csv
│   │   ├── clients\
│   │   │   └── client_total_YYYY-MM-DD.csv
│   │   └── CA\
│   │       └── ca_YYYY-MM.csv
│   └── magasin\
│       ├── stock\
│       │   └── stock_total_YYYY-MM-DD.csv
│       ├── clients\
│       │   └── client_total_YYYY-MM-DD.csv
│       └── CA\
│           └── ca_YYYY-MM.csv
├── extract_function\
│   ├── extract_ecommerce.py
│   └── extract_magasin.py
├── transform_function\
│   ├── transform_ecommerce.py
│   └── transform_magasin.py
├── service_google\
│   └── gdrive_credentials.json
└── main.py
```

## Prérequis

Pour exécuter ce projet, assurez-vous d'avoir installé :

- Python 3.8 ou supérieur
- Les packages Python requis (installez via `pip`) :

  ```bash
  pip install pandas pydrive2
  ```
- Les identifiants de l'API Google Drive (`gdrive_credentials.json`) pour accéder aux fichiers sur Google Drive. Suivez la documentation PyDrive2 pour configurer l'authentification.
- Accès aux dossiers Google Drive contenant les fichiers de données brutes (les identifiants des dossiers sont spécifiés dans `main.py`).

## Configuration

1. **Cloner le Dépôt** :

   ```bash
   git clone https://github.com/votre-nom-utilisateur/votre-depot.git
   cd votre-depot
   ```

2. **Installer les Dépendances** :

   ```bash
   pip install -r requirements.txt
   ```

   Créez un fichier `requirements.txt` avec :

   ```
   pandas
   pydrive2
   ```

3. **Configurer les Identifiants Google Drive** :

   - Placez le fichier `gdrive_credentials.json` dans le répertoire `service_google`.
   - Mettez à jour la variable `credentials_path` dans `main.py` si le fichier est stocké ailleurs.

4. **Mettre à jour les Identifiants des Dossiers** :

   - Dans `main.py`, assurez-vous que les variables `folder_id` correspondent aux identifiants des dossiers Google Drive contenant vos fichiers de données.
   - Mettez à jour les variables `local_save_path` pour correspondre à votre structure de répertoires locaux si nécessaire.

5. **Fichiers de Données** :

   - Assurez-vous que les dossiers Google Drive contiennent les fichiers requis :
     - Pour l'e-commerce : `ecommerce_orders_may2024.db` (base de données SQLite).
     - Pour les magasins : `products.csv` et `clients_YYYY-MM-DD.csv`.

## Utilisation

Exécutez le pipeline en lançant `main.py` :

```bash
python main.py
```

### Fonctionnement du Pipeline

1. **Extraction des Données** :

   - Télécharge `products.csv` et `clients_YYYY-MM-DD.csv` pour les données des magasins.
   - Télécharge et convertit la base de données SQLite `ecommerce_orders_may2024.db` en fichiers CSV (ex. : `ecommerce_orders.csv`).

2. **Transformation des Données** :

   - **E-commerce** :
     - Nettoie les données e-commerce (`ecommerce_orders.csv`) en supprimant les doublons, en convertissant les types de données et en ajoutant une colonne `annee_mois`.
     - Calcule les prix unitaires (`unit_price.csv`).
     - Calcule le stock quotidien (`stock_total_YYYY-MM-DD.csv`).
     - Calcule le nombre de clients uniques quotidiens (`client_total_YYYY-MM-DD.csv`).
     - Calcule le chiffre d'affaires mensuel (`ca_YYYY-MM.csv`).
   - **Magasins** :
     - Nettoie les données des magasins (`products.csv`) en supprimant les doublons, en convertissant les types de données et en ajoutant une colonne `annee_mois`.
     - Calcule le stock quotidien (`stock_total_YYYY-MM-DD.csv`).
     - Calcule le nombre de clients quotidiens (`client_total_YYYY-MM-DD.csv`).
     - Calcule le chiffre d'affaires mensuel (`ca_YYYY-MM.csv`) en utilisant les prix unitaires des données e-commerce.

3. **Enregistrement des Résultats** :

   - Toutes les données transformées sont enregistrées sous forme de fichiers CSV dans le répertoire `data_transform`, organisées par type de données (ex. : `unit_price`, `stock`, `clients`, `CA`).

### Exemple de Sortie

Pour une date de `2024-05-02` et un `annee_mois` de `2024-05`, le pipeline génère des fichiers tels que :

- `data_transform/e-commerce/unit_price/unit_price.csv`
- `data_transform/e-commerce/stock/stock_total_2024-05-02.csv`
- `data_transform/e-commerce/clients/client_total_2024-05-02.csv`
- `data_transform/e-commerce/CA/ca_2024-05.csv`
- `data_transform/magasin/stock/stock_total_2024-05-02.csv`
- `data_transform/magasin/clients/client_total_2024-05-02.csv`
- `data_transform/magasin/CA/ca_2024-05.csv`

## Contribution

Les contributions sont les bienvenues ! Veuillez soumettre une pull request ou ouvrir une issue pour proposer des améliorations ou signaler des problèmes.
