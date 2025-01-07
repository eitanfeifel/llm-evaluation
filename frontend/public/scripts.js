const form = document.getElementById("promptForm");
const responseContainer = document.querySelector(".swiper-wrapper");
const chatWindow = document.querySelector(".chat-window");

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const task = document.getElementById("task").value;
    const prompt = document.getElementById("prompt").value;
    const submitButton = form.querySelector("button");

    const formData = { task, prompt }

    // Show loading state
    submitButton.disabled = true;
    submitButton.textContent = "Sending...";
    responseContainer.innerHTML = `
        <div class="swiper-slide">
            <div class="response-item">
                <div class="response-content">Processing your request...</div>
            </div>
        </div>
    `;


    try {
        const response = await fetch("/prompt", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify( formData ),
        });

        const data = await response.json();
        const { responses, evaluations, best_model, best_score } = data;

        // Clear and populate responses
        responseContainer.innerHTML = "";
        Object.entries(evaluations).forEach(([model, evaluation]) => {
            const slide = document.createElement("div");
            slide.className = "swiper-slide";
            slide.innerHTML = `
                <div class="response-item">
                    <div class="model-name">${model}</div>
                    <div class="response-content">${responses[model]}</div>
                    <div class="evaluation">
                        <strong>Evaluation:</strong>
                        <ul>
                            ${Object.entries(evaluation)
                                .map(
                                    ([criterion, detail]) => `
                                    <li>
                                        <strong>${criterion.charAt(0).toUpperCase() + criterion.slice(1)}:</strong> ${detail.score}/10 - ${detail.reasoning}
                                    </li>
                                `
                                )
                                .join("")}
                        </ul>
                    </div>
                </div>
            `;
            responseContainer.appendChild(slide);
        });

        // Reinitialize Swiper
        new Swiper(".swiper-container", {
            navigation: {
                nextEl: ".swiper-button-next",
                prevEl: ".swiper-button-prev",
            },
            slidesPerView: 1,
            spaceBetween: 16,
        });

        // Clear any previous best result
        const existingBestResult = document.querySelector(".best-result");
        if (existingBestResult) {
            existingBestResult.remove();
        }

        // Display best result below carousel
        const bestResult = document.createElement("div");
        bestResult.className = "response-item best-result";
        bestResult.innerHTML = `
            <div class="model-name">Best Model: ${best_model}</div>
            <div class="response-content">Score: ${best_score}/10</div>
        `;
        chatWindow.appendChild(bestResult);
    } catch (error) {
        console.error("Error fetching or processing response:", error);
        responseContainer.innerHTML = `
            <div class="swiper-slide">
                <div class="error-message">
                    Error: Unable to fetch responses.
                </div>
            </div>
        `;
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = "Send";
    }
});
