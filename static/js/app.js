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
    const cards = document.querySelectorAll(".glassCard, .heroCard");
    cards.forEach(card => {
      card.style.transition = "transform 0.2s ease";
      card.addEventListener("mouseenter", () => {
        card.style.transform = "translateY(-4px)";
      });
      card.addEventListener("mouseleave", () => {
        card.style.transform = "translateY(0)";
      });
    });
  }

  /* ----------------------------------
     3. Button click feedback
     ---------------------------------- */
  const buttons = document.querySelectorAll("button");
  buttons.forEach(btn => {
    btn.addEventListener("mousedown", () => {
      btn.style.transform = "scale(0.97)";
    });
    btn.addEventListener("mouseup", () => {
      btn.style.transform = "scale(1)";
    });
    btn.addEventListener("mouseleave", () => {
      btn.style.transform = "scale(1)";
    });
  });

  /* ----------------------------------
     4. Input focus highlight
     ---------------------------------- */
  const inputs = document.querySelectorAll("input, select, textarea");
  inputs.forEach(input => {
    input.addEventListener("focus", () => {
      input.style.boxShadow = "0 0 0 2px rgba(37,99,235,0.25)";
    });
    input.addEventListener("blur", () => {
      input.style.boxShadow = "none";
    });
  });

});
