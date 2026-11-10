// S.E.T. Solar US: exit-intent signup for the free Solar Buyer's Course (added 2026-11-10).
// Desktop only (mouse leaves through the top of the window after 8s on the page). Shows at most once
// per visitor every 14 days, never after a signup, never on the course landing page or the store.
// Submissions go to the same FormSubmit inbox the hourly SET_Signup_Sync task reads into Brevo list 4.
(function () {
  'use strict';
  var KEY = 'set_exit_popup';
  var DAYS = 14;
  var path = location.pathname;
  if (/solar-buyers-guide|\/store\/|callback/.test(path)) return;
  if (!window.matchMedia || !window.matchMedia('(hover: hover) and (pointer: fine) and (min-width: 900px)').matches) return;

  function getState() { try { return JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { return {}; } }
  function setState(o) { try { localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) {} }
  var st = getState();
  if (st.subscribed) return;
  if (st.shown && (Date.now() - st.shown) < DAYS * 864e5) return;

  var armed = false, shown = false;
  setTimeout(function () { armed = true; }, 8000);

  function build() {
    var css = document.createElement('style');
    css.textContent =
      '.setx-ov{position:fixed;inset:0;background:rgba(15,23,42,.62);z-index:99999;display:flex;align-items:center;justify-content:center;padding:16px}' +
      '.setx-box{background:#fff;color:#1e1e2e;max-width:440px;width:100%;border-radius:16px;padding:28px 26px 22px;box-shadow:0 20px 60px rgba(0,0,0,.35);position:relative;font-family:Inter,system-ui,sans-serif}' +
      '.setx-box h2{font-size:22px;line-height:1.25;margin:0 0 8px;color:#0e2a47}' +
      '.setx-box p{font-size:15px;line-height:1.55;margin:0 0 16px;color:#475569}' +
      '.setx-box form{display:flex;flex-direction:column;gap:10px}' +
      '.setx-box input{padding:12px 14px;border:1.5px solid #cbd5e1;border-radius:8px;font-size:15px}' +
      '.setx-box button[type=submit]{background:#F5A623;color:#1e1e2e;border:0;border-radius:8px;padding:13px;font-weight:700;font-size:15px;cursor:pointer}' +
      '.setx-x{position:absolute;top:10px;right:12px;background:none;border:0;font-size:24px;line-height:1;color:#64748b;cursor:pointer}' +
      '.setx-note{font-size:12px!important;color:#94a3b8!important;margin:10px 0 0!important;text-align:center}';
    document.head.appendChild(css);

    var ov = document.createElement('div');
    ov.className = 'setx-ov';
    ov.innerHTML =
      '<div class="setx-box" role="dialog" aria-modal="true" aria-labelledby="setx-h">' +
      '<button type="button" class="setx-x" aria-label="Close">&times;</button>' +
      '<h2 id="setx-h">Before you go: get the free Solar Generator Buyer&rsquo;s Guide</h2>' +
      '<p>A free 12-page PDF with a sizing worksheet and printable Blackout Cheat Sheet, plus short plain-English follow-up emails.</p>' +
      '<form><input type="text" name="name" placeholder="First name" autocomplete="given-name" required>' +
      '<input type="email" name="email" placeholder="Email address" autocomplete="email" required>' +
      '<button type="submit">Send Me the Guide</button></form>' +
      '<p class="setx-note">No spam. Unsubscribe anytime.</p></div>';
    document.body.appendChild(ov);

    function close() { ov.remove(); document.removeEventListener('keydown', onKey); }
    function onKey(e) { if (e.key === 'Escape') close(); }
    ov.addEventListener('click', function (e) { if (e.target === ov) close(); });
    ov.querySelector('.setx-x').addEventListener('click', close);
    document.addEventListener('keydown', onKey);
    ov.querySelector('input').focus();

    ov.querySelector('form').addEventListener('submit', function (e) {
      e.preventDefault();
      var f = e.target, b = f.querySelector('button');
      b.textContent = 'Sending...'; b.disabled = true;
      fetch('https://formsubmit.co/ajax/biz@sunenergytechnology.net', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify({ name: f.name.value, email: f.email.value,
          _subject: 'S.E.T. Solar Guide Request (exit popup)', _template: 'table', _captcha: 'false', page: path })
      }).then(function (r) { return r.json(); }).then(function (d) {
        if (d.success) {
          setState({ shown: Date.now(), subscribed: true });
          b.textContent = "You're in! Check your inbox."; b.style.background = '#00C896'; b.style.color = '#fff';
          if (typeof window.gtag === 'function') window.gtag('event', 'generate_lead', { method: 'exit_popup' });
          setTimeout(close, 2200);
        } else { b.textContent = 'Try Again'; b.disabled = false; }
      }).catch(function () { b.textContent = 'Try Again'; b.disabled = false; });
    });
  }

  document.addEventListener('mouseout', function (e) {
    if (!armed || shown) return;
    if (e.relatedTarget || e.toElement) return;
    if (e.clientY > 8) return;
    shown = true;
    setState({ shown: Date.now() });
    build();
  });

  // Any other signup form on the page also suppresses the popup for this visitor.
  document.addEventListener('submit', function (e) {
    if (e.target && e.target.querySelector && e.target.querySelector('input[type=email]') && !e.target.closest('.setx-ov')) {
      setState({ shown: Date.now(), subscribed: true });
    }
  }, true);
})();
