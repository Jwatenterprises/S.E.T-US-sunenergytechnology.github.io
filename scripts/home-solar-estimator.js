// S.E.T. Solar US: ZIP-first home solar estimator (added 2026-11-10).
// Step 1 ZIP -> Step 2 monthly bill (+ editable rate) -> Step 3 roof shade -> on-site estimate card -> quote marketplace.
// Rough planning estimate only: state-average rates and sun hours, no incentives or tax credits included.
(function () {
  'use strict';
  var root = document.getElementById('hse');
  if (!root) return;

  // ZIP3 prefix ranges -> state
  var Z = [[10,27,'MA'],[28,29,'RI'],[30,38,'NH'],[39,49,'ME'],[50,54,'VT'],[55,55,'MA'],[56,59,'VT'],[60,69,'CT'],[70,89,'NJ'],
    [100,149,'NY'],[150,196,'PA'],[197,199,'DE'],[200,205,'DC'],[206,219,'MD'],[220,246,'VA'],[247,268,'WV'],[270,289,'NC'],
    [290,299,'SC'],[300,319,'GA'],[320,349,'FL'],[350,369,'AL'],[370,385,'TN'],[386,397,'MS'],[398,399,'GA'],[400,427,'KY'],
    [430,459,'OH'],[460,479,'IN'],[480,499,'MI'],[500,528,'IA'],[530,549,'WI'],[550,567,'MN'],[570,577,'SD'],[580,588,'ND'],
    [590,599,'MT'],[600,629,'IL'],[630,658,'MO'],[660,679,'KS'],[680,693,'NE'],[700,714,'LA'],[716,729,'AR'],[730,749,'OK'],
    [750,799,'TX'],[800,816,'CO'],[820,831,'WY'],[832,838,'ID'],[840,847,'UT'],[850,865,'AZ'],[870,884,'NM'],[885,885,'TX'],
    [889,898,'NV'],[900,961,'CA'],[967,968,'HI'],[970,979,'OR'],[980,994,'WA'],[995,999,'AK']];
  // Approximate state averages: [residential cents/kWh, average peak sun hours/day]. Planning defaults only; user can edit the rate.
  var S = {AL:[15,4.7],AK:[25,3.0],AZ:[15,6.0],AR:[13,4.7],CA:[32,5.5],CO:[16,5.2],CT:[30,4.1],DE:[17,4.4],DC:[19,4.3],FL:[15,5.0],
    GA:[15,4.8],HI:[42,5.5],ID:[12,4.8],IL:[17,4.2],IN:[16,4.2],IA:[15,4.4],KS:[15,5.0],KY:[13,4.3],LA:[13,4.8],ME:[28,4.1],
    MD:[19,4.4],MA:[31,4.1],MI:[19,3.9],MN:[16,4.3],MS:[14,4.8],MO:[14,4.5],MT:[13,4.4],NE:[12,4.7],NV:[15,5.8],NH:[26,4.1],
    NJ:[21,4.3],NM:[15,6.0],NY:[25,4.0],NC:[14,4.7],ND:[12,4.3],OH:[17,4.0],OK:[13,5.0],OR:[15,4.0],PA:[19,4.1],RI:[30,4.1],
    SC:[15,4.8],SD:[13,4.6],TN:[13,4.5],TX:[15,5.0],UT:[12,5.3],VT:[23,3.9],VA:[15,4.5],WA:[13,3.6],WV:[15,4.0],WI:[18,4.1],WY:[13,5.0]};
  var NAMES = {AL:'Alabama',AK:'Alaska',AZ:'Arizona',AR:'Arkansas',CA:'California',CO:'Colorado',CT:'Connecticut',DE:'Delaware',DC:'Washington, DC',
    FL:'Florida',GA:'Georgia',HI:'Hawaii',ID:'Idaho',IL:'Illinois',IN:'Indiana',IA:'Iowa',KS:'Kansas',KY:'Kentucky',LA:'Louisiana',ME:'Maine',
    MD:'Maryland',MA:'Massachusetts',MI:'Michigan',MN:'Minnesota',MS:'Mississippi',MO:'Missouri',MT:'Montana',NE:'Nebraska',NV:'Nevada',
    NH:'New Hampshire',NJ:'New Jersey',NM:'New Mexico',NY:'New York',NC:'North Carolina',ND:'North Dakota',OH:'Ohio',OK:'Oklahoma',OR:'Oregon',
    PA:'Pennsylvania',RI:'Rhode Island',SC:'South Carolina',SD:'South Dakota',TN:'Tennessee',TX:'Texas',UT:'Utah',VT:'Vermont',VA:'Virginia',
    WA:'Washington',WV:'West Virginia',WI:'Wisconsin',WY:'Wyoming'};
  var COST_LO = 2.5, COST_HI = 3.3; // installed $/W before incentives, typical U.S. range (planning only)
  var SHADE = { none: [1.0, 'little or no shade'], some: [0.85, 'some shade'], heavy: [0.65, 'heavy shade'] };

  function state(zip) { var p = parseInt(zip.slice(0, 3), 10); for (var i = 0; i < Z.length; i++) if (p >= Z[i][0] && p <= Z[i][1]) return Z[i][2]; return null; }
  function money(n) { return '$' + Math.round(n).toLocaleString('en-US'); }
  function ev(name, label) { if (typeof window.gtag === 'function') window.gtag('event', name, { event_category: 'Home Solar', event_label: label }); }

  var d = { zip: '', st: null, bill: '', rate: '', shade: '' };

  function step1() {
    root.innerHTML =
      '<div class="hse-step"><span class="hse-n">Step 1 of 3</span><label for="hseZip">Your ZIP code</label>' +
      '<form class="rooftop-form" id="hseF1"><input id="hseZip" class="rooftop-input" type="text" inputmode="numeric" maxlength="5" pattern="[0-9]{5}" placeholder="Enter ZIP Code" required value="' + d.zip + '" aria-label="ZIP code">' +
      '<button type="submit" class="rooftop-submit">Estimate My Savings &rarr;</button></form>' +
      '<p class="hse-note">No signup needed. We use your ZIP only to pick your state&rsquo;s average rate and sun hours; it isn&rsquo;t stored.</p></div>';
    document.getElementById('hseF1').addEventListener('submit', function (e) {
      e.preventDefault(); var z = document.getElementById('hseZip').value.trim();
      var st = /^\d{5}$/.test(z) ? state(z) : null;
      if (!st) { document.getElementById('hseZip').setCustomValidity('Please enter a valid U.S. ZIP code'); document.getElementById('hseZip').reportValidity(); return; }
      d.zip = z; d.st = st; if (!d.rate) d.rate = S[st][0]; ev('home_solar_step', 'zip'); step2();
    });
    document.getElementById('hseZip').addEventListener('input', function () { this.setCustomValidity(''); });
  }

  function step2() {
    root.innerHTML =
      '<div class="hse-step"><span class="hse-n">Step 2 of 3 &middot; ' + NAMES[d.st] + '</span><label for="hseBill">Average monthly electric bill</label>' +
      '<form id="hseF2" class="hse-form2"><div class="hse-row"><span class="hse-pre">$</span><input id="hseBill" class="rooftop-input" type="number" min="20" max="2000" step="1" required placeholder="e.g. 180" value="' + d.bill + '"></div>' +
      '<label for="hseRate" class="hse-small">Your rate (cents per kWh) &mdash; we filled in the ' + NAMES[d.st] + ' average; use the number from your bill if you know it</label>' +
      '<div class="hse-row"><input id="hseRate" class="rooftop-input" type="number" min="5" max="80" step="0.1" required value="' + d.rate + '"><span class="hse-post">&cent;/kWh</span></div>' +
      '<div class="hse-btns"><button type="button" class="hse-back">&larr; Back</button><button type="submit" class="rooftop-submit">Next &rarr;</button></div></form></div>';
    root.querySelector('.hse-back').onclick = step1;
    document.getElementById('hseF2').addEventListener('submit', function (e) {
      e.preventDefault(); d.bill = parseFloat(document.getElementById('hseBill').value); d.rate = parseFloat(document.getElementById('hseRate').value);
      ev('home_solar_step', 'bill'); step3();
    });
  }

  function step3() {
    root.innerHTML =
      '<div class="hse-step"><span class="hse-n">Step 3 of 3</span><label>How much shade does your roof get?</label><div class="hse-opts">' +
      Object.keys(SHADE).map(function (k) { return '<button type="button" data-k="' + k + '">' + SHADE[k][1].charAt(0).toUpperCase() + SHADE[k][1].slice(1) + '</button>'; }).join('') +
      '</div><div class="hse-btns"><button type="button" class="hse-back">&larr; Back</button></div></div>';
    root.querySelector('.hse-back').onclick = step2;
    root.querySelectorAll('.hse-opts button').forEach(function (b) {
      b.onclick = function () { d.shade = b.getAttribute('data-k'); ev('home_solar_step', 'shade'); result(); };
    });
  }

  function result() {
    var psh = S[d.st][1], sh = SHADE[d.shade][0];
    var monthlyKwh = d.bill / (d.rate / 100);
    var annualKwh = monthlyKwh * 12;
    var offset = 0.9; // size to cover ~90% of use
    var kw = annualKwh * offset / (psh * 365 * 0.78 * sh); // 0.78 system losses
    kw = Math.max(2, Math.min(kw, 20));
    var y1 = Math.min(annualKwh, kw * psh * 365 * 0.78 * sh) * (d.rate / 100);
    var total = 0; for (var y = 0; y < 25; y++) total += y1 * Math.pow(1.025, y) * Math.pow(0.995, y); // +2.5%/yr rates, -0.5%/yr panel output
    var cLo = kw * 1000 * COST_LO, cHi = kw * 1000 * COST_HI;
    var pbLo = cLo / y1, pbHi = cHi / y1;
    var heavy = d.shade === 'heavy';
    ev('home_solar_estimate', d.st);
    root.innerHTML =
      '<div class="hse-card">' +
      '<div class="hse-card-h">Your rough solar estimate &middot; ' + NAMES[d.st] + '</div>' +
      '<div class="hse-grid">' +
      '<div><span class="hse-big">' + kw.toFixed(1) + ' kW</span><span class="hse-lbl">Estimated system size (~' + Math.round(kw * 1000 / 400) + ' panels)</span></div>' +
      '<div><span class="hse-big">' + money(y1) + '</span><span class="hse-lbl">Estimated first-year bill savings</span></div>' +
      '<div><span class="hse-big">' + money(total) + '</span><span class="hse-lbl">Estimated 25-year savings</span></div>' +
      '<div><span class="hse-big">' + money(cLo) + '&ndash;' + money(cHi) + '</span><span class="hse-lbl">Typical installed cost before any incentives</span></div>' +
      '</div>' +
      '<p class="hse-pb">Simple payback before incentives: roughly <strong>' + Math.round(pbLo) + '&ndash;' + Math.round(pbHi) + ' years</strong>.' +
      (pbLo > 14 ? ' That&rsquo;s long &mdash; local incentives, financing terms, and your utility&rsquo;s solar credit rules will decide whether rooftop solar pays off for you.' : '') + '</p>' +
      (heavy ? '<p class="hse-warn">Heavy shade cuts output a lot. Ask installers for a shade analysis; a ground mount or community solar may be a better fit.</p>' : '') +
      '<p class="hse-assume">Estimate, not a quote. Based on your $' + Math.round(d.bill) + '/month bill at ' + d.rate + '&cent;/kWh (&asymp;' + Math.round(monthlyKwh).toLocaleString() + ' kWh/month), ' +
      NAMES[d.st] + ' average sun (' + psh + ' peak sun hours/day), ' + SHADE[d.shade][1] + ', sized to cover about 90% of your use, rates rising 2.5%/yr, panels losing 0.5%/yr. ' +
      'It does not include tax credits, rebates, financing costs, or your utility&rsquo;s net-metering or export rules, which vary by location. Real quotes depend on your roof, equipment, and installer.</p>' +
      '<div class="hse-next"><a class="rooftop-submit hse-go" href="https://www.energysage.com/market/start/?zip=' + encodeURIComponent(d.zip) + '" target="_blank" rel="sponsored noopener noreferrer">Compare Installer Quotes on EnergySage &#8599;</a>' +
      '<p class="hse-note">You&rsquo;ll continue on EnergySage, a quote marketplace where you compare bids from multiple installers. Read how they share your contact details before you enter a phone number. S.E.T. may earn a referral fee; it doesn&rsquo;t change our advice.</p>' +
      '<button type="button" class="hse-back">&larr; Start over</button></div></div>';
    root.querySelector('.hse-go').addEventListener('click', function () { ev('rooftop_solar_quote_click', 'EnergySage'); });
    root.querySelector('.hse-back').onclick = function () { d = { zip: '', st: null, bill: '', rate: '', shade: '' }; step1(); };
  }

  var css = document.createElement('style');
  css.textContent =
    '#hse{margin-top:6px}#hse label{display:block;font-weight:700;margin:6px 0 8px}' +
    '.hse-n{display:inline-block;font-size:.78rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;opacity:.75}' +
    '.hse-small{font-weight:500!important;font-size:.85rem;margin-top:12px!important;opacity:.85}' +
    '.hse-row{display:flex;align-items:center;gap:8px;max-width:360px}.hse-row .rooftop-input{flex:1}.hse-pre,.hse-post{font-weight:700}' +
    '.hse-btns{display:flex;gap:10px;margin-top:14px;align-items:center}.hse-back{background:none;border:0;color:inherit;opacity:.75;cursor:pointer;font-weight:600;text-decoration:underline}' +
    '.hse-opts{display:flex;gap:10px;flex-wrap:wrap}.hse-opts button{border:2px solid currentColor;background:transparent;color:inherit;border-radius:999px;padding:10px 18px;font-weight:700;cursor:pointer}' +
    '.hse-opts button:hover{background:rgba(255,255,255,.12)}' +
    '.hse-note{font-size:.82rem;opacity:.8;margin-top:10px}' +
    '.hse-card{background:#fff;color:#1e1e2e;border-radius:14px;padding:20px;text-align:left}' +
    '.hse-card p,.hse-card strong{color:#334155}.hse-card .hse-assume{color:#64748b}.hse-card .hse-warn{color:#7f1d1d}' +
    '.hse-card-h{font-weight:800;font-size:1.05rem;margin-bottom:12px;color:#0e2a47}' +
    '.hse-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-bottom:12px}' +
    '.hse-grid>div{background:#f3f6fa;border-radius:10px;padding:12px}.hse-big{display:block;font-size:1.35rem;font-weight:800;color:#0066FF}.hse-lbl{font-size:.82rem;color:#475569}' +
    '.hse-pb{margin:6px 0}.hse-warn{background:#fff4f4;border-left:4px solid #e5484d;padding:8px 12px;border-radius:0 8px 8px 0;font-size:.9rem}' +
    '.hse-assume{font-size:.78rem;color:#64748b;margin:10px 0}.hse-next .hse-go{display:inline-block;text-decoration:none}.hse-next .hse-note{color:#475569;opacity:1}' +
    '.hse-next .hse-back{color:#475569}@media(max-width:560px){.hse-grid{grid-template-columns:1fr}}';
  document.head.appendChild(css);
  step1();
})();
