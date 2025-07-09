from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import json

app = Flask(__name__)

# Charger les données pharmacie
with open("pharmacies.json", "r") as f:
    pharmacies = json.load(f)
    
@app.route("/", methods=["GET"])
def home():
    return "🚀 Bot WhatsApp Pharmacie est en ligne !"

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    response = MessagingResponse()
    msg = response.message()

    # Exemple : Si l'utilisateur parle de "CNSS"
    if "cnss" in incoming_msg:
        result = [
            p['nom'] for p in pharmacies
            if "CNSS" in p['assurances_acceptees']
        ]
        if result:
            msg.body("Pharmacies qui acceptent CNSS :\n" + "\n".join(result[:5]))
        else:
            msg.body("Aucune pharmacie trouvée avec CNSS.")
    else:
        msg.body("Bonjour 👋 ! Envoyez un message comme :\n- pharmacie CNSS\n- doliprane à agoè")

    return str(response)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)