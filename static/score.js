document.addEventListener("DOMContentLoaded", function () {
    const scoreElement = document.getElementById("score-percentage");
    const progressBarFill = document.querySelector(".progress-bar-fill");

    // Fetch score and total questions dynamically from data attributes
    const score = parseInt(scoreElement.dataset.score, 10); // Get the score from the HTML data attribute
    const totalQuestions = parseInt(scoreElement.dataset.total, 10); // Get the total number of questions from the data attribute

    // Calculate the percentage
    const percentage = (score / totalQuestions) * 100;

    // Update the progress bar and score display
    progressBarFill.style.width = percentage + "%";
    progressBarFill.textContent = percentage.toFixed(0) + "%";
    scoreElement.textContent = percentage.toFixed(0) + "%";

    // Apply custom color
    progressBarFill.style.backgroundColor = "#529EE0";
    scoreElement.style.color = "#529EE0";
});
