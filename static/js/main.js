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



// drop down animation in home page

const collapsibles = document.querySelectorAll(".collapsible");

        collapsibles.forEach(button => {
            button.addEventListener("click", function() {
                this.classList.toggle("active");
                const content = this.nextElementSibling;

                // Toggle max-height
                if (content.style.maxHeight) {
                    content.style.maxHeight = null;
                } else {
                    content.style.maxHeight = content.scrollHeight + "px";
                }
            });
        });