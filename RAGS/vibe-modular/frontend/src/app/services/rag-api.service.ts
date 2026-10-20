import { HttpClient, HttpErrorResponse, HttpEvent } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, map } from 'rxjs';

import { environment } from '../../environments/environment';
import {
  ApiErrorResponse,
  ChatRequest,
  ChatResponse,
  DocumentInfo,
  DocumentListResponse,
} from '../models/api.models';

@Injectable({ providedIn: 'root' })
export class RagApiService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = environment.apiUrl;

  listDocuments(): Observable<DocumentInfo[]> {
    return this.http
      .get<DocumentListResponse>(`${this.baseUrl}/documents`)
      .pipe(map((response) => response.documents));
  }

  /** Emits progress events while the file uploads, then the indexed document. */
  uploadDocument(file: File): Observable<HttpEvent<DocumentInfo>> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<DocumentInfo>(`${this.baseUrl}/documents/upload`, formData, {
      observe: 'events',
      reportProgress: true,
    });
  }

  deleteDocument(documentId: string): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/documents/${encodeURIComponent(documentId)}`);
  }

  ask(question: string): Observable<ChatResponse> {
    const body: ChatRequest = { question };
    return this.http.post<ChatResponse>(`${this.baseUrl}/chat`, body);
  }
}

/** Turn an HTTP failure into a message suitable for display. */
export function apiErrorMessage(error: unknown): string {
  if (!(error instanceof HttpErrorResponse)) {
    return 'An unexpected error occurred.';
  }
  if (error.status === 0) {
    return 'Cannot reach the backend. Check that the FastAPI server is running.';
  }
  const body = error.error as Partial<ApiErrorResponse> | null;
  return body?.error?.message ?? `Request failed with status ${error.status}.`;
}
