import { initSidebar } from './components/sidebar.js';
import { initChatWindow } from './components/chatWindow.js';
import { initChatInput } from './components/chatInput.js';

document.addEventListener('DOMContentLoaded', () => {
  initSidebar();
  initChatWindow();
  initChatInput();
});
