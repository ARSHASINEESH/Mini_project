setTimeout(() => {
    const flashes = document.querySelectorAll(".flash");
    flashes.forEach((flash) => {
        flash.style.transition = "opacity 0.5s ease";
        flash.style.opacity = "0";
        setTimeout(() => flash.remove(), 500);
    });
}, 4000);