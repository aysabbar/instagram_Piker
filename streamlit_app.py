import streamlit as st
import random
import time
from instagrapi import Client

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Giveaway Picker", page_icon="🏆")

# Custom CSS to mimic the clean look in your screenshots
st.markdown("""
<style>
    .step-container { background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center; }
    .success-text { color: green; font-weight: bold; }
    .stButton>button { width: 100%; background-color: #00C853; color: white; border: none; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (LOGIN) ---
with st.sidebar:
    st.header("🔐 Connexion Instagram")
    st.info("Un compte est nécessaire pour lire les commentaires.")
    username = st.text_input("Utilisateur")
    password = st.text_input("Mot de passe", type="password")
    login_btn = st.button("Se connecter")

    if login_btn and username and password:
        try:
            cl = Client()
            cl.login(username, password)
            st.session_state['client'] = cl
            st.success("Connecté !")
        except Exception as e:
            st.error(f"Erreur: {e}")

# --- MAIN INTERFACE ---
st.title("🏆 Instagram Giveaway Tool")

# VISUAL STEPS (Non-functional, just for UI matching)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("✅ **1. Numériser**")
with col2:
    st.markdown("✅ **2. Filtrer**")
with col3:
    st.markdown("Waiting... **3. Gagnant**")

st.divider()

# INPUTS
st.subheader("Définir la condition du concours")

url = st.text_input("🔗 Lien du Post / Reel Instagram", placeholder="https://www.instagram.com/reel/...")

col_config1, col_config2 = st.columns(2)
with col_config1:
    min_mentions = st.number_input("Nombre de mentions minimales", min_value=0, value=1, step=1)
with col_config2:
    n_winners = st.number_input("Nombre de gagnants", min_value=1, value=1, step=1)

# ACTION
if st.button("Trouver des gagnants"):
    if 'client' not in st.session_state:
        st.error("Veuillez d'abord vous connecter dans la barre latérale.")
    elif not url:
        st.warning("Veuillez coller un lien.")
    else:
        cl = st.session_state['client']
        
        with st.status("Analyse du concours en cours...", expanded=True) as status:
            try:
                # 1. Get Media ID
                st.write("🔍 Recherche du post...")
                media_pk = cl.media_pk_from_url(url)
                time.sleep(1)
                
                # 2. Get Comments
                st.write("📥 Téléchargement des commentaires...")
                comments = cl.media_comments(media_pk)
                st.write(f"✅ {len(comments)} commentaires trouvés.")
                
                # 3. Filter
                st.write("⚙️ Filtrage par mentions...")
                valid_entries = []
                for comment in comments:
                    # Count mentions (words starting with @)
                    mentions_count = str(comment.text).count('@')
                    if mentions_count >= min_mentions:
                        valid_entries.append(comment)
                
                st.write(f"🎯 {len(valid_entries)} participants qualifiés.")
                status.update(label="Terminé !", state="complete", expanded=False)

                # 4. Pick Winner
                if len(valid_entries) < n_winners:
                    st.error("Pas assez de participants qualifiés pour le nombre de gagnants demandé.")
                else:
                    winners = random.sample(valid_entries, n_winners)
                    
                    st.divider()
                    st.balloons()
                    st.subheader("🎉 Félicitations aux gagnants !")
                    
                    for w in winners:
                        st.success(f"@{w.user.username}")
                        st.caption(f"Commentaire : {w.text}")
                        # Optional: Show profile pic if available
                        # st.image(w.user.profile_pic_url, width=100)

            except Exception as e:
                st.error(f"Une erreur est survenue : {e}")
