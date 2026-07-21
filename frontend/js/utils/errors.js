export class ApiRequestError extends Error {
  constructor(message, status, errorType) {
    super(message);
    this.name = 'ApiRequestError';
    this.status = status;
    this.errorType = errorType;
  }
}

/**
 * Convierte la respuesta de error del backend en un mensaje legible.
 * Soporta tanto el envelope propio ({detail, error_type}) como el formato
 * por defecto de FastAPI para errores 422 de validacion ({detail: [...]}).
 * @param {Response} response
 * @returns {Promise<ApiRequestError>}
 */
export async function toApiError(response) {
  let body = null;
  try {
    body = await response.json();
  } catch {
    body = null;
  }

  if (body && typeof body.detail === 'string') {
    return new ApiRequestError(body.detail, response.status, body.error_type);
  }

  if (body && Array.isArray(body.detail) && body.detail.length > 0) {
    const first = body.detail[0];
    const message = typeof first === 'string' ? first : first.msg || 'La solicitud no es válida.';
    return new ApiRequestError(message, response.status, 'ValidationError');
  }

  if (response.status === 404) {
    return new ApiRequestError('No se encontró el recurso solicitado.', response.status);
  }

  if (response.status >= 500) {
    return new ApiRequestError('El servidor no pudo procesar la solicitud. Intenta nuevamente.', response.status);
  }

  return new ApiRequestError('Ocurrió un error inesperado. Intenta nuevamente.', response.status);
}
