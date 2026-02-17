import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURATION & STYLE (Vintage Moderne)
st.set_page_config(page_title="Tachainville Parcelles", page_icon="🚜", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@400;700&display=swap');
    .stApp { background-color: #FDFBF7; }
    h1 { font-family: 'Playfair Display', serif; color: #354F52; }
    .stButton>button { 
        background-color: #354F52; color: white; border-radius: 10px; 
        height: 3em; width: 100%; font-weight: bold;
    }
    .main-card {
        background-color: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 1px solid #E0E0E0;
    }
    </style>
    """, unsafe_allow_html=True)

# EN-TÊTE
st.title("🚜 Carnet de Parcelles")
st.markdown("*Suivi des interventions — Campagne 24-25*")
st.divider()

# 2. BASE DE DONNÉES (On définit vos parcelles et cultures pour les menus)
# Vous pourrez modifier ces listes facilement
parcelles_dict = {
    "Mare a...": 9.0,
    "La Plaine": 12.5,
    "Les Terres Rouges": 5.2,
    "Le Clos": 3.8
}
cultures_liste = ["Blé", "Colza", "Féverole", "Orge", "Maïs"]
interventions_liste = ["Actisol", "Semis", "Pulvé", "Fertilisation", "Récolte"]

# 3. FORMULAIRE DE SAISIE
with st.container():
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        parcelle_sel = st.selectbox("📍 Sélectionner la parcelle", options=list(parcelles_dict.keys()))
        culture_sel = st.selectbox("🌱 Culture", options=cultures_liste)
    with col2:
        date_int = st.date_input("📅 Date de l'opération", datetime.now())
        surface = parcelles_dict[parcelle_sel]
        st.info(f"Surface : {surface} ha")

    st.divider()
    
    col3, col4 = st.columns(2)
    with col3:
        type_int = st.selectbox("🔧 Intervention", options=interventions_liste)
        produit = st.text_input("📦 Produit utilisé", placeholder="ex: Gallup ST, Semence...")
    with col4:
        dose_ha = st.number_input("🧪 Dose / ha", min_value=0.0, step=0.1, format="%.3f")
        cout_ha = st.number_input("💶 Coût / ha (€)", min_value=0.0, step=0.01)

    # CALCUL AUTOMATIQUE
    quantite_totale = dose_ha * surface
    
    st.markdown(f"""
        <div style="background-color: #F1F3F2; padding: 15px; border-radius: 10px; margin: 10px 0;">
            <p style="margin:0; color: #354F52; font-size: 0.9rem;">Quantité totale pour la parcelle :</p>
            <h2 style="margin:0; color: #2F3E46;">{quantite_totale:.2f} <span style="font-size: 1rem;">unités</span></h2>
        </div>
    """, unsafe_allow_html=True)

    if st.button("💾 Enregistrer l'intervention"):
        # Ici on crée la ligne prête pour l'Excel
        nouvelle_ligne = {
            "Année": 2025,
            "Parcelle": parcelle_sel,
            "Culture": culture_sel,
            "Surface": surface,
            "Date": date_int.strftime("%d/%m/%Y"),
            "Intervention": type_int,
            "Produit": produit,
            "Quantité/ha": dose_ha,
            "Quantité Totale": quantite_totale,
            "Coût/ha": cout_ha
        }
        st.success(f"Intervention sur '{parcelle_sel}' enregistrée avec succès !")
        st.balloons()
        # Optionnel : Afficher un aperçu de la ligne
        st.table(pd.DataFrame([nouvelle_ligne]))

    st.markdown("</div>", unsafe_allow_html=True)

# 4. HISTORIQUE RAPIDE
st.divider()
st.subheader("📋 Dernières saisies")
st.info("Une fois connecté à Google Sheets, vos données s'afficheront ici en temps réel.")
