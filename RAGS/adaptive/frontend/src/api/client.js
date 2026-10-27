// Single HTTP client for the backend. Every request goes through `request`.

export const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000').replace(/\/+$/, '');

export class ApiError extends Error {
  constructor(message, { status = 0, code = 'unknown_error' } = {}) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.code = code;
  }

  get retryable() {
    return this.status === 0 || this.status === 429 || this.status >= 500;
  }
}

async function request(path, { method = 'GET', body, signal } = {}) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      method,
      signal,
      headers: body === undefined ? undefined : { 'Content-Type': 'application/json' },
      body: body === undefined ? undefined : JSON.stringify(body),
    });
  } catch (error) {
    if (error.name === 'AbortError') throw error;
    throw new ApiError(`Cannot reach the backend at ${API_BASE_URL}. Make sure the API server is running.`, {
      code: 'backend_offline',
    });
  }

  if (response.status === 204) return null;

  let payload = null;
  try {
    payload = await response.json();
  } catch {
    // Non-JSON body (e.g. a proxy error page); handled below.
  }

  if (!response.ok) {
    const detail = payload?.error;
    throw new ApiError(detail?.message || `Request failed with HTTP ${response.status}.`, {
      status: response.status,
      code: detail?.code || 'http_error',
    });
  }
  if (payload === null) {
    throw new ApiError('The backend returned an unreadable response.', { status: response.status, code: 'bad_response' });
  }
  return payload;
}

export const api = {
  health: (signal) => request('/api/health', { signal }),
  indexingStatus: (signal) => request('/api/indexing/status', { signal }),
  documents: (signal) => request('/api/documents', { signal }),
  sampleQuestions: (signal) => request('/api/sample-questions', { signal }),
  indexDocuments: () => request('/api/indexing/index', { method: 'POST' }),
  reindexDocuments: () => request('/api/indexing/reindex', { method: 'POST' }),
  chat: ({ question, sessionId }, signal) =>
    request('/api/chat', { method: 'POST', body: { question, session_id: sessionId }, signal }),
  clearSession: (sessionId) => request(`/api/chat/sessions/${encodeURIComponent(sessionId)}`, { method: 'DELETE' }),
};
