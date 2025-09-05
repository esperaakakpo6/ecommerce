import pandas as pd

def nettoyage_products():
    """ Nettoyage des données de products.csv """
    
    df  = pd.read_csv(r"D:\DAH\Data engeneer\seance 4\data_extract\magasin\products\products.csv")
    df = df.drop_duplicates()
    df["date"] = pd.to_datetime(df["date"])
    df["product_id"]  = df["product_id"].astype(str)
    df["stock"] = df["stock"].astype(int)
    return df

def colums_annee_mois_magasin():
    """ ajoute une colonne annee mois"""
    df = nettoyage_products()
    df["annee_mois"] = df["date"].dt.to_period("M")
    return df

def stock_products(date):
    """ Uniquement les csv qui contiennent les produits en stock """
    
    df = colums_annee_mois_magasin()
    stock_total = df[df['date'] == date]["stock"].sum()
    stock_df = pd.DataFrame({
        'date': [date],
        'stock_total': [stock_total]})
    
    output_file = rf"D:\DAH\Data engeneer\seance 4\data_transform\magasin\stock\stock_total_{date}.csv"
    stock_df.to_csv(output_file, index=False)
    print(f"Stock total magasin pour la date {date} sauvegardé dans 'stock_total.csv'")
    

def client_magasin(date):
    """Cette fonction calcule le client total journalière pour les clients_{date}.csv"""
    
    df = pd.read_csv(rf"D:\DAH\Data engeneer\seance 4\data_extract\magasin\clients\clients_{date}.csv")
    client_total = df.shape[0]
    client_total_df = pd.DataFrame({
        'date': [date],
        'client_total': [client_total]})
    
    output_file = rf"D:\DAH\Data engeneer\seance 4\data_transform\magasin\clients\client_total_{date}.csv"
    client_total_df.to_csv(output_file, index=False)
    print(f"Client total magasin de {date} sauvegardé dans 'client_total.csv'")
    


def price_total():
    df = colums_annee_mois_magasin()
    df_price = pd.read_csv(r"D:\DAH\Data engeneer\seance 4\data_transform\e-commerce\unit_price\unit_price.csv")
    
    # petite nettoyage
    df_price["product_id"] = df_price["product_id"].astype(str)
    df_price["unit_price"] = df_price["unit_price"].astype(float)
    
    # Fusionner les DataFrames sur la colonne id (inner join pour garder les id communs)
    merged_df = pd.merge(
        df[["product_id", "stock"]],
        df_price[["product_id", "unit_price"]],
        on="product_id",
        how='inner'
    )
    
    df["price"] = merged_df["stock"] * merged_df["unit_price"]
    return df

def ca_magasin(annee_mois):
    df = price_total()
    ca = df[df["annee_mois"] == annee_mois]["price"].sum()
    ca_df = pd.DataFrame({
        'annee_mois': [annee_mois],
        'ca': [ca]})
    
    output_file = rf"D:\DAH\Data engeneer\seance 4\data_transform\magasin\CA\ca_{annee_mois}.csv"
    ca_df.to_csv(output_file, index=False)
    print(f"chiffre d' affaire magasin pour le mois {annee_mois} sauvegardé dans 'ca.csv'")