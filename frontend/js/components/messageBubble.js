import { createElement } from '../utils/dom.js';

/**
 * @param {import('../types.js').ChatMessage} message
 * @returns {HTMLElement}
 */
export function renderMessage(message) {
  const isUser = message.role === 'user';
  const isError = message.role === 'error';
  const roleClass = isUser ? 'message--user' : isError ? 'message--assistant message--error' : 'message--assistant';

  const bubble = createElement('div', { className: 'bubble', text: message.text });
  const wrapper = createElement('div', { className: `message ${roleClass}`, children: [bubble] });

  if (message.sources && message.sources.length > 0) {
    const chips = message.sources.map((source) =>
      createElement('span', {
        className: 'source-chip',
        text: `${source.document} · p. ${source.page}`,
      })
    );
    wrapper.append(createElement('div', { className: 'sources', children: chips }));
  }

  return wrapper;
}

export function renderThinkingBubble() {
  const dots = [0, 1, 2].map(() => createElement('span', { className: 'thinking-dot' }));
  const bubble = createElement('div', { className: 'bubble thinking-bubble', children: dots });
  return createElement('div', { className: 'message message--assistant', children: [bubble] });
}
