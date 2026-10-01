const BASE_URL = import.meta.env.VITE_API_URL || '/api'
const TOKEN_KEY = 'vpro_token'

export const tokenStore = {
  get: () => localStorage.getItem(TOKEN_KEY),
  set: (token) => localStorage.setItem(TOKEN_KEY, token),
  clear: () => localStorage.removeItem(TOKEN_KEY),
}

// Called when the API rejects the token, so the auth context can log the user out.
let onUnauthorized = () => {}
export const setUnauthorizedHandler = (fn) => {
  onUnauthorized = fn
}

export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.status = status
  }
}

// FastAPI returns { detail: "..." } for HTTPException and { detail: [{ msg, loc }] } for validation errors.
function extractMessage(body, status) {
  const detail = body?.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail) && detail.length) {
    return detail.map((d) => `${d.loc?.slice(-1)[0] ?? 'field'}: ${d.msg}`).join(', ')
  }
  return body?.message || `Request failed (${status})`
}

async function request(path, { method = 'GET', body, auth = true } = {}) {
  const headers = { 'Content-Type': 'application/json' }
  const token = tokenStore.get()
  if (auth && token) headers.Authorization = `Bearer ${token}`

  let res
  try {
    res = await fetch(`${BASE_URL}${path}`, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined,
    })
  } catch {
    throw new ApiError('Cannot reach the server. Is FastAPI running?', 0)
  }

  const data = await res.json().catch(() => null)

  if (!res.ok) {
    if (auth && (res.status === 401 || res.status === 403)) onUnauthorized()
    throw new ApiError(extractMessage(data, res.status), res.status)
  }
  return data
}

export const authApi = {
  register: (username, password) =>
    request('/register', { method: 'POST', body: { username, password }, auth: false }),
  login: (username, password) =>
    request('/login', { method: 'POST', body: { username, password }, auth: false }),
}

export const studentsApi = {
  list: () => request('/students'),
  get: (id) => request(`/students/${id}`),
  create: (student) => request('/students', { method: 'POST', body: student }),
  update: (id, student) => request(`/students/${id}`, { method: 'PUT', body: student }),
  remove: (id) => request(`/students/${id}`, { method: 'DELETE' }),
}
