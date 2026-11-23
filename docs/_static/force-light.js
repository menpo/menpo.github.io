// The GitBook site was light only: default to light unless the visitor chose a theme.
(function () {
  if (!localStorage.getItem("theme") || localStorage.getItem("theme") === "auto") {
    if (!sessionStorage.getItem("menpo-theme-seen")) {
      localStorage.setItem("theme", "light");
      sessionStorage.setItem("menpo-theme-seen", "1");
    }
  }
  document.documentElement.dataset.theme = localStorage.getItem("theme") || "light";
  window.addEventListener("DOMContentLoaded", function () {
    document.body.dataset.theme = localStorage.getItem("theme") || "light";
  });
})();
