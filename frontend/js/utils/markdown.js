function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function renderInline(text) {
  let result = escapeHtml(text);
  result = result.replace(/`([^`]+)`/g, '<code>$1</code>');
  result = result.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  result = result.replace(/__([^_]+)__/g, '<strong>$1</strong>');
  result = result.replace(/\*([^*]+)\*/g, '<em>$1</em>');
  result = result.replace(/(?<!_)_([^_]+)_(?!_)/g, '<em>$1</em>');
  return result;
}

/**
 * Convierte un subconjunto simple de Markdown (negritas, cursivas, codigo, listas y saltos
 * de linea) a HTML, escapando primero cualquier HTML original para evitar inyecciones.
 * No altera el contenido: solo cambia el formato de presentacion.
 * @param {string} text
 * @returns {string} HTML listo para insertar con innerHTML
 */
export function renderMarkdown(text) {
  const lines = text.split('\n');
  const htmlParts = [];

  let listBuffer = [];
  let listType = null;
  let paragraphBuffer = [];
  let codeBuffer = [];
  let inCodeBlock = false;

  const flushList = () => {
    if (listBuffer.length > 0) {
      const tag = listType === 'ordered' ? 'ol' : 'ul';
      htmlParts.push(`<${tag}>${listBuffer.join('')}</${tag}>`);
      listBuffer = [];
      listType = null;
    }
  };

  const flushParagraph = () => {
    if (paragraphBuffer.length > 0) {
      htmlParts.push(`<p>${paragraphBuffer.join('<br>')}</p>`);
      paragraphBuffer = [];
    }
  };

  for (const line of lines) {
    if (line.trim().startsWith('```')) {
      if (inCodeBlock) {
        htmlParts.push(`<pre><code>${escapeHtml(codeBuffer.join('\n'))}</code></pre>`);
        codeBuffer = [];
        inCodeBlock = false;
      } else {
        flushParagraph();
        flushList();
        inCodeBlock = true;
      }
      continue;
    }

    if (inCodeBlock) {
      codeBuffer.push(line);
      continue;
    }

    const unorderedMatch = line.match(/^\s*[-*]\s+(.*)/);
    const orderedMatch = line.match(/^\s*\d+\.\s+(.*)/);

    if (unorderedMatch) {
      flushParagraph();
      if (listType !== 'unordered') flushList();
      listType = 'unordered';
      listBuffer.push(`<li>${renderInline(unorderedMatch[1])}</li>`);
      continue;
    }

    if (orderedMatch) {
      flushParagraph();
      if (listType !== 'ordered') flushList();
      listType = 'ordered';
      listBuffer.push(`<li>${renderInline(orderedMatch[1])}</li>`);
      continue;
    }

    flushList();

    if (line.trim() === '') {
      flushParagraph();
    } else {
      paragraphBuffer.push(renderInline(line));
    }
  }

  flushList();
  flushParagraph();

  if (inCodeBlock && codeBuffer.length > 0) {
    htmlParts.push(`<pre><code>${escapeHtml(codeBuffer.join('\n'))}</code></pre>`);
  }

  return htmlParts.join('');
}
