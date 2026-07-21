/**
 * Crea un elemento DOM con atributos, clases e hijos en una sola llamada.
 * @param {string} tag
 * @param {Object} [options]
 * @param {string} [options.className]
 * @param {string} [options.text]
 * @param {string} [options.html]
 * @param {Object<string,string>} [options.attrs]
 * @param {Array<Node|string>} [options.children]
 * @returns {HTMLElement}
 */
export function createElement(tag, options = {}) {
  const el = document.createElement(tag);

  if (options.className) el.className = options.className;
  if (options.text !== undefined) el.textContent = options.text;
  if (options.html !== undefined) el.innerHTML = options.html;

  if (options.attrs) {
    for (const [key, value] of Object.entries(options.attrs)) {
      el.setAttribute(key, value);
    }
  }

  if (options.children) {
    for (const child of options.children) {
      el.append(child);
    }
  }

  return el;
}

export function qs(selector, parent = document) {
  return parent.querySelector(selector);
}

export function clearChildren(el) {
  while (el.firstChild) {
    el.removeChild(el.firstChild);
  }
}
