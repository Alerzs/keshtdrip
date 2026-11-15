(function () {
  var main = document.getElementById("kd-main-image");
  var frame = document.getElementById("kd-zoom");
  var thumbs = document.querySelectorAll("[data-kd-thumb]");

  function resetZoom() {
    if (!main) return;
    main.style.transform = "scale(1)";
    main.style.transformOrigin = "center center";
  }
  function zoomAt(e) {
    if (!main || !frame) return;
    var rect = frame.getBoundingClientRect();
    if (!rect.width || !rect.height) return;
    var x = ((e.clientX - rect.left) / rect.width) * 100;
    var y = ((e.clientY - rect.top) / rect.height) * 100;
    main.style.transformOrigin = x + "% " + y + "%";
    main.style.transform = "scale(2)";
  }
  if (frame && main) {
    frame.addEventListener("mousemove", zoomAt);
    frame.addEventListener("mouseenter", zoomAt);
    frame.addEventListener("mouseleave", resetZoom);
  }

  thumbs.forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (!main) return;
      resetZoom();
      main.src = btn.getAttribute("data-src");
      main.alt = btn.getAttribute("data-alt") || "";
      thumbs.forEach(function (item) {
        item.classList.remove("border-cyanbtn", "ring-2", "ring-cyanbtn/20");
        item.classList.add("border-slate-200");
      });
      btn.classList.add("border-cyanbtn", "ring-2", "ring-cyanbtn/20");
      btn.classList.remove("border-slate-200");
    });
  });

  var input = document.getElementById("kd-qty-input");
  var minus = document.getElementById("kd-qty-minus");
  var plus = document.getElementById("kd-qty-plus");
  function clampQty() {
    if (!input) return;
    var min = Number(input.min || 1);
    var value = Number(input.value || min);
    if (Number.isNaN(value) || value < min) value = min;
    input.value = String(value);
  }
  minus?.addEventListener("click", function () {
    input.value = Number(input.value || 1) - 1;
    clampQty();
  });
  plus?.addEventListener("click", function () {
    input.value = Number(input.value || 1) + 1;
    clampQty();
  });
  input?.addEventListener("change", clampQty);

  var specs = document.getElementById("kd-specs");
  var moreBtn = document.getElementById("kd-specs-more");
  var lessBtn = document.getElementById("kd-specs-less");
  var fade = document.getElementById("kd-specs-fade");
  function setSpecsOpen(open) {
    if (!specs) return;
    specs.classList.toggle("max-h-44", !open);
    specs.classList.toggle("overflow-hidden", !open);
    fade?.classList.toggle("hidden", open);
    moreBtn?.classList.toggle("hidden", open);
    lessBtn?.classList.toggle("hidden", !open);
  }
  if (specs && specs.scrollHeight <= specs.clientHeight + 8) {
    setSpecsOpen(true);
    moreBtn?.classList.add("hidden");
    lessBtn?.classList.add("hidden");
  } else {
    moreBtn?.addEventListener("click", function () { setSpecsOpen(true); });
    lessBtn?.addEventListener("click", function () { setSpecsOpen(false); });
  }
})();
