import { createElement } from '../utils/dom.js';

/**
 * Muestra una notificacion transitoria en la esquina inferior derecha.
 * @param {string} message
 * @param {'error'|'success'|'info'} [type]
 */
export function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  const toast = createElement('div', {
    className: `toast toast--${type}`,
    text: message,
  });

  container.append(toast);

  setTimeout(() => {
    toast.remove();
  }, 4500);
}
