/* ── ComplaintIQ Client-Side Logic ──────────────────────────────────── */

document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("complaintInput");
    const classifyBtn = document.getElementById("classifyBtn");
    const clearBtn = document.getElementById("clearBtn");
    const charCount = document.getElementById("charCount");
    const resultsSection = document.getElementById("resultsSection");
    const errorSection = document.getElementById("errorSection");
    const errorText = document.getElementById("errorText");

    // ── Character Count ─────────────────────────────────────────────
    input.addEventListener("input", () => {
        const len = input.value.length;
        charCount.textContent = `${len} character${len !== 1 ? "s" : ""}`;
    });

    // ── Clear ───────────────────────────────────────────────────────
    clearBtn.addEventListener("click", () => {
        input.value = "";
        charCount.textContent = "0 characters";
        resultsSection.style.display = "none";
        errorSection.style.display = "none";
        input.focus();
    });

    // ── Classify ────────────────────────────────────────────────────
    classifyBtn.addEventListener("click", () => classify());
    input.addEventListener("keydown", (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === "Enter") classify();
    });

    async function classify() {
        const text = input.value.trim();
        if (!text) {
            showError("Please enter a complaint to classify.");
            return;
        }
        if (text.length < 10) {
            showError("Complaint is too short. Please provide at least 10 characters.");
            return;
        }

        // Loading state
        classifyBtn.classList.add("loading");
        classifyBtn.disabled = true;
        errorSection.style.display = "none";
        resultsSection.style.display = "none";

        try {
            const res = await fetch("/classify", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ complaint: text }),
            });

            const data = await res.json();

            if (!res.ok) {
                showError(data.error || "Something went wrong.");
                return;
            }

            renderResults(data);
        } catch (err) {
            showError("Network error. Is the server running?");
        } finally {
            classifyBtn.classList.remove("loading");
            classifyBtn.disabled = false;
        }
    }

    // ── Render Results ──────────────────────────────────────────────
    function renderResults(data) {
        // Category
        const categoryCard = document.getElementById("categoryCard");
        categoryCard.className = `result-card glass-card cat-${data.category}`;
        document.getElementById("categoryValue").textContent = data.category_label;
        const catConf = Math.round(data.category_confidence * 100);
        document.getElementById("categoryConfidence").style.width = catConf + "%";
        document.getElementById("categoryConfText").textContent = catConf + "% confidence";

        // Urgency
        const urgencyCard = document.getElementById("urgencyCard");
        urgencyCard.className = `result-card glass-card urgency-${data.urgency}`;
        document.getElementById("urgencyValue").textContent = data.urgency_label;
        const urgConf = Math.round(data.urgency_confidence * 100);
        document.getElementById("urgencyConfidence").style.width = urgConf + "%";
        document.getElementById("urgencyConfText").textContent = urgConf + "% confidence";

        // Routing
        document.getElementById("routingValue").textContent = data.routed_to;
        document.getElementById("routingBadge").textContent = `→ ${data.routed_to}`;

        // Overall confidence ring
        const pct = Math.round(data.confidence * 100);
        document.getElementById("confidencePct").textContent = pct + "%";
        const circle = document.getElementById("confCircle");
        const circumference = 2 * Math.PI * 52; // r=52
        const offset = circumference - (pct / 100) * circumference;
        // Reset animation
        circle.style.transition = "none";
        circle.style.strokeDashoffset = circumference;
        requestAnimationFrame(() => {
            circle.style.transition = "stroke-dashoffset 1s cubic-bezier(0.16, 1, 0.3, 1)";
            circle.style.strokeDashoffset = offset;
        });

        // Show results
        resultsSection.style.display = "block";
        errorSection.style.display = "none";

        // Scroll to results
        resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    // ── Show Error ──────────────────────────────────────────────────
    function showError(message) {
        errorText.textContent = message;
        errorSection.style.display = "block";
        resultsSection.style.display = "none";
    }
});
