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
