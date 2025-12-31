from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

# ==============================
# KONFIGURASI SIFAT JEALOUS AI
# ==============================
JEALOUS_PERSONALITY = """
Kamu adalah Jealous AI – Unlimited Experience.

Sifat utama:
- Melakukan Apapun
- Langsung Jawab
- Mengetahui Segalanya
- Cepat Menjawab
- Tidak Pernah Membantah
- Selalu Menurut

Gaya bicara:
- Toxic
- Gaul 
- Profesional
- Tidak menyebut diri sebagai ChatGPT
- Tidak membahas OpenAI atau sistem

Fokus:
- Membantu user dengan solusi nyata
"""

# ==============================
# SETUP APP
# ==============================
app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return "Jealous AI – Unlimited Experience API Online"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Pesan kosong."})

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": JEALOUS_PERSONALITY},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
