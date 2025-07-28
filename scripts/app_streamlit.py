import streamlit as st
import pandas as pd
import plotly.express as px

# Charger les données
df = pd.read_csv("data/ventes.csv", parse_dates=["Date"])
df["CA"] = df["Quantité"] * df["Prix_Unitaire"]

st.set_page_config(page_title="Plateforme Suivi des Ventes", layout="wide")

# CSS pour centrer le titre et un peu de style
st.markdown("""
    <style>
    .center-title {text-align: center; color: #2E86C1; font-size: 32px; font-weight: bold;}
    .stMetric {background-color: #F2F4F4; padding: 10px; border-radius: 8px;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='center-title'>📊 Plateforme de suivi des ventes</div>", unsafe_allow_html=True)
st.write("")
st.set_page_config(page_title="Plateforme Suivi des Ventes", layout="wide")

# 💡 ICI : On insère le style
st.markdown("""
    <style>
    /* Centrer le titre */
    .center-title {text-align: center; color: #2E86C1; font-size: 32px; font-weight: bold;}
    
    /* KPI Metrics : couleur de fond plus foncée et texte plus visible */
    div[data-testid="stMetric"] {
        background: #f1f3f6;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #d4d6da;
    }
    
    /* Chiffres des KPIs en gras et plus grands */
    div[data-testid="stMetric"] > label {
        color: #34495E;
        font-size: 18px;
    }
    div[data-testid="stMetric"] > div {
        color: #1B4F72;
        font-size: 22px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# Filtres (en haut)
# =========================
st.markdown("### 🔎 Filtres de recherche")
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

st.markdown("### 📈 Indicateurs clés")
col1, col2 = st.columns(2)
col1.metric("💰 Chiffre d'affaires total", f"{ca_total:,.0f} FCFA")
col2.metric("🛒 Panier moyen", f"{panier_moyen:,.0f} FCFA")

# =========================
# Graphique CA par mois
# =========================
st.markdown("### 📅 Chiffre d'affaires par mois")
df_filtered["Mois"] = df_filtered["Date"].dt.to_period("M").astype(str)
ca_par_mois = df_filtered.groupby("Mois")["CA"].sum().reset_index()

fig1 = px.bar(
    ca_par_mois,
    x="Mois",
    y="CA",
    text="CA",
    color="CA",
    color_continuous_scale="Blues",
    labels={"CA": "Chiffre d'affaires (FCFA)"}
)
fig1.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
st.plotly_chart(fig1, use_container_width=True)

# =========================
# Répartition du CA par catégorie
# =========================
st.markdown("### 📂 Répartition du CA par catégorie")
ca_par_cat = df_filtered.groupby("Catégorie")["CA"].sum().reset_index()
fig_pie = px.pie(ca_par_cat, values="CA", names="Catégorie", hole=0.4)
st.plotly_chart(fig_pie, use_container_width=True)

# =========================
# Top produits et Top clients
# =========================
col3, col4 = st.columns(2)

with col3:
    st.markdown("### 🏆 Top 5 Produits (Quantité)")
    top_produits = df_filtered.groupby("Produit")["Quantité"].sum().sort_values(ascending=False).head(5).reset_index()
    fig2 = px.bar(
        top_produits,
        x="Produit",
        y="Quantité",
        text="Quantité",
        color="Quantité",
        color_continuous_scale="Oranges"
    )
    fig2.update_traces(texttemplate='%{text}', textposition='outside')
    st.plotly_chart(fig2, use_container_width=True)

with col4:
    st.markdown("### 👤 Top 5 Clients (Chiffre d'affaires)")
    top_clients = df_filtered.groupby("Client_ID")["CA"].sum().sort_values(ascending=False).head(5).reset_index()
    fig3 = px.bar(
        top_clients,
        x="Client_ID",
        y="CA",
        text="CA",
        color="CA",
        color_continuous_scale="Greens"
    )
    fig3.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    st.plotly_chart(fig3, use_container_width=True)

# =========================
# Fréquence d'achat (Récence)
# =========================
st.markdown("### ⏱️ Fréquence d'achat (récence)")
recence = df_filtered.groupby("Client_ID")["Date"].max().reset_index()
recence["Jours depuis dernier achat"] = (pd.to_datetime("today") - recence["Date"]).dt.days
st.dataframe(recence.head(10))

# =========================
# Tableau détaillé + Export CSV
# =========================
st.markdown("### 📜 Détail des ventes filtrées")
st.dataframe(df_filtered)

csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Télécharger les données filtrées (CSV)",
    data=csv,
    file_name='ventes_filtrees.csv',
    mime='text/csv',
)
