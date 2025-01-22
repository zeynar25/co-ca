document.addEventListener("DOMContentLoaded", function () {
    const scoreElement = document.getElementById("score-percentage");
    const resultTitle = document.getElementById("result-title");
    const percentageText = document.getElementById("percentage-text");
    const circle = document.querySelector(".circle");

    // Fetch score and total questions dynamically from data attributes
    const score = parseInt(scoreElement.dataset.score, 10); // Get the score from the HTML data attribute
    const totalQuestions = parseInt(scoreElement.dataset.total, 10); // Get the total number of questions from the data attribute

    // Calculate the percentage
    const percentage = (score / totalQuestions) * 100;

    // Update the circle's background dynamically
    circle.style.background = `conic-gradient(#529EE0 ${percentage}%, #ddd ${percentage}%)`;

    // Update the percentage text in the center of the circle
    percentageText.textContent = `${percentage.toFixed(0)}%`;

    // Update the title with the score
    resultTitle.textContent = `Congrats! You got ${score}/${totalQuestions}`;
});