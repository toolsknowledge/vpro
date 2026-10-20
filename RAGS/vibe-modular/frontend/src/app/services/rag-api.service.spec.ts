import { HttpErrorResponse, provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { environment } from '../../environments/environment';
import { RagApiService, apiErrorMessage } from './rag-api.service';

describe('RagApiService', () => {
  let service: RagApiService;
  let http: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({ providers: [provideHttpClient(), provideHttpClientTesting()] });
    service = TestBed.inject(RagApiService);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('lists documents from the configured API URL', () => {
    let filenames: string[] = [];
    service.listDocuments().subscribe((documents) => (filenames = documents.map((d) => d.filename)));

    http.expectOne(`${environment.apiUrl}/documents`).flush({
      documents: [
        { document_id: 'a', filename: 'guide.docx', chunk_count: 2, uploaded_at: '', title: null, author: null },
      ],
    });

    expect(filenames).toEqual(['guide.docx']);
  });

  it('uploads the file as multipart form data', () => {
    const file = new File(['content'], 'guide.docx');
    service.uploadDocument(file).subscribe();

    const request = http.expectOne(`${environment.apiUrl}/documents/upload`);
    expect(request.request.method).toBe('POST');
    expect((request.request.body as FormData).get('file')).toBe(file);
    request.flush({});
  });

  it('deletes a document by encoded id', () => {
    service.deleteDocument('a/b').subscribe();
    const request = http.expectOne(`${environment.apiUrl}/documents/a%2Fb`);
    expect(request.request.method).toBe('DELETE');
    request.flush(null);
  });

  it('posts the question to the chat endpoint', () => {
    service.ask('What is covered?').subscribe();
    const request = http.expectOne(`${environment.apiUrl}/chat`);
    expect(request.request.body).toEqual({ question: 'What is covered?' });
    request.flush({ answer: 'Everything.', sources: [] });
  });
});

describe('apiErrorMessage', () => {
  it('uses the backend error message', () => {
    const error = new HttpErrorResponse({ status: 409, error: { error: { code: 'x', message: 'Already indexed.' } } });
    expect(apiErrorMessage(error)).toBe('Already indexed.');
  });

  it('explains when the backend is unreachable', () => {
    expect(apiErrorMessage(new HttpErrorResponse({ status: 0 }))).toContain('Cannot reach the backend');
  });

  it('falls back to the status code', () => {
    expect(apiErrorMessage(new HttpErrorResponse({ status: 500, error: 'oops' }))).toBe(
      'Request failed with status 500.',
    );
  });
});
