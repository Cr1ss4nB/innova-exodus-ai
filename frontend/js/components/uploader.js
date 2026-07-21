import { uploadDocument } from '../services/apiClient.js';
import { addPendingDocument, removeDocument, replacePendingDocument } from '../state/documentsStore.js';
import { showToast } from './toast.js';

/**
 * Sube un PDF mostrando un estado "pendiente" mientras el backend lo procesa e indexa.
 * @param {File} file
 */
export async function handleUpload(file) {
  const looksLikePdf = file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf');
  if (!looksLikePdf) {
    showToast('Solo se permiten archivos PDF.', 'error');
    return;
  }

  const tempId = `pending-${Date.now()}`;
  addPendingDocument({ document_id: tempId, filename: file.name, isPending: true });

  try {
    const record = await uploadDocument(file);
    replacePendingDocument(tempId, record);
    showToast(`"${record.filename}" se cargó e indexó correctamente.`, 'success');
  } catch (error) {
    removeDocument(tempId);
    showToast(error.message || 'No se pudo subir el documento.', 'error');
  }
}
