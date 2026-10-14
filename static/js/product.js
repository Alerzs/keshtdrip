(function () {
  var variantNode = document.getElementById("kd-variants");
  var pressureSelect = document.getElementById("kd-pressure");
  var diameterSelect = document.getElementById("kd-diameter");
  var priceNode = document.getElementById("kd-price");
  var noteNode = document.getElementById("kd-variant-note");
  var skuNode = document.getElementById("kd-sku");
  var slugInput = document.getElementById("kd-variant-slug");
  if (variantNode && priceNode) {
    var variants = JSON.parse(variantNode.textContent);

    function fa(text) {
      return String(text).replace(/\d/g, function (digit) {
        return "۰۱۲۳۴۵۶۷۸۹"[digit];
      });
    }
    function faPrice(value) {
      return fa(String(value).replace(/\B(?=(\d{3})+(?!\d))/g, "٬"));
    }
    function specLabel(variant) {
      var parts = [];
      if (variant.diameter) parts.push("قطر " + fa(variant.diameter));
      if (variant.working_pressure) parts.push("فشار کاری " + fa(variant.working_pressure));
      return parts.join("، ");
    }
    function allowedDiameters(pressure) {
      var values = [];
      variants.forEach(function (variant) {
        if (pressureSelect && variant.working_pressure !== pressure) return;
        if (variant.diameter && values.indexOf(variant.diameter) === -1) values.push(variant.diameter);
      });
      return values;
    }
    function currentVariant() {
      var pressure = pressureSelect ? pressureSelect.value : "";
      var diameter = diameterSelect ? diameterSelect.value : "";
      return variants.find(function (variant) {
        if (pressureSelect && variant.working_pressure !== pressure) return false;
        if (diameterSelect && variant.diameter !== diameter) return false;
        return true;
      });
    }
    function syncDiameters() {
      if (!diameterSelect) return;
      var allowed = allowedDiameters(pressureSelect ? pressureSelect.value : "");
      var first = "";
      var currentOk = false;
      Array.prototype.forEach.call(diameterSelect.options, function (option) {
        var ok = allowed.indexOf(option.value) !== -1;
        option.disabled = !ok;
        option.hidden = !ok;
        if (ok && !first) first = option.value;
        if (ok && option.value === diameterSelect.value) currentOk = true;
      });
      if (!currentOk && first) diameterSelect.value = first;
    }
    function renderPrice() {
      var variant = currentVariant();
      if (!variant) return;
      priceNode.textContent = faPrice(variant.price);
      if (noteNode) noteNode.textContent = specLabel(variant);
      if (skuNode && variant.slug) skuNode.textContent = variant.slug;
      if (slugInput && variant.slug) slugInput.value = variant.slug;
      if (window.history && window.history.replaceState) {
        var url = new URL(window.location.href);
        url.searchParams.set("variant", String(variant.id));
        window.history.replaceState({}, "", url);
      }
    }
    pressureSelect?.addEventListener("change", function () {
      syncDiameters();
      renderPrice();
    });
    diameterSelect?.addEventListener("change", renderPrice);
    syncDiameters();
    renderPrice();
  }

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
    var max = Number(input.max || 99);
    var value = Number(input.value || min);
    if (Number.isNaN(value)) value = min;
    input.value = Math.min(max, Math.max(min, value));
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
