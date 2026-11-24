
document.addEventListener("DOMContentLoaded", function () {

    // Refresh the dashboard every 10 seconds.
    const refreshInterval = 10000;

    setInterval(function () {
        if (document.visibilityState === "visible") {
            window.location.reload();
        }
    }, refreshInterval);

});
