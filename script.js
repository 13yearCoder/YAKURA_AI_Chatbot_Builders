document.getElementById("askBtn").addEventListener("click", async function () {
    const question = document.getElementById("question").value;
    const answerBox = document.getElementById("answer");
    answerBox.innerText = "Thinking... 🤔";
    const response = await fetch("http://127.0.0.1:5000/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            question: question
        })
    });
    const data = await response.json();
    answerBox.innerText = data.answer;
});