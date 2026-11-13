import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  timeout: 15000,
})

// Corrective RAG can make several OpenAI calls (evaluate, rewrite, retrieve again, answer).
const CHAT_TIMEOUT_MS = 120000

export async function fetchHealth() {
  const { data } = await apiClient.get('/health', { timeout: 5000 })
  return data
}

export async function fetchDocuments() {
  const { data } = await apiClient.get('/documents')
  return data
}

export async function ingestDocuments() {
  const { data } = await apiClient.post('/documents/ingest', null, { timeout: CHAT_TIMEOUT_MS })
  return data
}

export async function askQuestion(question) {
  const { data } = await apiClient.post('/chat', { question }, { timeout: CHAT_TIMEOUT_MS })
  const isValid =
    data &&
    typeof data.answer === 'string' &&
    typeof data.retrieval_status === 'string' &&
    Array.isArray(data.sources) &&
    Array.isArray(data.retrieved_documents) &&
    Array.isArray(data.attempts)
  if (!isValid) {
    throw new Error('INVALID_RESPONSE')
  }
  return data
}

/** Turn any request failure into a short message a student can understand. */
export function getErrorMessage(error) {
  if (error?.message === 'INVALID_RESPONSE') {
    return 'The server sent an unexpected response. Please try again.'
  }
  if (error?.code === 'ECONNABORTED') {
    return 'The request took too long. Please try again in a moment.'
  }
  if (!error?.response) {
    return 'Cannot connect to the learning assistant server. Please make sure the backend is running.'
  }
  const detail = error.response.data?.detail
  return typeof detail === 'string' ? detail : 'Something went wrong. Please try again.'
}
