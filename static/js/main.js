// slide bar active

document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.querySelector(".menu-toggle");
    const sidebarMenu = document.querySelector(".sidebar-menu");
    const closeBtn = document.querySelector(".close-btn");

    menuToggle.addEventListener("click", function () {
        sidebarMenu.classList.add("active");
    });

    closeBtn.addEventListener("click", function () {
        sidebarMenu.classList.remove("active");
    });
});
