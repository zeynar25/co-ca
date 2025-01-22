let currentIndex = 0;
const items = document.querySelectorAll('.carousel-item');
const prevButton = document.getElementById('prevButton');
const nextButton = document.getElementById('nextButton');

// Initially display the first question
items[currentIndex].classList.add('active');

// Add event listeners for Prev and Next buttons
prevButton.addEventListener('click', () => {
    if (currentIndex > 0) {
        items[currentIndex].classList.remove('active');
        currentIndex--;
        items[currentIndex].classList.add('active');
    }
});

nextButton.addEventListener('click', () => {
    if (currentIndex < items.length - 1) {
        items[currentIndex].classList.remove('active');
        currentIndex++;
        items[currentIndex].classList.add('active');
    }
});


// Disables prevButton at the first card, and nextButton at the last card
document.addEventListener("DOMContentLoaded", function () {
    const items = document.querySelectorAll(".carousel-item");
    const prevButton = document.getElementById("prevButton");
    const nextButton = document.getElementById("nextButton");

    let currentIndex = 0;

    function updateButtons() {
        // Disable Prev button on the first card
        prevButton.disabled = currentIndex === 0;

        // Disable Next button on the last card
        nextButton.disabled = currentIndex === items.length - 1;
    }

    function showCard(index) {
        items.forEach((item, i) => {
            item.classList.toggle("active", i === index);
        });
        currentIndex = index;
        updateButtons();
    }

    // Event listeners for navigation
    prevButton.addEventListener("click", () => {
        if (currentIndex > 0) {
            showCard(currentIndex - 1);
        }
    });

    nextButton.addEventListener("click", () => {
        if (currentIndex < items.length - 1) {
            showCard(currentIndex + 1);
        }
    });

    // Initialize carousel
    showCard(currentIndex);
});


// adds/removes selected class to a button
document.addEventListener("DOMContentLoaded", () => {
    // Select all quiz buttons
    const quizButtons = document.querySelectorAll(".quiz-button");

    quizButtons.forEach(button => {
        // Add a click event listener to each button
        button.addEventListener("click", () => {
            // Find all radio inputs within this button group
            const parentGroup = button.parentElement;
            const buttonsInGroup = parentGroup.querySelectorAll(".quiz-button");

            // Remove "selected" class from all buttons in the group
            buttonsInGroup.forEach(b => b.classList.remove("selected"));

            // Add "selected" class to the clicked button
            button.classList.add("selected");
        });
    });
});