import pandas as pd

def nettoyage_ecommerce():
    """ Nettoyage des données de ecommerce.csv """
    
    df  = pd.read_csv(r"D:\DAH\Data engeneer\seance 4\data_extract\e-commerce\ecommerce_orders.csv")
    df = df.drop_duplicates()
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["product_id"]  = df["product_id"].astype(str)
    df["customer_id"]  = df["customer_id"].astype(str)
    df["order_id"] = df["order_id"].astype(str)
    df["quantity"] = df["quantity"].astype(int)
    df["price"] = df["price"].astype(float)
    return df

def colums_annee_mois_ecommerce():
    df = nettoyage_ecommerce()
    df["annee_mois"] = df["order_date"].dt.to_period("M")
    return df

def unit_price():
    df = colums_annee_mois_ecommerce()
    unit_price = round((df["price"] / df["quantity"]), 2)
    
    unit_price_df = pd.DataFrame({
        'product_id': df["product_id"],
        'unit_price': unit_price
    })
    
    unit_price_df.drop_duplicates(inplace=True)
    output_file = r"D:\DAH\Data engeneer\seance 4\data_transform\e-commerce\unit_price\unit_price.csv"
    unit_price_df.to_csv(output_file, index=False)
    print(f"Unit price sauvegardé dans 'unit_price.csv'")
    
def stock_ecommerce(date):
    """ Uniquement le csv de base de donnee ecommerce.
    La fonction calclue le stock totale payer par jour et sauvegarde le resultat dans un fichier csv.
    """
    df = colums_annee_mois_ecommerce()
    stock_total = df[df['order_date'] == date]["quantity"].sum()
    stock_df = pd.DataFrame({
        'date': [date],
        'stock_total': [stock_total]})
    
    output_file = rf"D:\DAH\Data engeneer\seance 4\data_transform\e-commerce\stock\stock_total_{date}.csv"
    stock_df.to_csv(output_file, index=False)
    print(f"Stock total ecommerce pour la date {date} sauvegardé dans 'stock_total.csv'")
    
def client_ecommerce(date):
    """Cette fonction calcule le client total journalière"""
    
    df = colums_annee_mois_ecommerce()
    client_total = df[df['order_date'] == date]["customer_id"].unique()
    client_total = len(client_total)
    client_total_df = pd.DataFrame({
        'date': [date],
        'stock_total': [client_total]})
    
    output_file = rf"D:\DAH\Data engeneer\seance 4\data_transform\e-commerce\clients\client_total_{date}.csv"
    client_total_df.to_csv(output_file, index=False)
    print(f"Client total ecommerce pour la date {date} sauvegardé dans 'client_total.csv'")


def ca_ecommerce(annee_mois):
    df = colums_annee_mois_ecommerce()
    ca = df[df["annee_mois"] == annee_mois]["price"].sum()
    ca_df = pd.DataFrame({
        'annee_mois': [annee_mois],
        'ca': [ca]})
    
    output_file = rf"D:\DAH\Data engeneer\seance 4\data_transform\e-commerce\CA\ca_{annee_mois}.csv"
    ca_df.to_csv(output_file, index=False)
    print(f"Chiffre d'affaire ecommerce pour {annee_mois} sauvegardé dans 'ca_{annee_mois}.csv'")