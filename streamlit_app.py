<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Instagram Giveaway Winner</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #f4f4f4; display: flex; flex-direction: column; align-items: center; padding-top: 50px; }
        .card { background: white; width: 600px; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); text-align: center; }
        h1 { color: #333; margin-bottom: 30px; }
        
        /* Les étapes visuelles */
        .steps { display: flex; justify-content: space-between; margin-bottom: 40px; color: #aaa; font-size: 14px; }
        .step { display: flex; flex-direction: column; align-items: center; gap: 5px; }
        .step.active { color: #00C853; font-weight: bold; }
        .circle { width: 30px; height: 30px; border: 2px solid #ddd; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 5px; }
        .active .circle { border-color: #00C853; background: #e8f5e9; color: #00C853; }

        /* Inputs */
        input { width: 90%; padding: 15px; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 20px; font-size: 16px; background: #fafafa; }
        .options { display: flex; gap: 10px; justify-content: center; margin-bottom: 20px; }
        .small-input { width: 60px; text-align: center; }

        /* Bouton */
        button { background-color: #00C853; color: white; border: none; padding: 15px 40px; font-size: 18px; border-radius: 30px; cursor: pointer; transition: 0.3s; font-weight: bold; box-shadow: 0 4px 10px rgba(0,200,83,0.3); }
        button:hover { transform: scale(1.05); background-color: #009624; }
        
        /* Loading */
        #loading { display: none; margin-top: 20px; }
        .progress-bar { width: 100%; height: 8px; background: #eee; border-radius: 4px; overflow: hidden; margin-top: 10px; }
        .progress-fill { height: 100%; background: #00C853; width: 0%; transition: width 0.3s; }
        .status-text { color: #666; font-size: 14px; margin-top: 10px; font-style: italic; }

        /* Résultat */
        #result { display: none; margin-top: 30px; animation: popIn 0.5s ease; border-top: 2px dashed #eee; padding-top: 20px; }
        .winner-box { background: #f0fdf4; border: 1px solid #bbf7d0; padding: 20px; border-radius: 10px; }
        .avatar { width: 80px; height: 80px; background: #ddd; border-radius: 50%; margin: 0 auto 15px; background-size: cover; border: 3px solid #00C853; }
        .username { font-size: 24px; font-weight: bold; color: #333; margin-bottom: 10px; }
        .comment { font-size: 16px; color: #555; font-style: italic; }

        @keyframes popIn { from { transform: scale(0.8); opacity: 0; } to { transform: scale(1); opacity: 1; } }
    </style>
</head>
<body>

<div class="card">
    <h1>🏆 Instagram Giveaway Tool</h1>

    <div class="steps">
        <div class="step active" id="step1"><div class="circle">1</div>Numériser</div>
        <div class="step" id="step2"><div class="circle">2</div>Filtrer</div>
        <div class="step" id="step3"><div class="circle">3</div>Gagnant</div>
    </div>

    <div id="inputSection">
        <input type="text" placeholder="Collez le lien du post Instagram ici..." value="https://www.instagram.com/p/Cyl7..." >
        
        <div class="options">
            <div>Mentions min: <input type="number" class="small-input" value="1"></div>
            <div>Gagnants: <input type="number" class="small-input" value="1"></div>
        </div>

        <button onclick="startFakeProcess()">Trouver le gagnant</button>
    </div>

    <div id="loading">
        <div class="progress-bar"><div class="progress-fill" id="fill"></div></div>
        <div class="status-text" id="status">Connexion à Instagram...</div>
    </div>

    <div id="result">
        <h3>🎉 FÉLICITATIONS !</h3>
        <div class="winner-box">
            <img src="https://cdn-icons-png.flaticon.com/512/149/149071.png" class="avatar" id="winnerPic">
            <div class="username" id="winnerName">@gagnant</div>
            <div class="comment">" <span id="winnerComment">Super concours !</span> "</div>
        </div>
    </div>
</div>

<script>
    // ==========================================
    // 🛑  🛑
    // C'est ici que tu décides qui gagne avant même de lancer !
    // ==========================================
    
    const LE_GAGNANT = "amine10sa"; 
    const LE_COMMENTAIRE = "J'adore le concept, je participe fort ! 🔥 @ami...";
    
    // ==========================================

    function startFakeProcess() {
        // Masquer les inputs
        document.getElementById('inputSection').style.display = 'none';
        document.getElementById('loading').style.display = 'block';

        const fill = document.getElementById('fill');
        const status = document.getElementById('status');
        const step2 = document.getElementById('step2');
        const step3 = document.getElementById('step3');

        // Scénario d'animation (Fake)
        let progress = 0;
        
        // Séquence d'animation
        const interval = setInterval(() => {
            progress += Math.floor(Math.random() * 5) + 2; // Avance un peu au hasard
            if (progress > 100) progress = 100;
            fill.style.width = progress + "%";

            // Changer les textes pour faire "vrai"
            if (progress > 20 && progress < 50) {
                status.innerText = "Récupération des commentaires (342 trouvés)...";
            } else if (progress > 50 && progress < 80) {
                status.innerText = "Filtrage des mentions et doublons...";
                step2.classList.add('active');
            } else if (progress > 90) {
                status.innerText = "Sélection aléatoire du gagnant...";
            }

            if (progress === 100) {
                clearInterval(interval);
                setTimeout(showWinner, 800);
            }
        }, 100); // Vitesse de la barre
    }

    function showWinner() {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('step3').classList.add('active');
        
        // Injecter les fausses données
        document.getElementById('winnerName').innerText = "@" + LE_GAGNANT;
        document.getElementById('winnerComment').innerText = LE_COMMENTAIRE;
        
        document.getElementById('result').style.display = 'block';
        
        // Confettis simples (Emoji)
        createConfetti();
    }

    function createConfetti() {
        // Juste un petit effet visuel
        document.body.style.overflow = "hidden"; 
    }
</script>

</body>
</html>
