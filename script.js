document.getElementById("askBtn").addEventListener("click", async function () {

    const question = document.getElementById("question").value;
    const answerBox = document.getElementById("answer");

    if (question.trim() === "") {
        answerBox.innerText = "Please enter a question.";
        return;
    }

    answerBox.innerText = "Thinking... 🤔";

    try {

const response = await fetch("https://yakura-school-ai.onrender.com/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        if (!response.ok) {
            throw new Error("Server returned an error: " + response.status);
        }

        const data = await response.json();

        answerBox.innerText = data.answer;

    } catch (error) {

        console.error("Chatbot error:", error);

        answerBox.innerText =
            "❌ Could not connect to the AI server. Please make sure Flask is running.";

    }

});