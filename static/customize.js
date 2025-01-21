document.addEventListener("DOMContentLoaded", function () {
    const groups = ["mode-group", "category-group", "option-group"];

    // Function to highlight selected button
    function highlightSelection(groupId) {
        const group = document.getElementById(groupId);
        const buttons = group.querySelectorAll(".quiz-button");

        buttons.forEach((button) => {
            const input = button.querySelector("input");
            input.addEventListener("change", () => {
                // Remove 'selected' class from all buttons in the group
                buttons.forEach((btn) => btn.classList.remove("selected"));
                // Add 'selected' class to the currently chosen button
                if (input.checked) {
                    button.classList.add("selected");
                }
            });
        });
    }

    // Attach the highlightSelection function to each group
    groups.forEach((group) => highlightSelection(group));
});
