import streamlit as st
import random
from instagrapi import Client

# --- CONFIGURATION PAGE ---
st.set_page_config(page_title="Giveaway Picker", page_icon="🏆")

# Masquer les menus Streamlit pour faire propre
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stButton>button { width: 100%; background-color: #00C853; color: white; border: none; font-size: 18px; padding: 12px; }
        .stButton>button:hover { background-color: #009624; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("🏆 Instagram Giveaway")

# --- INTERFACE ---
url = st.text_input("🔗 Lien du Post Instagram")
c1, c2 = st.columns(2)
min_mentions = c1.number_input("Mentions minimum", min_value=0, value=1)
n_winners = c2.number_input("Nombre de gagnants", min_value=1, value=1)

if st.button("Lancer le tirage"):
    if not url:
        st.warning("Il faut coller un lien d'abord !")
    else:
        # Barre de chargement simple
        progress = st.progress(0)
        status = st.empty()
        
        try:
            status.text("⏳ Analyse en cours...")
            
            # --- PARTIE INVISIBLE ---
            cl = Client()
            # Connexion silencieuse avec vos identifiants
            cl.login("ay.sabbarr", "HvL8$kPhpW9vp6N") 
            progress.progress(30)
            
            # Récupération du post
            media_pk = cl.media_pk_from_url(url)
            comments = cl.media_comments(media_pk)
            progress.progress(60)
            
            # --- FILTRAGE ---
            valid_entries = []
            for comment in comments:
                if str(comment.text).count('@') >= min_mentions:
                    valid_entries.append(comment)
            
            progress.progress(100)
            status.empty() # On efface le texte de chargement
            progress.empty() # On efface la barre

            # --- RESULTAT ---
            if not valid_entries:
                st.error("Aucun commentaire valide trouvé.")
            elif len(valid_entries) < n_winners:
                st.warning(f"Seulement {len(valid_entries)} participants. Pas assez pour {n_winners} gagnants.")
            else:
                winners = random.sample(valid_entries, n_winners)
                st.balloons()
                st.success("🎉 GAGNANT(S) :")
                
                for w in winners:
                    st.info(f"👤 **@{w.user.username}**\n\n💬 {w.text}")

        except Exception as e:
            st.error(f"Erreur : {e}")
