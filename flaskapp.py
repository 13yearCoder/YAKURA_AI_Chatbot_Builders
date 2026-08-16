from flask import Flask, request, jsonify
from flask_cors import CORS
from schoolragengine import ask_question

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "YAKURA AI School Server is running!"


@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()

        question = data.get("question")

        print("Question received:", question)

        if not question:
            return jsonify({
                "answer": "Please enter a question."
            }), 400

        answer = ask_question(question)

        print("Answer generated:", answer)

        return jsonify({
            "answer": answer
        })

    except Exception as e:
        print("ERROR:", e)

        return jsonify({
            "answer": "Sorry, something went wrong on the AI server."
        }), 500

import os

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True,
        use_reloader=False
    )