'use strict';
// Test harness: runs the generated page's real <script> in a vm with a minimal fake DOM,
// drives it by clicking, and prints what it rendered as JSON.
//
// The vm context deliberately has NO fetch, XMLHttpRequest, WebSocket, navigator or
// location, so any network use by the page throws a ReferenceError and fails the run.
// The fake DOM has no innerHTML (setting it throws), so markup injection from data is
// impossible to perform without failing the run.
//
// usage: node harness.js <page.html>

const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync(process.argv[2], 'utf8');
const dataMatch = /<script id="fv-data" type="application\/json">([\s\S]*?)<\/script>/.exec(html);
if (!dataMatch) { throw new Error('data block not found'); }
const pageScripts = [...html.matchAll(/<script(?![^>]*type="application\/json")[^>]*>([\s\S]*?)<\/script>/g)];
if (pageScripts.length !== 1) { throw new Error('expected exactly one page script, found ' + pageScripts.length); }

function textNode(t) { return { isText: true, text: String(t) }; }

function el(tag) {
  const node = {
    tag, attrs: {}, children: [], listeners: {},
    get firstChild() { return this.children[0] || null; },
    appendChild(c) { this.children.push(c); return c; },
    removeChild(c) { const i = this.children.indexOf(c); if (i >= 0) { this.children.splice(i, 1); } return c; },
    setAttribute(k, v) { this.attrs[k] = String(v); },
    getAttribute(k) { return k in this.attrs ? this.attrs[k] : null; },
    addEventListener(type, fn) { (this.listeners[type] = this.listeners[type] || []).push(fn); },
    get textContent() { return this.children.map(c => c.isText ? c.text : c.textContent).join(''); },
    set innerHTML(v) { throw new Error('innerHTML is forbidden'); },
    set outerHTML(v) { throw new Error('outerHTML is forbidden'); },
    insertAdjacentHTML() { throw new Error('insertAdjacentHTML is forbidden'); },
  };
  return node;
}

const statics = {};
const document = {
  getElementById(id) {
    if (id === 'fv-data') { return { textContent: dataMatch[1] }; }
    if (!statics[id]) { statics[id] = el('div'); statics[id].attrs.id = id; }
    return statics[id];
  },
  createElement: el,
  createTextNode: textNode,
  write() { throw new Error('document.write is forbidden'); },
};

function walk(node, fn) {
  if (node.isText) { return; }
  fn(node);
  node.children.forEach(c => walk(c, fn));
}
function findAll(pred) {
  const found = [];
  Object.keys(statics).forEach(id => walk(statics[id], n => { if (pred(n)) { found.push(n); } }));
  return found;
}
function byId(id) {
  const direct = statics[id];
  if (direct) { return direct; }
  return findAll(n => n.attrs.id === id)[0] || null;
}
function click(node) { (node.listeners.click || []).forEach(fn => fn({ preventDefault() {} })); }
const tiles = () => findAll(n => n.tag === 'button' && n.attrs['data-slug']);
const pressedTiles = () => tiles().filter(n => n.attrs['aria-pressed'] === 'true');

vm.runInNewContext(pageScripts[0][1], { document }, { filename: 'page-script' });

const INTERACTIVE = new Set(['button', 'a', 'input', 'select', 'textarea', 'form']);
function snapshot() {
  const result = byId('fv-result');
  const status = findAll(n => n.attrs.id === 'fv-status-line')[0];
  const details = findAll(n => n.attrs.id === 'fv-status-details')[0];
  const interactive = [];
  walk(result, n => { if (INTERACTIVE.has(n.tag)) { interactive.push(n.tag); } });
  return {
    selected: pressedTiles().map(n => n.attrs['data-slug']),
    resultText: result.textContent,
    fusionName: (findAll(n => n.attrs.id === 'fv-fusion-name')[0] || { textContent: null }).textContent,
    missingText: (findAll(n => n.attrs.id === 'fv-missing')[0] || { textContent: null }).textContent,
    statusLine: status ? status.textContent : null,
    detailsPresent: !!details,
    detailsOpenAttr: details ? ('open' in details.attrs) : null,
    detailsText: details ? details.textContent : null,
    interactiveInResult: interactive,
    sourceNames: findAll(n => n.attrs['data-source']).map(n => n.attrs['data-source']),
    ownership: findAll(n => n.attrs['data-ownership']).map(n => ({ slug: n.attrs['data-ownership'], text: n.textContent })),
    footerText: byId('fv-footer').textContent,
    comparisonPresent: findAll(n => n.attrs.id === 'fv-comparison').length === 1,
    comparisonText: (findAll(n => n.attrs.id === 'fv-comparison')[0] || { textContent: null }).textContent,
    comparisonTally: (findAll(n => n.attrs.id === 'fv-cmp-tally')[0] || { textContent: null }).textContent,
    comparisonTraits: findAll(n => n.attrs['data-cmp-trait']).map(n => ({ id: n.attrs['data-cmp-trait'], outcome: n.attrs['data-outcome'], text: n.textContent })),
    comparisonSlots: findAll(n => n.attrs['data-cmp-slot']).map(n => ({ slot: n.attrs['data-cmp-slot'], origin: n.attrs['data-origin'], text: n.textContent })),
  };
}

const out = { initial: snapshot(), pairs: [] };
const slugs = tiles().map(n => n.attrs['data-slug']);
function clickSlug(s) { click(tiles().filter(n => n.attrs['data-slug'] === s)[0]); }
function selectPair(x, y) {
  while (pressedTiles().length) { click(pressedTiles()[0]); }
  clickSlug(x);
  clickSlug(y);
}
for (const x of slugs) {
  for (const y of slugs) {
    if (x === y) { continue; }
    selectPair(x, y);
    out.pairs.push(Object.assign({ x, y }, snapshot()));
  }
}

// selecting the same character twice must not select it twice
while (pressedTiles().length) { click(pressedTiles()[0]); }
clickSlug(slugs[0]);
clickSlug(slugs[0]);
out.afterDoubleClick = snapshot();

// a third selection replaces the oldest
while (pressedTiles().length) { click(pressedTiles()[0]); }
clickSlug(slugs[0]); clickSlug(slugs[1]); clickSlug(slugs[2]);
out.afterThird = snapshot();

process.stdout.write(JSON.stringify(out));
