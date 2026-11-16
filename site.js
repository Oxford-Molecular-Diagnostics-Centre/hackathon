
/* Site settings. Fill these in when the programme has a place to receive entries. */

const onlineSubmissionReady = SITE_CONFIG.submissionEnabled === true
  && /^https:\/\//.test(SITE_CONFIG.submitUrl)
  && /^https:\/\//.test(SITE_CONFIG.privacyUrl);
document.documentElement.classList.add('js');
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];

function wireFilter(host, items, attr, after) {
  if (!host) return;
  host.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    $$('button', host).forEach(x => x.setAttribute('aria-pressed', x === b));
    items.forEach(it => { it.hidden = b.dataset.v !== 'all' && it.getAttribute(attr) !== b.dataset.v; });
    if (after) after();
  });
}
wireFilter($('#challenge-filters'), $$('.ch'), 'data-ready', () => {
  $$('.theme').forEach(t => { t.hidden = !$$('.ch', t).some(c => !c.hidden); });
});
wireFilter($('#data-filters'), $$('#data-rows tr'), 'data-tier');
$$('[data-theme-jump]').forEach(link => link.addEventListener('click', () => {
  $('#challenge-filters button[data-v=all]')?.click();
}));

if ($('#role-tabs')) {
let role = 'challenge';
const form = () => $('#form-' + role);
function draftText() {
  const f = form();
  const lines = [f.dataset.heading, 'Oxford Cancer AI Challenges — draft proposal', 'Prepared locally; this text is not proof of submission or programme approval.', ''];
  $$('.field', f).forEach(w => {
    const labelElement = $('label', w), c = $('input,select,textarea', w);
    if (!labelElement || !c) return;
    const label = labelElement.dataset.name;
    lines.push(label + (label.endsWith('?') ? '' : ':'), c.value.trim() || '—', '');
  });
  return lines.join('\n').trim();
}
function renderDraft() { $('#draft-text').textContent = draftText(); }
function setRole(r) {
  if (!['challenge', 'team', 'infrastructure'].includes(r)) return;
  role = r;
  $$('#role-tabs button').forEach(b => {
    b.setAttribute('aria-selected', String(b.dataset.tab === r));
    b.tabIndex = b.dataset.tab === r ? 0 : -1;
  });
  $$('.join form').forEach(f => { f.hidden = f.id !== 'form-' + r; });
  $('#draft-status').hidden = true;
  renderDraft();
}
$('#role-tabs').addEventListener('click', e => { const b = e.target.closest('button'); if (b) setRole(b.dataset.tab); });
$('#role-tabs').addEventListener('keydown', e => {
  const tabs = $$('#role-tabs button');
  const current = tabs.indexOf(document.activeElement);
  if (current < 0 || !['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(e.key)) return;
  e.preventDefault();
  const index = e.key === 'Home' ? 0 : e.key === 'End' ? tabs.length - 1
    : (current + (e.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
  setRole(tabs[index].dataset.tab); tabs[index].focus();
});
$$('[data-role]').forEach(a => a.addEventListener('click', () => setRole(a.dataset.role)));
$$('.join form').forEach(f => {
  f.addEventListener('input', renderDraft);
  f.addEventListener('submit', async e => {
    e.preventDefault();
    const err = $('.err', f); err.hidden = true;
    if (!f.reportValidity()) return;
    const box = $('#draft-status'); box.hidden = false;
    if (!onlineSubmissionReady) {
      box.textContent = SITE_CONFIG.contactEmail
        ? 'Your draft is ready. Nothing has been submitted. Copy or download it and share it with ' + SITE_CONFIG.contactEmail + ' when you are ready.'
        : 'Your draft is ready to copy or download. Nothing has been submitted. A submission route and privacy arrangements must be approved before online collection opens.';
      box.focus();
      return;
    }
    const data = Object.fromEntries(new FormData(f).entries());
    data.type = role;
    const submitButton = $('button[type=submit]', f);
    submitButton.disabled = true;
    try {
      const res = await fetch(SITE_CONFIG.submitUrl, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
      if (!res.ok) throw new Error(res.status);
      box.textContent = 'Thank you. We have received your entry.';
      f.reset(); renderDraft();
    } catch {
      box.hidden = true; err.hidden = false;
      err.textContent = 'Submission could not be confirmed. Please retain a copy of your draft and contact the organisers before retrying.';
    } finally { submitButton.disabled = false; }
    if (!box.hidden) box.focus();
  });
});
if (onlineSubmissionReady) {
  $$('.privacy').forEach(a => { a.href = SITE_CONFIG.privacyUrl; a.hidden = false; });
  $('#draft-help').textContent = 'Online collection is enabled under the linked privacy notice. Review your draft and that notice before submitting. This page remains a proposal for the programme.';
  $$('.check span').forEach(span => {
    const link = document.createElement('a'); link.href = SITE_CONFIG.privacyUrl; link.textContent = 'Read the privacy notice.';
    span.replaceChildren(document.createTextNode('I confirm this entry contains no patient data or confidential information and I have read the privacy notice explaining the use of my contact details. '), link);
  });
  $('#form-challenge button[type=submit]').textContent = 'Send research challenge proposal';
  $('#form-team button[type=submit]').textContent = 'Send future interest';
  $('#form-infrastructure button[type=submit]').textContent = 'Send support enquiry';
}
$('#download-draft').addEventListener('click', () => {
  const blob = new Blob([draftText() + '\n'], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url; link.download = 'oxford-cancer-' + role + '-draft.txt';
  document.body.append(link); link.click(); link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 10000);
  const box = $('#draft-status'); box.hidden = false;
  box.textContent = 'Draft download started. Nothing has been submitted.';
});
$('#copy-draft').addEventListener('click', async e => {
  const btn = e.currentTarget;
  try { await navigator.clipboard.writeText(draftText()); btn.textContent = 'Copied'; }
  catch { const r = document.createRange(); r.selectNodeContents($('#draft-text')); const s = getSelection(); s.removeAllRanges(); s.addRange(r); btn.textContent = 'Press Ctrl+C to copy'; }
  setTimeout(() => { btn.textContent = 'Copy draft'; }, 2200);
});
const query = new URLSearchParams(location.search);
setRole(['team','infrastructure'].includes(query.get('role')) ? query.get('role') : 'challenge');
if (query.get('challenge') === 'vaccine') {
  $('#challenge-0').value = 'Cancer vaccine epitope prioritisation'; renderDraft();
}

}

// Native submit controls stay disabled without JavaScript, so draft fields are not sent in a GET URL.
$$('.join form button[type=submit]').forEach(button => { button.disabled = false; });
const menuButton = $('.nav-toggle');
function closeMenu() { $('.site-head')?.classList.remove('nav-open'); menuButton?.setAttribute('aria-expanded','false'); }
menuButton?.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open)); $('.site-head').classList.toggle('nav-open', open);
});
$('#site-nav')?.addEventListener('click', e => { if (e.target.closest('a')) closeMenu(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape' && menuButton?.getAttribute('aria-expanded') === 'true') { closeMenu(); menuButton.focus(); } });
// Open a collapsed brief when reached through a deep link.
function revealLinkedBrief() {
  const el = document.getElementById(location.hash.slice(1));
  for (let ancestor = el?.parentElement; ancestor; ancestor = ancestor.parentElement) {
    if (ancestor.tagName === 'DETAILS') ancestor.open = true;
  }
  if (el?.matches('.ch')) el.querySelector('details')?.setAttribute('open','');
  if (el?.matches('details')) el.setAttribute('open','');
}
addEventListener('hashchange', revealLinkedBrief); revealLinkedBrief();

// LEGACY_SINGLE_PAGE_ROUTES
const LEGACY_ROUTES = {"clinical": "index.html", "explore": "index.html", "how": "programme.html", "schedule": "programme.html", "who": "programme.html", "faq": "programme.html", "terms": "programme.html", "why": "programme.html", "review": "programme.html", "challenges": "challenges.html", "cfdna-benchmark": "challenges.html", "challenge-filters": "challenges.html", "theme-blood": "challenges.html", "multimodal": "challenges.html", "platelet": "challenges.html", "nanopore": "challenges.html", "harmonise": "challenges.html", "theme-tissue": "challenges.html", "histology": "challenges.html", "spatial": "challenges.html", "theme-predict": "challenges.html", "proteomic": "challenges.html", "immuno": "challenges.html", "theme-drugs": "challenges.html", "binding": "challenges.html", "theme-validation": "challenges.html", "assay-prototypes": "challenges.html", "functional-omics": "challenges.html", "theme-vaccines": "vaccines.html", "vaccine-epitopes": "vaccines.html", "prior-art": "vaccines.html", "vaccine-brief": "vaccines.html", "data": "resources.html", "data-filters": "resources.html", "data-rows": "resources.html", "infrastructure": "resources.html", "data-protection": "resources.html", "sources": "resources.html", "events": "precedents.html", "event-assay-a-thon": "precedents.html", "event-tesla": "precedents.html", "event-immrep25": "precedents.html", "event-tap": "precedents.html", "event-adaptyv-pmhc": "precedents.html", "event-gem-rbx1": "precedents.html", "event-dream-pd1": "precedents.html", "deck-mapping": "precedents.html", "overlap": "precedents.html", "review-before-launch": "precedents.html", "join": "propose.html", "role-tabs": "propose.html", "tab-challenge": "propose.html", "tab-team": "propose.html", "tab-infrastructure": "propose.html", "form-challenge": "propose.html", "challenge-0": "propose.html", "challenge-1": "propose.html", "challenge-2": "propose.html", "challenge-3": "propose.html", "challenge-4": "propose.html", "challenge-5": "propose.html", "challenge-6": "propose.html", "access-help": "propose.html", "challenge-7": "propose.html", "challenge-8": "propose.html", "challenge-9": "propose.html", "challenge-availability": "propose.html", "challenge-compute": "propose.html", "challenge-cancer": "propose.html", "challenge-resources": "propose.html", "challenge-notes": "propose.html", "challenge-consent": "propose.html", "form-team": "propose.html", "team-0": "propose.html", "team-1": "propose.html", "team-2": "propose.html", "team-3": "propose.html", "team-4": "propose.html", "team-5": "propose.html", "team-6": "propose.html", "team-7": "propose.html", "team-consent": "propose.html", "form-infrastructure": "propose.html", "infrastructure-0": "propose.html", "infrastructure-1": "propose.html", "infrastructure-2": "propose.html", "infrastructure-3": "propose.html", "infrastructure-4": "propose.html", "infrastructure-5": "propose.html", "infrastructure-6": "propose.html", "infrastructure-7": "propose.html", "infrastructure-consent": "propose.html", "draft-status": "propose.html", "draft-help": "propose.html", "draft-text": "propose.html", "copy-draft": "propose.html", "download-draft": "propose.html"};
if (document.body.dataset.page === 'index.html' && location.hash) {
  const id = location.hash.slice(1); const page = LEGACY_ROUTES[id];
  if (page && page !== 'index.html' && !document.getElementById(id)) location.replace(page + location.hash);
}
