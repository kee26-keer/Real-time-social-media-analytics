// Wait until the DOM content is loaded
document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript loaded and ready!");

    // Example: Reload the page when clicking a refresh button
    const refreshButton = document.getElementById("refresh");
    if (refreshButton) {
        refreshButton.addEventListener("click", function () {
            location.reload();
        });
    }
});
