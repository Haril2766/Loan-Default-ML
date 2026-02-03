document.addEventListener("DOMContentLoaded", () => {

  // Smooth scroll to error
  const alert = document.querySelector(".alert-danger");
  if (alert) {
    alert.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  // Soft hover lift for cards
  document.querySelectorAll(".glassCard, .heroCard").forEach(card => {
    card.addEventListener("mouseenter", () => {
      card.style.transform = "translateY(-4px)";
    });
    card.addEventListener("mouseleave", () => {
      card.style.transform = "translateY(0)";
    });
  });

  // Button press feedback
  document.querySelectorAll("button").forEach(btn => {
    btn.addEventListener("mousedown", () => btn.style.transform = "scale(0.97)");
    btn.addEventListener("mouseup", () => btn.style.transform = "scale(1)");
  });

});
