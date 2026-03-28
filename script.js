const chatBox = document.getElementById("chatBox");
const userInput = document.getElementById("userInput");
const chatWidget = document.getElementById("chatWidget");
const quickReplies = document.getElementById("quickReplies");

let faqData = [];

// Load FAQ data
fetch("faq_js_data.json")
    .then(res => res.json())
    .then(data => { faqData = data; })
    .catch(() => { faqData = []; });

// ------------------------------
// LOAD PREVIOUS CHAT
// ------------------------------
window.onload = () => {
    chatBox.innerHTML = `
        <div class="message bot">
            Hello 👋 Welcome to Athenura Internship.
        </div>
        <div class="quick-suggestion">
            <button class="suggestion-btn" onclick="selectQuickReply('Internship Info')">Internship Info</button>
        </div>
    `;
};

// ------------------------------
// ENTER KEY SEND
// ------------------------------
userInput.addEventListener("keypress", function(e) {
    if (e.key === "Enter") sendMessage();
});

// ------------------------------
// OPEN / CLOSE CHAT
// ------------------------------
function toggleChat() {
    if (chatWidget.style.display === "none" || chatWidget.style.display === "") {
        chatWidget.style.display = "block";
    } else {
        chatWidget.style.display = "none";
    }
}

// ------------------------------
// QUICK REPLY SELECTION
// ------------------------------
function selectQuickReply(text) {
    userInput.value = text;
    sendMessage();
    if (quickReplies) quickReplies.style.display = "none";
}

// ------------------------------
// TEXT SIMILARITY (Jaccard)
// ------------------------------
function preprocess(text) {
    return text.toLowerCase().replace(/[^\w\s]/g, '').trim();
}

function similarity(a, b) {
    const wordsA = new Set(preprocess(a).split(/\s+/));
    const wordsB = new Set(preprocess(b).split(/\s+/));
    const intersection = [...wordsA].filter(w => wordsB.has(w)).length;
    const union = new Set([...wordsA, ...wordsB]).size;
    return union === 0 ? 0 : intersection / union;
}

function findBestMatch(userMsg) {
    let best = null;
    let bestScore = 0;
    for (const item of faqData) {
        const score = similarity(userMsg, item.q);
        if (score > bestScore) {
            bestScore = score;
            best = item;
        }
    }
    return bestScore > 0.15 ? best : null;
}

// ------------------------------
// SEND MESSAGE
// ------------------------------
function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage(message, "user");
    userInput.value = "";

    const typing = addMessage("Typing...", "bot");

    setTimeout(() => {
        typing.remove();
        if (faqData.length === 0) {
            addMessage("Sorry, FAQ data is still loading. Please try again.", "bot");
            return;
        }
        const match = findBestMatch(message);
        if (match) {
            addMessage(match.a, "bot");
        } else {
            addMessage("Sorry, I couldn't find a relevant answer. Please try rephrasing your question.", "bot");
        }
    }, 400);
}

// ------------------------------
// ADD MESSAGE
// ------------------------------
function addMessage(text, sender) {
    const msg = document.createElement("div");
    msg.classList.add("message", sender);
    msg.innerText = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
    return msg;
}
