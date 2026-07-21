import { createElement } from '../utils/dom.js';
import { formatBytes, formatDate } from '../utils/formatters.js';

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

  const info = createElement('div', {
    className: 'document-info',
    children: [
      createElement('p', { className: 'document-name', text: doc.filename }),
      createElement('p', { className: 'document-meta', text: meta }),
    ],
  });

  const item = createElement('li', {
    className: `document-item${doc.isPending ? ' is-pending' : ''}`,
    children: [icon, info],
  });

  if (!doc.isPending) {
    const deleteBtn = createElement('button', {
      className: 'document-delete',
      html: '&times;',
      attrs: { type: 'button', 'aria-label': `Eliminar ${doc.filename}` },
    });
    deleteBtn.addEventListener('click', () => onDelete(doc.document_id));
    item.append(deleteBtn);
  }

  return item;
}
