document.getElementById("kd-menu-btn")?.addEventListener("click", function () {
  document.getElementById("kd-mobile-nav")?.classList.toggle("hidden");
});
(function () {
  document.querySelectorAll(".kd-rail").forEach(function (rail) {
    var track = rail.querySelector(".kd-rail-track");
    var prev = rail.querySelector(".kd-rail-prev");
    var next = rail.querySelector(".kd-rail-next");
    var more = rail.querySelector(".kd-rail-more");
    if (!track || !prev || !next) return;
    function maxScroll() {
      return track.scrollWidth - track.clientWidth;
    }
    function moreExtraWidth() {
      if (!more || more.classList.contains("hidden")) return 0;
      var gap = parseFloat(getComputedStyle(track).columnGap || getComputedStyle(track).gap) || 0;
      return more.offsetWidth + gap;
    }
    function update() {
      var productsOverflow = maxScroll() - moreExtraWidth() > 4;
      if (more) more.classList.toggle("hidden", !productsOverflow);
      var max = maxScroll();
      var overflow = max > 4;
      var sl = track.scrollLeft;
      var atLeft;
      var atRight;
      if (getComputedStyle(track).direction === "rtl") {
        if (sl <= 0) {
          atRight = sl >= -2;
          atLeft = sl <= -max + 2;
        } else {
          atLeft = sl <= 2;
          atRight = sl >= max - 2;
        }
      } else {
        atLeft = sl <= 2;
        atRight = sl >= max - 2;
      }
      prev.classList.toggle("invisible", !overflow || atLeft);
      prev.classList.toggle("pointer-events-none", !overflow || atLeft);
      next.classList.toggle("invisible", !overflow || atRight);
      next.classList.toggle("pointer-events-none", !overflow || atRight);
    }
    function step() {
      return Math.max(track.clientWidth * 0.8, 260);
    }
    prev.addEventListener("click", function (e) {
      e.preventDefault();
      track.scrollBy({ left: -step(), behavior: "smooth" });
    });
    next.addEventListener("click", function (e) {
      e.preventDefault();
      track.scrollBy({ left: step(), behavior: "smooth" });
    });
    track.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    if (window.ResizeObserver) new ResizeObserver(update).observe(track);
    var dragging = false;
    var dragged = false;
    var startX = 0;
    var startScroll = 0;
    var pointerId = null;
    function endDrag(e) {
      if (!dragging) return;
      if (e && pointerId != null && e.pointerId !== pointerId) return;
      dragging = false;
      pointerId = null;
      track.classList.remove("cursor-grabbing");
      track.classList.add("cursor-grab");
    }
    track.addEventListener("pointerdown", function (e) {
      if (e.pointerType === "touch") return;
      if (e.button !== 0) return;
      pointerId = e.pointerId;
      dragging = true;
      dragged = false;
      startX = e.clientX;
      startScroll = track.scrollLeft;
    });
    window.addEventListener("pointermove", function (e) {
      if (!dragging || e.pointerId !== pointerId) return;
      var dx = e.clientX - startX;
      if (!dragged) {
        if (Math.abs(dx) < 8) return;
        dragged = true;
        track.classList.add("cursor-grabbing");
        track.classList.remove("cursor-grab");
        try { track.setPointerCapture(e.pointerId); } catch (err) {}
      }
      e.preventDefault();
      track.scrollLeft = startScroll - dx;
    }, { passive: false });
    window.addEventListener("pointerup", endDrag);
    window.addEventListener("pointercancel", endDrag);
    track.addEventListener("dragstart", function (e) {
      e.preventDefault();
    }, true);
    track.addEventListener("click", function (e) {
      if (!dragged) return;
      e.preventDefault();
      e.stopPropagation();
      dragged = false;
    }, true);
    update();
  });
})();
