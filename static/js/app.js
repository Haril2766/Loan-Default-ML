document.addEventListener("DOMContentLoaded", () => {
  const alert = document.querySelector(".alert-danger");
  if (alert) {
    alert.scrollIntoView({ behavior: "smooth", block: "center" });
  }
});
