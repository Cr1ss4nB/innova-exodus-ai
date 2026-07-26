import { API_ROUTES } from '../config.js';
import { toApiError } from '../utils/errors.js';

/**
 * Verifica el estado del backend.
 * @returns {Promise<boolean>}
 */
export async function checkHealth() {
  try {
    const response = await fetch(API_ROUTES.health);
    return response.ok;
  } catch {
    return false;
  }
}

/**
 * Obtiene todos los documentos registrados.
 * @returns {Promise<{documents: import('../types.js').DocumentRecord[], total: number}>}
 */
export async function fetchDocuments() {
  const response = await fetch(API_ROUTES.documents);
  if (!response.ok) throw await toApiError(response);
  return response.json();
}

/**
 * Sube un PDF para procesarlo e indexarlo.
 * @param {File} file
 * @returns {Promise<import('../types.js').DocumentRecord>}
 */
export async function uploadDocument(file) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(API_ROUTES.documents, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) throw await toApiError(response);
  return response.json();
}

/**
 * Procesa e indexa los PDFs corporativos de resources/documents/, omitiendo
 * automaticamente los que ya esten registrados.
 * @returns {Promise<{loaded: import('../types.js').DocumentRecord[], already_existing: string[], total_loaded: number, total_already_existing: number}>}
 */
export async function loadCorporateDocuments() {
  const response = await fetch(`${API_ROUTES.documents}/corporate`, {
    method: 'POST',
  });

  if (!response.ok) throw await toApiError(response);
  return response.json();
}

/**
 * Elimina un documento y sus vectores asociados.
 * @param {string} documentId
 */
export async function deleteDocument(documentId) {
  const response = await fetch(`${API_ROUTES.documents}/${documentId}`, {
    method: 'DELETE',
  });

  if (!response.ok) throw await toApiError(response);
  return response.json();
}

/**
 * Envia una pregunta al asistente, junto con un historial corto y efimero de la conversacion
 * actual (nunca se persiste en el backend).
 * @param {string} question
 * @param {import('../types.js').ChatHistoryTurn[]} [history]
 * @returns {Promise<{answer: string, sources: import('../types.js').SourceReference[]}>}
 */
export async function sendMessage(question, history = []) {
  const response = await fetch(API_ROUTES.chat, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, history }),
  });

  if (!response.ok) throw await toApiError(response);
  return response.json();
}
