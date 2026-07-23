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
 * Como el historial que se envia al backend se deriva de este mismo arreglo, limpiarlo aqui
 * hace que el siguiente mensaje viaje sin ningun contexto previo, automaticamente.
 */
export function clearMessages() {
  state = { ...state, messages: [], isThinking: false };
  notify();
}

/**
 * Retorna los ultimos N intercambios completos (pregunta de usuario + respuesta del asistente),
 * en orden cronologico. Ignora preguntas que quedaron sin respuesta (por ejemplo, si el backend
 * devolvio un error), ya que no representan un intercambio real que ayude a dar contexto.
 * @param {number} [limit]
 * @returns {import('../types.js').ChatHistoryTurn[]}
 */
export function getRecentHistory(limit = 3) {
  const turns = [];
  let pendingQuestion = null;

  for (const message of state.messages) {
    if (message.role === 'user') {
      pendingQuestion = message.text;
    } else if (message.role === 'assistant' && pendingQuestion !== null) {
      turns.push({ question: pendingQuestion, answer: message.text });
      pendingQuestion = null;
    } else if (message.role === 'error') {
      pendingQuestion = null;
    }
  }

  return turns.slice(-limit);
}

export function createMessageId() {
  return typeof crypto !== 'undefined' && crypto.randomUUID
    ? crypto.randomUUID()
    : `msg-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}
