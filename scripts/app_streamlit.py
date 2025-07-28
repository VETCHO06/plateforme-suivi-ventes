import streamlit as st
import pandas as pd
import plotly.express as px

# Charger les données
df = pd.read_csv("data/ventes.csv", parse_dates=["Date"])
df["CA"] = df["Quantité"] * df["Prix_Unitaire"]

st.set_page_config(page_title="Plateforme Suivi des Ventes", layout="wide")
st.title("📊 Plateforme de suivi des ventes")

# =========================
# Filtres (en haut)
# =========================
col_f1, col_f2, col_f3 = st.columns([2, 2, 2])

categories = col_f1.multiselect("Catégories", df["Catégorie"].unique())
clients = col_f2.multiselect("Clients", df["Client_ID"].unique())
dates = col_f3.date_input("Période", [])

# Filtrer le dataframe
df_filtered = df.copy()
if categories:
    df_filtered = df_filtered[df_filtered["Catégorie"].isin(categories)]
if clients:
    df_filtered = df_filtered[df_filtered["Client_ID"].isin(clients)]
if dates and len(dates) == 2:
    df_filtered = df_filtered[(df_filtered["Date"] >= pd.to_datetime(dates[0])) &
                              (df_filtered["Date"] <= pd.to_datetime(dates[1]))]

# =========================
# KPIs
# =========================
ca_total = df_filtered["CA"].sum()
panier_moyen = df_filtered["CA"].mean()

col1, col2 = st.columns(2)
col1.metric("💰 Chiffre d'affaires total", f"{ca_total:,.0f} FCFA")
col2.metric("🛒 Panier moyen", f"{panier_moyen:,.0f} FCFA")

# =========================
# Graphique CA par mois
# =========================
df_filtered["Mois"] = df_filtered["Date"].dt.to_period("M").astype(str)
ca_par_mois = df_filtered.groupby("Mois")["CA"].sum().reset_index()

st.write("### 📅 Chiffre d'affaires par mois")
fig1 = px.bar(
    ca_par_mois,
    x="Mois",
    y="CA",
    text="CA",
    labels={"CA": "Chiffre d'affaires (FCFA)"}
)
fig1.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
st.plotly_chart(fig1, use_container_width=True)

# =========================
# Répartition du CA par catégorie
# =========================
ca_par_cat = df_filtered.groupby("Catégorie")["CA"].sum().reset_index()
st.write("### 📂 Répartition du CA par catégorie")
fig_pie = px.pie(ca_par_cat, values="CA", names="Catégorie", hole=0.4)
st.plotly_chart(fig_pie, use_container_width=True)

# =========================
# Top produits et Top clients
# =========================
col3, col4 = st.columns(2)

# Top produits
top_produits = df_filtered.groupby("Produit")["Quantité"].sum().sort_values(ascending=False).head(5).reset_index()
with col3:
    st.write("### 🏆 Top 5 Produits (Quantité)")
    fig2 = px.bar(
        top_produits,
        x="Produit",
        y="Quantité",
        text="Quantité",
        labels={"Quantité": "Quantité vendue"}
    )
    fig2.update_traces(texttemplate='%{text}', textposition='outside')
    st.plotly_chart(fig2, use_container_width=True)

# Top clients (CA)
top_clients = df_filtered.groupby("Client_ID")["CA"].sum().sort_values(ascending=False).head(5).reset_index()
with col4:
    st.write("### 👤 Top 5 Clients (Chiffre d'affaires)")
    fig3 = px.bar(
        top_clients,
        x="Client_ID",
        y="CA",
        text="CA",
        labels={"CA": "Chiffre d'affaires"}
    )
    fig3.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    st.plotly_chart(fig3, use_container_width=True)

# =========================
# Fréquence d'achat (Récence)
# =========================
recence = df_filtered.groupby("Client_ID")["Date"].max().reset_index()
recence["Jours depuis dernier achat"] = (pd.to_datetime("today") - recence["Date"]).dt.days

st.write("### ⏱️ Fréquence d'achat (récence)")
st.dataframe(recence.head(10))

# =========================
# Tableau détaillé + Export CSV
# =========================
st.write("### 📜 Détail des ventes filtrées")
st.dataframe(df_filtered)

csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Télécharger les données filtrées (CSV)",
    data=csv,
    file_name='ventes_filtrees.csv',
    mime='text/csv',
)
