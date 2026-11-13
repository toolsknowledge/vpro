/**
 * Builds the "How Corrective RAG Works" stages from a real /api/chat response.
 * Nothing here is invented: every status and detail comes from the backend data.
 */

export const RELEVANCE_LABELS = {
  relevant: 'Relevant',
  partially_relevant: 'Partially Relevant',
  irrelevant: 'Irrelevant',
}

export const STATUS_LABELS = {
  completed: 'Completed',
  in_progress: 'In Progress',
  corrected: 'Corrected',
  failed: 'Failed',
  skipped: 'Not Needed',
  pending: 'Waiting',
}

export const RETRIEVAL_STATUS_INFO = {
  relevant: { label: 'Relevant', tone: 'success', text: 'Answered from the first retrieval.' },
  corrected: { label: 'Corrected', tone: 'corrected', text: 'Answered after corrective retrieval.' },
  insufficient: { label: 'Insufficient', tone: 'danger', text: 'Not enough information in the materials.' },
}

const STAGES = [
  ['Question Received', 'Your question is sent to the FastAPI backend and validated.'],
  ['Query Processing', 'The question is converted into an embedding (a list of numbers) with OpenAI.'],
  ['Initial Document Retrieval', 'ChromaDB finds the 5 chunks of the PDF whose embeddings are most similar.'],
  ['Relevance Evaluation', 'The LLM grades each chunk as Relevant, Partially Relevant or Irrelevant.'],
  ['Corrective Retrieval', 'If no chunk is relevant, the query is rewritten and ChromaDB is searched again.'],
  ['Final Answer Generation', 'The LLM writes an answer using only the relevant chunks, with page references.'],
]

function stage(index, status, details = []) {
  const [name, explanation] = STAGES[index]
  return { name, explanation, status, details }
}

function pluralize(count, word) {
  return `${count} ${word}${count === 1 ? '' : 's'}`
}

function gradeSummary(attempt) {
  return `${attempt.relevant_count} relevant · ${attempt.partially_relevant_count} partial · ${attempt.irrelevant_count} irrelevant`
}

/** Stages shown before any question is asked. */
export function buildIdleStages() {
  return STAGES.map((_, index) => stage(index, 'pending'))
}

/** Stages shown while the backend is working on a question. */
export function buildLoadingStages(question) {
  return STAGES.map((_, index) => {
    if (index === 0) return stage(0, 'completed', [`“${question}”`])
    if (index === 1) return stage(1, 'in_progress', ['The backend is retrieving, evaluating and correcting…'])
    return stage(index, 'pending')
  })
}

/** Stages for a finished response. */
export function buildWorkflowStages(response) {
  const [initial, ...corrections] = response.attempts
  const initialDocuments = response.retrieved_documents.filter((doc) => doc.attempt === 0)
  const pages = [...new Set(initialDocuments.map((doc) => doc.page_number))].sort((a, b) => a - b)
  const answered = response.retrieval_status !== 'insufficient'

  let correctionStage
  if (!response.corrective_retrieval_used) {
    correctionStage = stage(4, 'skipped', ['Initial retrieval was relevant. No correction was required.'])
  } else {
    correctionStage = stage(
      4,
      corrections.some((attempt) => attempt.sufficient) ? 'corrected' : 'failed',
      corrections.map(
        (attempt) =>
          `Attempt ${attempt.attempt_number}: “${attempt.query}” → ${attempt.sufficient ? 'relevant context found' : 'still not relevant'} (${gradeSummary(attempt)})`,
      ),
    )
  }

  return [
    stage(0, 'completed', [`“${response.question}”`]),
    stage(1, 'completed', ['Question validated and embedded with the OpenAI embedding model.']),
    stage(2, 'completed', [
      `${pluralize(initialDocuments.length, 'chunk')} retrieved from ChromaDB`,
      pages.length ? `Pages: ${pages.join(', ')}` : 'No pages found',
    ]),
    stage(3, initial?.sufficient ? 'completed' : 'failed', [
      initial ? gradeSummary(initial) : 'No evaluation available',
      initial?.evaluation_summary,
    ].filter(Boolean)),
    correctionStage,
    stage(5, answered ? 'completed' : 'failed', [
      answered
        ? `Answer generated from ${pluralize(response.sources.length, 'source chunk')}.`
        : 'Not enough supporting information – a safe response was returned instead of guessing.',
    ]),
  ]
}
