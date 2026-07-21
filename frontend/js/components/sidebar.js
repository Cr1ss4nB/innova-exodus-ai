import { qs, clearChildren } from '../utils/dom.js';
import { initials } from '../utils/formatters.js';
import { checkHealth, fetchDocuments, deleteDocument } from '../services/apiClient.js';
import {
  subscribeDocuments,
  getDocumentsState,
  setDocuments,
  setDocumentsError,
  removeDocument,
} from '../state/documentsStore.js';
import { clearMessages } from '../state/chatStore.js';
import { renderDocumentItem } from './documentItem.js';
import { handleUpload } from './uploader.js';
import { confirmAction } from './confirmDialog.js';
import { showToast } from './toast.js';

const HEALTH_CHECK_INTERVAL_MS = 15000;

function setupLogo() {
  const img = qs('#brand-logo');
  const fallback = qs('#brand-logo-fallback');
  fallback.textContent = initials('Innova Exodus');

  const candidates = ['assets/logo.png', 'assets/logo.jpg'];
  let index = 0;

  const tryNext = () => {
    if (index >= candidates.length) {
      img.hidden = true;
      fallback.hidden = false;
      return;
    }
    img.src = candidates[index];
    index += 1;
  };

  img.addEventListener('error', tryNext);
  img.addEventListener('load', () => {
    img.hidden = false;
    fallback.hidden = true;
  });

  tryNext();
}

async function refreshStatus() {
  const dot = qs('#status-dot');
  const text = qs('#status-text');
  const isOnline = await checkHealth();

  dot.classList.toggle('online', isOnline);
  dot.classList.toggle('offline', !isOnline);
  text.textContent = isOnline ? 'Conectado' : 'Sin conexión con el backend';
}

async function onDeleteRequested(documentId) {
  const doc = getDocumentsState().documents.find((item) => item.document_id === documentId);
  const filename = doc ? doc.filename : 'este documento';

  const confirmed = await confirmAction({
    title: 'Eliminar documento',
    message: `¿Eliminar "${filename}"? Esta acción no se puede deshacer y el asistente dejará de usar su contenido.`,
  });

  if (!confirmed) return;

  try {
    const result = await deleteDocument(documentId);
    removeDocument(documentId);
    showToast(`"${result.filename}" fue eliminado.`, 'success');
  } catch (error) {
    showToast(error.message || 'No se pudo eliminar el documento.', 'error');
  }
}

function renderDocuments(state) {
  const list = qs('#document-list');
  const empty = qs('#document-empty');
  clearChildren(list);

  if (state.status === 'error') {
    empty.hidden = false;
    qs('.empty-state-title', empty).textContent = 'No se pudieron cargar los documentos';
    qs('.empty-state-hint', empty).textContent = 'Verifica que el backend esté disponible e intenta de nuevo.';
    return;
  }

  if (state.documents.length === 0) {
    empty.hidden = false;
    qs('.empty-state-title', empty).textContent = 'Aún no hay documentos';
    qs('.empty-state-hint', empty).textContent =
      'Sube un PDF para que el asistente pueda responder con base en él.';
    return;
  }

  empty.hidden = true;

  for (const doc of state.documents) {
    list.append(renderDocumentItem(doc, onDeleteRequested));
  }
}

function setupUpload() {
  const trigger = qs('#upload-trigger');
  const input = qs('#file-input');

  trigger.addEventListener('click', () => input.click());
  input.addEventListener('change', () => {
    const file = input.files[0];
    if (file) handleUpload(file);
    input.value = '';
  });
}

function setupClearChat() {
  const button = qs('#clear-chat');

  button.addEventListener('click', async () => {
    const confirmed = await confirmAction({
      title: 'Limpiar conversación',
      message: 'Se vaciará el historial mostrado en pantalla. Los documentos y el índice no se ven afectados.',
      confirmLabel: 'Limpiar',
    });

    if (!confirmed) return;

    clearMessages();
    showToast('Conversación reiniciada.', 'info');
  });
}

function setupDrawer() {
  const app = qs('#app');
  const sidebar = qs('#sidebar');
  const openBtn = qs('#menu-open');
  const closeBtn = qs('#sidebar-close');
  const backdrop = qs('#backdrop');

  const open = () => {
    sidebar.classList.add('is-open');
    app.classList.add('sidebar-open');
  };

  const close = () => {
    sidebar.classList.remove('is-open');
    app.classList.remove('sidebar-open');
  };

  openBtn.addEventListener('click', open);
  closeBtn.addEventListener('click', close);
  backdrop.addEventListener('click', close);
}

export async function initSidebar() {
  setupLogo();
  setupUpload();
  setupClearChat();
  setupDrawer();
  subscribeDocuments(renderDocuments);

  refreshStatus();
  setInterval(refreshStatus, HEALTH_CHECK_INTERVAL_MS);

  try {
    const { documents } = await fetchDocuments();
    setDocuments(documents);
  } catch {
    setDocumentsError();
  }
}
