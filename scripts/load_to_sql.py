import pandas as pd
from sqlalchemy import create_engine

# Charger le CSV
df = pd.read_csv("data/ventes.csv", parse_dates=["Date"])

# Créer la colonne CA
df["CA"] = df["Quantité"] * df["Prix_Unitaire"]

# Connexion à SQLite (fichier ventes.db)
engine = create_engine("sqlite:///data/ventes.db", echo=False)

# Charger dans la table 'ventes'
df.to_sql("ventes", con=engine, if_exists="replace", index=False)

print("✅ Données chargées dans data/ventes.db (table 'ventes')")
