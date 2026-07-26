import { qs } from '../utils/dom.js';
import { sendMessage } from '../services/apiClient.js';
import {
  addMessage,
  setThinking,
  createMessageId,
  getChatState,
  getRecentHistory,
  subscribeChat,
} from '../state/chatStore.js';
import { showToast } from './toast.js';

function autoResize(textarea) {
  textarea.style.height = 'auto';
  textarea.style.height = `${Math.min(textarea.scrollHeight, 140)}px`;
}

async function submitQuestion(textarea) {
  const question = textarea.value.trim();
  if (!question || getChatState().isThinking) return;

  const history = getRecentHistory(3);

  addMessage({ id: createMessageId(), role: 'user', text: question });
  textarea.value = '';
  autoResize(textarea);
  setThinking(true);

  try {
    const result = await sendMessage(question, history);
    addMessage({ id: createMessageId(), role: 'assistant', text: result.answer, sources: result.sources });
  } catch (error) {
    const message = error.message || 'No se pudo obtener una respuesta del asistente.';
    addMessage({ id: createMessageId(), role: 'error', text: message });
    showToast(message, 'error');
  } finally {
    setThinking(false);
    textarea.focus();
  }
}

export function initChatInput() {
  const form = qs('#chat-form');
  const textarea = qs('#chat-input');
  const sendButton = qs('#send-button');

  subscribeChat((state) => {
    textarea.disabled = state.isThinking;
    sendButton.disabled = state.isThinking;
  });

  textarea.addEventListener('input', () => autoResize(textarea));

  textarea.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      submitQuestion(textarea);
    }
  });

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    submitQuestion(textarea);
  });
}