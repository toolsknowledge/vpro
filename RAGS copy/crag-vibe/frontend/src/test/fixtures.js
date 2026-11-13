// Response shapes copied from the real FastAPI /api/chat schema.

const chunk = (overrides) => ({
  chunk_id: 'python_learning_guide-p6-c0',
  document_name: 'python_learning_guide.pdf',
  page_number: 6,
  text: 'A tuple is an ordered collection like a list, but it is immutable.',
  similarity: 0.71,
  relevance: 'relevant',
  reason: 'Explains the difference.',
  attempt: 0,
  query: 'What is the difference between List and Tuple?',
  ...overrides,
})

const attempt = (overrides) => ({
  attempt_number: 0,
  query: 'What is the difference between List and Tuple?',
  rewrite_reason: null,
  relevant_count: 1,
  partially_relevant_count: 0,
  irrelevant_count: 0,
  sufficient: true,
  evaluation_summary: 'The chunk explains the difference.',
  ...overrides,
})

export const relevantResponse = {
  question: 'What is the difference between List and Tuple?',
  answer: 'A **list** is mutable, a **tuple** is immutable (Page 6).\n\n```python\npoint = (10, 20)\n```',
  retrieval_status: 'relevant',
  corrective_retrieval_used: false,
  correction_attempts: 0,
  sources: [
    {
      chunk_id: 'python_learning_guide-p6-c0',
      document_name: 'python_learning_guide.pdf',
      page_number: 6,
      relevance: 'relevant',
      snippet: 'A tuple is an ordered collection like a list, but it is immutable.',
    },
  ],
  retrieved_documents: [chunk()],
  attempts: [attempt()],
}

export const correctedResponse = {
  ...relevantResponse,
  question: 'What is OOPS?',
  answer: 'OOP organises code around objects (Page 10).',
  retrieval_status: 'corrected',
  corrective_retrieval_used: true,
  correction_attempts: 1,
  retrieved_documents: [
    chunk({ relevance: 'partially_relevant', query: 'What is OOPS?' }),
    chunk({ chunk_id: 'python_learning_guide-p10-c0', page_number: 10, attempt: 1, query: 'object-oriented programming classes objects' }),
  ],
  attempts: [
    attempt({ query: 'What is OOPS?', relevant_count: 0, partially_relevant_count: 1, sufficient: false, evaluation_summary: 'Only partly covered.' }),
    attempt({ attempt_number: 1, query: 'object-oriented programming classes objects', rewrite_reason: 'Expanded the abbreviation OOPS.' }),
  ],
}

export const insufficientResponse = {
  question: 'Who won the FIFA World Cup in 2022?',
  answer:
    'I could not find sufficient information in the available learning materials to answer this question accurately. Please try rephrasing your question or consult your trainer.',
  retrieval_status: 'insufficient',
  corrective_retrieval_used: true,
  correction_attempts: 2,
  sources: [],
  retrieved_documents: [chunk({ relevance: 'irrelevant' })],
  attempts: [
    attempt({ relevant_count: 0, irrelevant_count: 5, sufficient: false }),
    attempt({ attempt_number: 1, query: 'FIFA World Cup 2022 winner', relevant_count: 0, irrelevant_count: 5, sufficient: false }),
    attempt({ attempt_number: 2, query: 'FIFA champion 2022', relevant_count: 0, irrelevant_count: 5, sufficient: false }),
  ],
}

export const knowledgeBase = {
  documents: [
    { document_name: 'python_learning_guide.pdf', size_kb: 24.6, page_count: 11, indexed_chunks: 25, indexed: true },
  ],
  total_chunks: 25,
}
