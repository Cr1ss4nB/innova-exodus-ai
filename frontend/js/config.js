// URL base del backend. Cambiar aqui al desplegar (por ejemplo, la IP/dominio de OCI).
export const API_BASE_URL = 'http://localhost:8000';

export const API_ROUTES = {
  health: `${API_BASE_URL}/api/v1/health`,
  documents: `${API_BASE_URL}/api/v1/documents`,
  chat: `${API_BASE_URL}/api/v1/chat`,
};
