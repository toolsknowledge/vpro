export interface DocumentInfo {
  document_id: string;
  filename: string;
  chunk_count: number;
  uploaded_at: string;
  title: string | null;
  author: string | null;
}

export interface DocumentListResponse {
  documents: DocumentInfo[];
}

export interface ChatRequest {
  question: string;
}

export interface SourceReference {
  document_id: string;
  filename: string;
  chunk_index: number;
  score: number;
  text: string;
}

export interface ChatResponse {
  answer: string;
  sources: SourceReference[];
}

export interface ApiErrorResponse {
  error: {
    code: string;
    message: string;
  };
}
