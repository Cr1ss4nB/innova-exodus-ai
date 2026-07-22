import { createElement } from '../utils/dom.js';
import { formatBytes, formatDate } from '../utils/formatters.js';
import { API_ROUTES } from '../config.js';

/**
 * @param {import('../types.js').DocumentRecord & {isPending?: boolean}} doc
 * @param {(documentId: string) => void} onDelete
 * @returns {HTMLElement}
 */
export function renderDocumentItem(doc, onDelete) {
  const icon = createElement('div', {
    className: 'document-icon',
    text: doc.isPending ? '⏳' : '📄',
  });

  const meta = doc.isPending
    ? 'Procesando…'
    : `${formatDate(doc.upload_date)} · ${doc.total_pages} pág. · ${formatBytes(doc.size_bytes)}`;

  const nameEl = createElement('p', { className: 'document-name', text: doc.filename });
  nameEl.title = doc.filename;

  const info = createElement('div', {
    className: 'document-info',
    children: [nameEl, createElement('p', { className: 'document-meta', text: meta })],
  });

  const item = createElement('li', {
    className: `document-item${doc.isPending ? ' is-pending' : ''}`,
    children: [icon, info],
  });

  if (!doc.isPending) {
    item.classList.add('document-item--clickable');
    item.tabIndex = 0;
    item.setAttribute('role', 'button');
    item.setAttribute('title', `Abrir "${doc.filename}" en una nueva pestaña`);

    const openDocument = () => {
      window.open(API_ROUTES.documentView(doc.document_id), '_blank', 'noopener,noreferrer');
    };

    item.addEventListener('click', openDocument);
    item.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        openDocument();
      }
    });

    const deleteBtn = createElement('button', {
      className: 'document-delete',
      html: '&times;',
      attrs: { type: 'button', 'aria-label': `Eliminar ${doc.filename}` },
    });
    deleteBtn.addEventListener('click', (event) => {
      event.stopPropagation();
      onDelete(doc.document_id);
    });
    item.append(deleteBtn);
  }

  return item;
}
