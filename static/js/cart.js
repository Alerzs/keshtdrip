(function () {
  document.querySelectorAll("[data-kd-qty-form]").forEach(function (form) {
    var select = form.querySelector("[data-kd-qty-select]");
    var custom = form.querySelector("[data-kd-qty-custom]");
    if (!select || !custom) return;
    select.addEventListener("change", function () {
      if (select.value === "custom") {
        select.removeAttribute("name");
        custom.disabled = false;
        custom.classList.remove("hidden");
        custom.focus();
        custom.select();
        return;
      }
      custom.disabled = true;
      form.submit();
    });
    custom.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        form.submit();
      }
    });
    custom.addEventListener("blur", function () {
      if (!custom.disabled && custom.value) form.submit();
    });
  });
})();
