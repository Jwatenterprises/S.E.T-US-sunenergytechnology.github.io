// S.E.T. Solar US — Centralized Tracking
// GA4 + Impact.com + Meta Pixel + TikTok Pixel + Custom Events

(function() {
  'use strict';

  var GA4_ID = 'G-W8W4W8LPNC';
  var IMPACT_PROGRAM_ID = 'P-A6782322-8a4f-4218-9a98-fb3e2a61a6961';
  var META_PIXEL_ID = '2023918628214957';
  var TIKTOK_PIXEL_ID = '7650989745631281169';

  // ── GA4 ──
  var gaScript = document.createElement('script');
  gaScript.async = true;
  gaScript.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA4_ID;
  document.head.appendChild(gaScript);

  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag('js', new Date());
  gtag('config', GA4_ID, {
    send_page_view: true,
    cookie_flags: 'SameSite=None;Secure'
  });

  // ── Impact.com ──
  (function(i, m, p, a, c, t) {
    c.ire_o = p;
    c[p] = c[p] || function() { (c[p].a = c[p].a || []).push(arguments); };
    t = a.createElement(m);
    var z = a.getElementsByTagName(m)[0];
    t.async = 1;
    t.src = i;
    z.parentNode.insertBefore(t, z);
  })('https://utt.impactcdn.com/' + IMPACT_PROGRAM_ID + '.js', 'script', 'impactStat', document, window);
  window.impactStat('transformLinks');
  window.impactStat('trackImpression');

  // ── Meta Pixel (activate by adding pixel ID above) ──
  if (META_PIXEL_ID) {
    !function(f, b, e, v, n, t, s) {
      if (f.fbq) return;
      n = f.fbq = function() { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      if (!f._fbq) f._fbq = n;
      n.push = n; n.loaded = true; n.version = '2.0';
      n.queue = [];
      t = b.createElement(e); t.async = true; t.src = v;
      s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
    }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', META_PIXEL_ID);
    fbq('track', 'PageView');
  }

  // ── TikTok Pixel (activate by adding pixel ID above) ──
  if (TIKTOK_PIXEL_ID) {
    !function(w, d, t) {
      w.TiktokAnalyticsObject = t;
      var ttq = w[t] = w[t] || [];
      ttq.methods = ["page","track","identify","instances","debug","on","off","once","ready","alias","group","trackPull","install","instance"];
      ttq.setAndDefer = function(t, e) { t[e] = function() { t.push([e].concat(Array.prototype.slice.call(arguments, 0))); }; };
      for (var i = 0; i < ttq.methods.length; i++) ttq.setAndDefer(ttq, ttq.methods[i]);
      ttq.instance = function(t) { for (var e = ttq._i[t] || [], n = 0; n < ttq.methods.length; n++) ttq.setAndDefer(e, ttq.methods[n]); return e; };
      ttq.load = function(e, n) {
        var o = "https://analytics.tiktok.com/i18n/pixel/events.js";
        ttq._i = ttq._i || {}; ttq._i[e] = []; ttq._i[e]._u = o;
        ttq._t = ttq._t || {}; ttq._t[e] = +new Date;
        ttq._o = ttq._o || {}; ttq._o[e] = n || {};
        var a = d.createElement("script"); a.type = "text/javascript"; a.async = true;
        a.src = o + "?sdkid=" + e + "&lib=" + t;
        var r = d.getElementsByTagName("script")[0]; r.parentNode.insertBefore(a, r);
      };
      ttq.load(TIKTOK_PIXEL_ID);
      ttq.page();
    }(window, document, 'ttq');
  }

  // ── UTM Capture ──
  var params = new URLSearchParams(window.location.search);
  var utmKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
  utmKeys.forEach(function(key) {
    var val = params.get(key);
    if (val) sessionStorage.setItem(key, val);
  });

  function getUtm() {
    var utm = {};
    utmKeys.forEach(function(key) {
      var val = sessionStorage.getItem(key);
      if (val) utm[key] = val;
    });
    return utm;
  }

  // ── Affiliate Partner Detection ──
  var PARTNER_DOMAINS = {
    'awin1.com': 'Awin',
    'amazon.com': 'Amazon Associates',
    'energysage.com': 'EnergySage',
    'modernize.com': 'Modernize',
    'sunrun.com': 'Sunrun',
    '4patriots.com': '4Patriots'
  };

  // Awin sub-brand detection from destination URL
  var AWIN_BRANDS = [
    ['bluetti', 'BLUETTI'],
    ['ecoflow', 'EcoFlow'],
    ['allpowers', 'ALLPOWERS'],
    ['natures-generator', "Nature's Generator"],
    ['naturesgenerator', "Nature's Generator"],
    ['litime', 'LiTime']
  ];

  function identifyPartner(href) {
    if (!href) return null;
    try {
      var url = new URL(href, window.location.origin);
      var host = url.hostname.replace('www.', '');
      for (var domain in PARTNER_DOMAINS) {
        if (host === domain || host.endsWith('.' + domain)) {
          return PARTNER_DOMAINS[domain];
        }
      }
    } catch (e) {}
    return null;
  }

  function identifyAwinBrand(href) {
    if (!href) return 'other';
    var lower = href.toLowerCase();
    for (var i = 0; i < AWIN_BRANDS.length; i++) {
      if (lower.indexOf(AWIN_BRANDS[i][0]) !== -1) return AWIN_BRANDS[i][1];
    }
    return 'other';
  }

  function getPageName() {
    var path = window.location.pathname;
    if (path === '/' || path === '/index.html') return 'homepage';
    return path.replace(/^\//, '').replace(/\.html$/, '').replace(/\//g, '_');
  }

  // ── Event Tracking ──
  function trackEvent(eventName, eventParams) {
    var utm = getUtm();
    var merged = Object.assign({}, eventParams || {}, utm, { page_location: getPageName() });

    if (window.gtag) gtag('event', eventName, merged);

    if (window.ttq && TIKTOK_PIXEL_ID) {
      if (eventName === 'affiliate_click') {
        ttq.track('ClickButton', { content_name: merged.partner || 'unknown' });
      }
    }

    if (window.fbq && META_PIXEL_ID) {
      if (eventName === 'affiliate_click') {
        fbq('trackCustom', 'AffiliateClick', { partner: merged.partner, brand: merged.brand || '' });
      } else if (eventName === 'lead_capture') {
        fbq('track', 'Lead');
      } else if (eventName === 'quiz_complete') {
        fbq('trackCustom', 'QuizComplete');
      }
    }
  }

  // ── Auto-attach Affiliate Click Tracking ──
  function attachAffiliateTracking() {
    var links = document.querySelectorAll('a[href]');
    links.forEach(function(link) {
      var partner = identifyPartner(link.href);
      if (partner) {
        link.addEventListener('click', function() {
          var data = {
            partner: partner,
            link_url: link.href,
            link_text: (link.textContent || '').trim().substring(0, 100)
          };
          if (partner === 'Awin') {
            data.brand = identifyAwinBrand(link.href);
          }
          trackEvent('affiliate_click', data);
        });
        link.setAttribute('data-set-partner', partner);
      }
    });
  }

  // ── CTA Click Tracking ──
  function attachCTATracking() {
    var ctas = document.querySelectorAll('.btn-cta, .btn-gold, .cta-button, [class*="cta"], .buy-btn, button[type="submit"]');
    ctas.forEach(function(el) {
      el.addEventListener('click', function() {
        trackEvent('cta_click', {
          cta_text: (el.textContent || '').trim().substring(0, 100),
          cta_class: el.className
        });
      });
    });
  }

  // ── Scroll Depth Tracking ──
  function attachScrollTracking() {
    var milestones = [25, 50, 75, 90];
    var fired = {};
    window.addEventListener('scroll', function() {
      var scrollPct = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
      milestones.forEach(function(m) {
        if (scrollPct >= m && !fired[m]) {
          fired[m] = true;
          trackEvent('scroll_depth', { depth_percent: m });
        }
      });
    }, { passive: true });
  }

  // ── Time-on-Page Engagement ──
  function attachEngagementTracking() {
    var intervals = [30, 60, 120];
    intervals.forEach(function(sec) {
      setTimeout(function() {
        trackEvent('page_engaged', { seconds: sec });
      }, sec * 1000);
    });
  }

  // ── Initialize ──
  function init() {
    attachAffiliateTracking();
    attachCTATracking();
    attachScrollTracking();
    attachEngagementTracking();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  window.setTrack = trackEvent;

})();
