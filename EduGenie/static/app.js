const task = document.getElementById("task");
const inputText = document.getElementById("inputText");
const submitBtn = document.getElementById("submitBtn");
const result = document.getElementById("result");
const statusBox = document.getElementById("status");
const copyBtn = document.getElementById("copyBtn");

const placeholders = {
    qa: "Example: Which is the largest ocean?",
    explain: "Example: Explain photosynthesis in simple language.",
    quiz: "Paste a topic or passage. Example: Photosynthesis is the process...",
    summarize: "Paste a long educational passage here...",
    learn: "Example: SQL"
};

task.addEventListener("change", () => {
    inputText.placeholder = placeholders[task.value];
});

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function renderResult(data) {
    if (task.value !== "quiz" || !data.questions) {
        result.textContent = data;
        return;
    }

    result.innerHTML = data.questions.map((q, index) => {
        const options = q.options.map(
            option => `<div class="quiz-option">${escapeHtml(option)}</div>`
        ).join("");

        return `
            <div class="quiz-question">
                <strong>${index + 1}. ${escapeHtml(q.question)}</strong>
                ${options}
                <div class="quiz-answer">
                    Answer: ${escapeHtml(q.correct_answer)}
                </div>
                <div>${escapeHtml(q.explanation)}</div>
            </div>
        `;
    }).join("");
}

async function submitTask() {
    const value = inputText.value.trim();

    if (!value) {
        result.innerHTML = '<div class="error">Please enter some text first.</div>';
        return;
    }

    submitBtn.disabled = true;
    statusBox.hidden = false;
    statusBox.textContent = "EduGenie is thinking...";
    result.innerHTML = '<p class="muted">Generating your result...</p>';

    const endpoint = task.value === "learn"
        ? "/learn/recommendations"
        : `/${task.value}`;

    const fieldName = task.value === "qa" ? "question" : "text";
    const finalFieldName = task.value === "explain" || task.value === "learn"
        ? (task.value === "learn" ? "topic" : "topic")
        : fieldName;

    const form = new FormData();
    form.append(finalFieldName, value);

    try {
        const response = await fetch(endpoint, {
            method: "POST",
            body: form
        });

        const contentType = response.headers.get("content-type") || "";

let data;

if (contentType.includes("application/json")) {
    data = await response.json();
} else {
    const text = await response.text();
    throw new Error(
        `Server error (${response.status}): ${text.substring(0, 300)}`
    );
}

        if (!response.ok) {
            throw new Error(data.detail || "Request failed.");
        }

        renderResult(data.result);
        statusBox.textContent = "Done.";
    } catch (error) {
        result.innerHTML = `<div class="error">${escapeHtml(error.message)}</div>`;
        statusBox.textContent = "Something went wrong.";
    } finally {
        submitBtn.disabled = false;
    }
}

submitBtn.addEventListener("click", submitTask);

copyBtn.addEventListener("click", async () => {
    const text = result.innerText.trim();

    if (!text) {
        return;
    }

    try {
        await navigator.clipboard.writeText(text);
        copyBtn.textContent = "Copied!";
        setTimeout(() => copyBtn.textContent = "Copy", 1200);
    } catch {
        copyBtn.textContent = "Copy failed";
        setTimeout(() => copyBtn.textContent = "Copy", 1200);
    }
});
