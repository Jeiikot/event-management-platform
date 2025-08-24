export function parseError(error) {
  const data = error?.response?.data;

  if (Array.isArray(data?.detail)) {
    const msg = data.detail
      .map((e) => e?.msg || e?.message || '')
      .filter(Boolean)
      .join(' | ');
    if (msg) return msg;
  }
  if (typeof data?.detail === 'string') return data.detail;
  if (data?.detail && typeof data.detail === 'object') {
    const values = Object.values(data.detail).filter(Boolean);
    if (values.length) return values.join(' | ');
  }
  if (typeof data === 'string') return data;
  if (error?.message) return error.message;

  const status = error?.response?.status;
  if (status === 401) return 'No autorizado';
  if (status === 403) return 'Prohibido';
  if (status === 404) return 'Recurso no encontrado';
  if (status === 409) return 'Conflicto';
  if (status >= 500) return 'Error interno del servidor';

  return 'Error inesperado';
}
