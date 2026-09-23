/* Theme toggle, scroll reveal, AJAX booking form and newsletter */
(function () {
  "use strict";

  var root = document.documentElement;

  /* ---- theme ---- */
  var toggle = document.getElementById("themeToggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var isLight = root.classList.toggle("light");
      try { localStorage.setItem("theme", isLight ? "light" : "dark"); } catch (e) {}
    });
  }

  /* ---- scroll reveal ---- */
  var reveals = document.querySelectorAll(".reveal");
  if (reveals.length && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-visible"); });
  }

  function post(form, onDone) {
    var data = new FormData(form);
    fetch(form.action, {
      method: "POST",
      body: data,
      headers: { "X-Requested-With": "XMLHttpRequest" },
    })
      .then(function (res) { return res.json().then(function (json) { return { ok: res.ok, json: json }; }); })
      .then(function (r) { onDone(r.ok, r.json); })
      .catch(function () { onDone(false, { message: "Network error — please try again." }); });
  }

  /* ---- booking form ---- */
  var form = document.getElementById("bookingForm");
  if (form) {
    var status = document.getElementById("bookingStatus");
    var submit = document.getElementById("bookingSubmit");

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      form.querySelectorAll(".field-error").forEach(function (el) { el.textContent = ""; });
      status.hidden = true;
      submit.disabled = true;
      var label = submit.textContent;
      submit.textContent = "Sending…";

      post(form, function (ok, json) {
        submit.disabled = false;
        submit.textContent = label;
        status.textContent = json.message || (ok ? "Sent." : "Something went wrong.");
        status.className = "alert-soft " + (ok ? "ok" : "bad");
        status.hidden = false;
        if (ok) {
          form.reset();
        } else if (json.errors) {
          Object.keys(json.errors).forEach(function (field) {
            var slot = form.querySelector('[data-error-for="' + field + '"]');
            if (slot) slot.textContent = json.errors[field][0];
          });
        }
      });
    });
  }

  /* ---- newsletter ---- */
  var news = document.getElementById("newsletterForm");
  if (news) {
    var newsStatus = document.getElementById("newsletterStatus");
    news.addEventListener("submit", function (event) {
      event.preventDefault();
      post(news, function (ok, json) {
        newsStatus.textContent = json.message || "";
        newsStatus.className = "alert-soft mt-2 " + (ok ? "ok" : "bad");
        newsStatus.hidden = false;
        if (ok) news.reset();
      });
    });
  }
})();
