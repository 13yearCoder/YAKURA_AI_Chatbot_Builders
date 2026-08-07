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
    data = request.get_json()
    question = data.get("question")

    print("Question received:", question)

    answer = ask_question(question)

    return jsonify({
        "answer": answer
    })

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)