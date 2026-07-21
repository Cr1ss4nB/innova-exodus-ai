import { createElement } from '../utils/dom.js';

let dialogEl = null;

function ensureDialog() {
  if (!dialogEl) {
    dialogEl = createElement('dialog', { className: 'confirm-dialog' });
    document.body.append(dialogEl);
  }
  return dialogEl;
}

/**
 * Muestra un dialogo de confirmacion y resuelve true si el usuario confirma.
 * @param {{title: string, message: string, confirmLabel?: string}} options
 * @returns {Promise<boolean>}
 */
export function confirmAction({ title, message, confirmLabel = 'Eliminar' }) {
  const dialog = ensureDialog();
  dialog.replaceChildren();

  const titleEl = createElement('p', { className: 'confirm-title', text: title });
  const messageEl = createElement('p', { className: 'confirm-message', text: message });

  const cancelBtn = createElement('button', {
    className: 'btn btn-ghost',
    text: 'Cancelar',
    attrs: { type: 'button' },
  });

  const confirmBtn = createElement('button', {
    className: 'btn btn-danger',
    text: confirmLabel,
    attrs: { type: 'button' },
  });

  dialog.append(
    titleEl,
    messageEl,
    createElement('div', { className: 'confirm-actions', children: [cancelBtn, confirmBtn] })
  );

  return new Promise((resolve) => {
    const finish = (result) => {
      dialog.close();
      resolve(result);
    };

    cancelBtn.addEventListener('click', () => finish(false), { once: true });
    confirmBtn.addEventListener('click', () => finish(true), { once: true });
    dialog.addEventListener('cancel', () => resolve(false), { once: true });

    dialog.showModal();
  });
}
