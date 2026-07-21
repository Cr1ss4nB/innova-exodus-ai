const listeners = new Set();

let state = {
  documents: [],
  status: 'loading', // loading | ready | error
};

function notify() {
  for (const listener of listeners) listener(state);
}

/**
 * @param {(state: {documents: Array, status: string}) => void} listener
 * @returns {() => void} funcion para cancelar la suscripcion
 */
export function subscribeDocuments(listener) {
  listeners.add(listener);
  listener(state);
  return () => listeners.delete(listener);
}

export function getDocumentsState() {
  return state;
}

export function setDocuments(documents) {
  state = { ...state, documents, status: 'ready' };
  notify();
}

export function setDocumentsError() {
  state = { ...state, status: 'error' };
  notify();
}

export function addPendingDocument(pendingDocument) {
  state = { ...state, documents: [...state.documents, pendingDocument] };
  notify();
}

export function replacePendingDocument(tempId, record) {
  state = {
    ...state,
    documents: state.documents.map((doc) => (doc.document_id === tempId ? record : doc)),
  };
  notify();
}

export function removeDocument(documentId) {
  state = {
    ...state,
    documents: state.documents.filter((doc) => doc.document_id !== documentId),
  };
  notify();
}
