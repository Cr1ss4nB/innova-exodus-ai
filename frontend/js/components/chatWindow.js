import { qs, clearChildren } from '../utils/dom.js';
import { subscribeChat } from '../state/chatStore.js';
import { renderMessage, renderThinkingBubble } from './messageBubble.js';

let emptyStateEl = null;

function render(state) {
  const windowEl = qs('#chat-window');
  clearChildren(windowEl);

  if (state.messages.length === 0 && !state.isThinking) {
    windowEl.append(emptyStateEl);
    return;
  }

  for (const message of state.messages) {
    windowEl.append(renderMessage(message));
  }

  if (state.isThinking) {
    windowEl.append(renderThinkingBubble());
  }

  windowEl.scrollTop = windowEl.scrollHeight;
}

export function initChatWindow() {
  emptyStateEl = qs('#chat-empty');
  subscribeChat(render);
}
