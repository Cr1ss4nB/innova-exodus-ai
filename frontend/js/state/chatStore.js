const listeners = new Set();

let state = {
  messages: [],
  isThinking: false,
};

function notify() {
  for (const listener of listeners) listener(state);
}

/**
 * @param {(state: {messages: Array, isThinking: boolean}) => void} listener
 * @returns {() => void}
 */
export function subscribeChat(listener) {
  listeners.add(listener);
  listener(state);
  return () => listeners.delete(listener);
}

export function getChatState() {
  return state;
}

/**
 * @param {import('../types.js').ChatMessage} message
 */
export function addMessage(message) {
  state = { ...state, messages: [...state.messages, message] };
  notify();
}

export function setThinking(isThinking) {
  state = { ...state, isThinking };
  notify();
}

/**
 * Vacia el historial visual de la conversacion. No afecta documentos, FAISS ni el backend.
 */
export function clearMessages() {
  state = { ...state, messages: [], isThinking: false };
  notify();
}

export function createMessageId() {
  return typeof crypto !== 'undefined' && crypto.randomUUID
    ? crypto.randomUUID()
    : `msg-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}
