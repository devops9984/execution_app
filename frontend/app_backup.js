const API_URL = "https://execution-app.onrender.com";


// =========================================================
// PAGE LOAD
// =========================================================

document.addEventListener("DOMContentLoaded", () => {

    loadDashboard();
    loadNextExecutions();
    loadPositiveExecutions();
    loadPatterns();
    loadGrowthExecutions();

});


// =========================================================
// SHOW / HIDE FORM
// =========================================================

function showForm(formId) {

    const form = document.getElementById(formId);

    form.classList.toggle("hidden");

}


// =========================================================
// DASHBOARD
// =========================================================

async function loadDashboard() {

    try {

        const response = await fetch(`${API_URL}/dashboard`);

        const data = await response.json();

        document.getElementById("positive-count").textContent =
            data.positive_executions;

        document.getElementById("pattern-count").textContent =
            data.patterns;

        document.getElementById("growth-count").textContent =
            data.growth_executions;

        document.getElementById("pending-count").textContent =
            data.pending_next_executions;

        document.getElementById("completed-count").textContent =
            data.completed_executions;

    } catch (error) {

        console.error("Dashboard error:", error);

    }

}


// =========================================================
// POSITIVE EXECUTIONS
// =========================================================

async function loadPositiveExecutions() {

    try {

        const response =
            await fetch(`${API_URL}/positive-executions`);

        const executions = await response.json();

        const container =
            document.getElementById("positive-list");

        container.innerHTML = "";

        if (executions.length === 0) {

            container.innerHTML =
                "<p>No positive executions yet.</p>";

            return;
        }


        executions.forEach(execution => {

            const card = document.createElement("div");

            card.className =
                "execution-card positive-card";

            card.innerHTML = `

                <h3>${escapeHTML(execution.title)}</h3>

                <p>
                    <strong>What I did:</strong>
                    ${escapeHTML(execution.what_i_did)}
                </p>

                <p>
                    <strong>Old pattern defeated:</strong>
                    ${escapeHTML(execution.old_pattern_defeated || "-")}
                </p>

                <p>
                    <strong>What worked:</strong>
                    ${escapeHTML(execution.what_worked || "-")}
                </p>

                <small>
                    ${execution.created_at}
                </small>

            `;

            container.appendChild(card);

        });

    } catch (error) {

        console.error(
            "Positive execution error:",
            error
        );

    }

}


// =========================================================
// CREATE POSITIVE EXECUTION
// =========================================================

async function createPositiveExecution() {

    const title =
        document.getElementById("positive-title").value;

    const whatIDid =
        document.getElementById("positive-what").value;

    const oldPattern =
        document.getElementById("positive-pattern").value;

    const whatWorked =
        document.getElementById("positive-worked").value;


    if (!title || !whatIDid) {

        alert("Title and What I Did are required.");

        return;

    }


    try {

        const response = await fetch(
            `${API_URL}/positive-executions`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    title: title,

                    what_i_did: whatIDid,

                    old_pattern_defeated: oldPattern,

                    what_worked: whatWorked

                })

            }
        );


        if (!response.ok) {

            throw new Error(
                "Failed to create positive execution"
            );

        }


        alert("Positive execution saved!");

        document.getElementById(
            "positive-title"
        ).value = "";

        document.getElementById(
            "positive-what"
        ).value = "";

        document.getElementById(
            "positive-pattern"
        ).value = "";

        document.getElementById(
            "positive-worked"
        ).value = "";


        document.getElementById(
            "positive-form"
        ).classList.add("hidden");


        loadPositiveExecutions();

        loadDashboard();

    } catch (error) {

        console.error(error);

        alert("Could not save positive execution.");

    }

}


// =========================================================
// PATTERNS
// =========================================================

async function loadPatterns() {

    try {

        const response =
            await fetch(`${API_URL}/patterns`);

        const patterns = await response.json();

        const container =
            document.getElementById("pattern-list");

        container.innerHTML = "";


        if (patterns.length === 0) {

            container.innerHTML =
                "<p>No patterns recorded yet.</p>";

            return;

        }


        patterns.forEach(pattern => {

            const card =
                document.createElement("div");

            card.className =
                "execution-card pattern-card";

            card.innerHTML = `

                <h3>
                    Old Pattern
                </h3>

                <p>
                    <strong>
                        ${escapeHTML(pattern.old_pattern)}
                    </strong>
                </p>

                <div class="counter-thought">

                    <strong>
                        Counter Thought
                    </strong>

                    <p>
                        ${escapeHTML(pattern.counter_thought)}
                    </p>

                </div>

                <p>
                    <strong>My Response:</strong>
                    ${escapeHTML(pattern.my_response || "-")}
                </p>

                <p>
                    <strong>Next Execution:</strong>
                    ${escapeHTML(pattern.next_execution || "-")}
                </p>

                <small>
                    ${pattern.created_at}
                </small>

            `;

            container.appendChild(card);

        });

    } catch (error) {

        console.error(
            "Pattern error:",
            error
        );

    }

}


// =========================================================
// CREATE PATTERN
// =========================================================

async function createPattern() {

    const oldPattern =
        document.getElementById("pattern-old").value;

    const counterThought =
        document.getElementById("pattern-counter").value;

    const response =
        document.getElementById("pattern-response").value;

    const nextExecution =
        document.getElementById("pattern-next").value;


    if (!oldPattern || !counterThought) {

        alert(
            "Old pattern and counter thought are required."
        );

        return;

    }


    try {

        const result = await fetch(
            `${API_URL}/patterns`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    old_pattern: oldPattern,

                    counter_thought: counterThought,

                    my_response: response,

                    next_execution: nextExecution

                })

            }
        );


        if (!result.ok) {

            throw new Error(
                "Failed to create pattern"
            );

        }


        alert("Pattern saved!");


        document.getElementById(
            "pattern-old"
        ).value = "";

        document.getElementById(
            "pattern-counter"
        ).value = "";

        document.getElementById(
            "pattern-response"
        ).value = "";

        document.getElementById(
            "pattern-next"
        ).value = "";


        document.getElementById(
            "pattern-form"
        ).classList.add("hidden");


        loadPatterns();

        loadDashboard();

    } catch (error) {

        console.error(error);

        alert("Could not save pattern.");

    }

}


// =========================================================
// GROWTH EXECUTIONS
// =========================================================

async function loadGrowthExecutions() {

    try {

        const response =
            await fetch(`${API_URL}/growth-executions`);

        const executions = await response.json();

        const container =
            document.getElementById("growth-list");

        container.innerHTML = "";


        if (executions.length === 0) {

            container.innerHTML =
                "<p>No growth executions yet.</p>";

            return;

        }


        executions.forEach(execution => {

            const card =
                document.createElement("div");

            card.className =
                "execution-card growth-card";

            card.innerHTML = `

                <h3>
                    ${escapeHTML(execution.title)}
                </h3>

                <p>
                    <strong>Why:</strong>
                    ${escapeHTML(
                        execution.why_i_want_to_try || "-"
                    )}
                </p>

                <p>
                    <strong>Action:</strong>
                    ${escapeHTML(execution.action)}
                </p>

                <p>
                    <strong>Experience:</strong>
                    ${escapeHTML(
                        execution.experience || "-"
                    )}
                </p>

                <p>
                    <strong>What I learned:</strong>
                    ${escapeHTML(
                        execution.what_i_learned || "-"
                    )}
                </p>

                <p>
                    <strong>Would repeat:</strong>
                    ${
                        execution.would_repeat
                            ? "Yes"
                            : "No"
                    }
                </p>

                <p>
                    <strong>Next growth execution:</strong>
                    ${escapeHTML(
                        execution.next_growth_execution || "-"
                    )}
                </p>

                <small>
                    ${execution.created_at}
                </small>

            `;

            container.appendChild(card);

        });

    } catch (error) {

        console.error(
            "Growth execution error:",
            error
        );

    }

}


// =========================================================
// CREATE GROWTH EXECUTION
// =========================================================

async function createGrowthExecution() {

    const title =
        document.getElementById("growth-title").value;

    const why =
        document.getElementById("growth-why").value;

    const action =
        document.getElementById("growth-action").value;

    const experience =
        document.getElementById("growth-experience").value;

    const learned =
        document.getElementById("growth-learned").value;

    const repeat =
        document.getElementById("growth-repeat").checked;

    const nextGrowth =
        document.getElementById("growth-next").value;


    if (!title || !action) {

        alert(
            "Title and action are required."
        );

        return;

    }


    try {

        const response = await fetch(
            `${API_URL}/growth-executions`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    title: title,

                    why_i_want_to_try: why,

                    action: action,

                    experience: experience,

                    what_i_learned: learned,

                    would_repeat: repeat,

                    next_growth_execution: nextGrowth

                })

            }
        );


        if (!response.ok) {

            throw new Error(
                "Failed to create growth execution"
            );

        }


        alert("Growth execution saved!");


        document.getElementById(
            "growth-title"
        ).value = "";

        document.getElementById(
            "growth-why"
        ).value = "";

        document.getElementById(
            "growth-action"
        ).value = "";

        document.getElementById(
            "growth-experience"
        ).value = "";

        document.getElementById(
            "growth-learned"
        ).value = "";

        document.getElementById(
            "growth-repeat"
        ).checked = false;

        document.getElementById(
            "growth-next"
        ).value = "";


        document.getElementById(
            "growth-form"
        ).classList.add("hidden");


        loadGrowthExecutions();

        loadDashboard();

    } catch (error) {

        console.error(error);

        alert(
            "Could not save growth execution."
        );

    }

}


// =========================================================
// NEXT EXECUTIONS
// =========================================================

async function loadNextExecutions() {

    try {

        const response =
            await fetch(`${API_URL}/next-executions/pending`);

        const executions = await response.json();

        const container =
            document.getElementById(
                "next-execution-container"
            );

        container.innerHTML = "";


        if (executions.length === 0) {

            container.innerHTML = `
                <div class="execution-card next-card">

                    <h3>
                        No pending execution
                    </h3>

                    <p>
                        Create your next action.
                    </p>

                </div>
            `;

            return;

        }


        const execution = executions[0];


        const card =
            document.createElement("div");

        card.className =
            "execution-card next-card";


        card.innerHTML = `

            <h3>
                ${escapeHTML(execution.action)}
            </h3>

            <p>
                <strong>Type:</strong>
                ${escapeHTML(execution.execution_type)}
            </p>

            <p>
                <strong>Reason:</strong>
                ${escapeHTML(execution.reason || "-")}
            </p>

            <button
                class="complete-button"
                onclick="completeExecution(${execution.id})"
            >
                ✓ Complete Execution
            </button>

        `;


        container.appendChild(card);

    } catch (error) {

        console.error(
            "Next execution error:",
            error
        );

    }

}


// =========================================================
// COMPLETE EXECUTION
// =========================================================

async function completeExecution(id) {

    try {

        const response = await fetch(
            `${API_URL}/next-executions/${id}/complete`,
            {
                method: "PUT"
            }
        );


        if (!response.ok) {

            throw new Error(
                "Failed to complete execution"
            );

        }


        alert("Execution completed!");


        loadNextExecutions();

        loadDashboard();

    } catch (error) {

        console.error(error);

        alert(
            "Could not complete execution."
        );

    }

}


// =========================================================
// SECURITY HELPER
// =========================================================

function escapeHTML(value) {

    if (value === null || value === undefined) {

        return "";

    }


    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");

}