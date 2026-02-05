import streamlit as st
import random
from instagrapi import Client

# --- CONFIGURATION DU ROBOT ---
# Identifiants mis à jour
ROBOT_USER = "ay.sabbarr"
ROBOT_PASS = "HvL8$kPhpW9vp6N"

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Giveaway Picker", page_icon="🏆")

# CSS pour le look épuré
st.markdown("""
<style>
    .stButton>button { width: 100%; background-color: #00C853; color: white; border: none; font-size: 18px; padding: 10px; }
    .stButton>button:hover { background-color: #009624; color: white; }
    h1 { text-align: center; }
    .reportview-container { background: #f0f2f6; }
</style>
""", unsafe_allow_html=True)

# --- MAIN INTERFACE ---
st.title("🏆 Instagram Giveaway Tool")

# Indicateurs visuels
cols = st.columns(3)
cols[0].markdown("✅ **1. Numériser**")
cols[1].markdown("✅ **2. Filtrer**")
cols[2].markdown("⏳ **3. Gagnant**")
st.divider()

# INPUTS
st.subheader("Définir la condition du concours")
url = st.text_input("🔗 Lien du Post / Reel Instagram")

c1, c2 = st.columns(2)
min_mentions = c1.number_input("Mentions min.", min_value=0, value=1)
n_winners = c2.number_input("Gagnants", min_value=1, value=1)

# ACTION
if st.button("Trouver des gagnants"):
    if not url:
        st.warning("Veuillez coller un lien.")
    elif "instagram.com" not in url:
        st.error("Ce n'est pas un lien Instagram valide.")
    else:
        status_text = st.empty()
        status_bar = st.progress(0)
        
        try:
            # 1. CONNEXION AUTOMATIQUE
            status_text.write(f"🤖 Connexion au compte {ROBOT_USER}...")
            cl = Client()
            
            try:
                cl.login(ROBOT_USER, ROBOT_PASS)
            except Exception as e:
                st.error(f"Erreur de connexion : {e}")
                st.stop()
            
            status_bar.progress(30)
            
            # 2. RECUPERATION
            status_text.write("🔍 Analyse du post...")
            # Extraction de l'ID du média
            try:
                media_pk = cl.media_pk_from_url(url)
            except Exception as e:
                st.error("Impossible de trouver le post. Vérifiez que le lien est correct et que le post est public.")
                st.stop()
            
            status_text.write("📥 Téléchargement des commentaires...")
            comments = cl.media_comments(media_pk)
            status_bar.progress(60)
            
            # 3. FILTRAGE
            status_text.write("⚙️ Filtrage des participations...")
            valid_entries = []
            for comment in comments:
                # On compte les mentions (@)
                if str(comment.text).count('@') >= min_mentions:
                    valid_entries.append(comment)
            
            status_bar.progress(100)
            status_text.empty() # Nettoyer le texte de chargement

            # 4. RESULTAT
            if len(valid_entries) < n_winners:
                st.error(f"Seulement {len(valid_entries)} participants valides. Pas assez pour tirer {n_winners} gagnants.")
            else:
                winners = random.sample(valid_entries, n_winners)
                
                # Effet visuel
                st.balloons()
                st.success(f"🎉 {len(winners)} GAGNANT(S) SÉLECTIONNÉ(S) !")
                
                st.write("---")
                for i, w in enumerate(winners):
                    st.markdown(f"### 🏅 Gagnant #{i+1}")
                    st.info(f"👤 **Compte : @{w.user.username}**\n\n💬 **Commentaire :** {w.text}")

        except Exception as e:
            st.error(f"Une erreur technique est survenue : {e}")
