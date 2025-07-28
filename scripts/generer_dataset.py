import pandas as pd
import random
from datetime import datetime, timedelta
import os

# --- Paramètres ---
nb_lignes = 1000
produits = [
    ("Laptop HP", "Informatique", 300000),
    ("Smartphone Samsung", "Téléphonie", 250000),
    ("Clavier Logitech", "Accessoires", 15000),
    ("Chaussures Nike", "Mode", 45000),
    ("Casque JBL", "Accessoires", 20000),
    ("T-shirt Zara", "Mode", 10000),
    ("Sac à dos Puma", "Mode", 25000),
    ("TV LG 42\"", "Électronique", 350000),
    ("Montre Casio", "Accessoires", 18000)
]
paiements = ["Carte bancaire", "Cash", "Mobile Money"]
clients = [f"C{str(i).zfill(4)}" for i in range(1, 101)]  # 100 clients

# --- Génération des ventes ---
ventes = []
date_debut = datetime(2024, 1, 1)
for _ in range(nb_lignes):
    produit, categorie, prix = random.choice(produits)
    date_vente = date_debut + timedelta(days=random.randint(0, 365))
    quantite = random.randint(1, 5)
    client = random.choice(clients)
    paiement = random.choice(paiements)

    ventes.append([date_vente, produit, categorie, client, quantite, prix, paiement])

# --- Sauvegarde ---
df = pd.DataFrame(ventes, columns=[
    "Date", "Produit", "Catégorie", "Client_ID", "Quantité", "Prix_Unitaire", "Moyen_Paiement"
])

os.makedirs("data", exist_ok=True)
df.to_csv("data/ventes.csv", index=False, encoding="utf-8")
print("✅ Fichier data/ventes.csv généré avec succès !")
