document.addEventListener("DOMContentLoaded", () => {

  /* ----------------------------------
     1. Smooth scroll to error message
     ---------------------------------- */
  const alertBox = document.querySelector(".alert-danger");
  if (alertBox) {
    alertBox.scrollIntoView({
      behavior: "smooth",
      block: "center"
    });
  }

  /* ----------------------------------
     2. Card hover effect (desktop only)
     ---------------------------------- */
  if (window.innerWidth > 900) {
    document.querySelectorAll(".glassCard, .heroCard").forEach(card => {
      card.classList.add("hover-card");
    });
  }

  /* ----------------------------------
     3. Button click feedback (safe)
     ---------------------------------- */
  document.querySelectorAll("button").forEach(btn => {
    btn.addEventListener("mousedown", () => {
      btn.classList.add("btn-pressed");
    });
    btn.addEventListener("mouseup", () => {
      btn.classList.remove("btn-pressed");
    });
    btn.addEventListener("mouseleave", () => {
      btn.classList.remove("btn-pressed");
    });
  });

  /* ----------------------------------
     4. Input focus highlight (CSS driven)
     ---------------------------------- */
  document.querySelectorAll("input, select, textarea").forEach(el => {
    el.addEventListener("focus", () => {
      el.classList.add("input-focus");
    });
    el.addEventListener("blur", () => {
      el.classList.remove("input-focus");
    });
  });

});

/* ----------------------------------
   5. Mobile menu toggle
   ---------------------------------- */
function toggleMenu() {
  const menu = document.getElementById("mobileNav");
  if (menu) {
    menu.classList.toggle("open");
  }
}
