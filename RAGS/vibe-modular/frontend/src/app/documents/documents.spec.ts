import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';

import { environment } from '../../environments/environment';
import { DocumentInfo } from '../models/api.models';
import { Documents } from './documents';

const GUIDE: DocumentInfo = {
  document_id: 'abc',
  filename: 'guide.docx',
  chunk_count: 3,
  uploaded_at: '2026-01-01T10:00:00+00:00',
  title: null,
  author: null,
};

describe('Documents', () => {
  let fixture: ComponentFixture<Documents>;
  let http: HttpTestingController;
  let element: HTMLElement;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Documents],
      providers: [provideHttpClient(), provideHttpClientTesting()],
    }).compileComponents();
    fixture = TestBed.createComponent(Documents);
    http = TestBed.inject(HttpTestingController);
    element = fixture.nativeElement;
    fixture.detectChanges();
  });

  afterEach(() => http.verify());

  async function flushList(documents: DocumentInfo[]): Promise<void> {
    http.expectOne(`${environment.apiUrl}/documents`).flush({ documents });
    await fixture.whenStable();
  }

  it('lists indexed documents', async () => {
    await flushList([GUIDE]);
    expect(element.textContent).toContain('guide.docx');
    expect(element.textContent).toContain('3 chunks');
  });

  it('shows an empty state', async () => {
    await flushList([]);
    expect(element.textContent).toContain('No documents indexed yet.');
  });

  it('uploads the selected file and refreshes the list', async () => {
    await flushList([]);
    const input = element.querySelector<HTMLInputElement>('input[type=file]')!;
    const file = new File(['docx'], 'guide.docx');
    Object.defineProperty(input, 'files', { value: [file] });
    input.dispatchEvent(new Event('change'));
    await fixture.whenStable();

    element.querySelector<HTMLButtonElement>('.upload button')!.click();
    http.expectOne(`${environment.apiUrl}/documents/upload`).flush(GUIDE, { status: 201, statusText: 'Created' });
    await flushList([GUIDE]);

    expect(element.textContent).toContain('Indexed guide.docx (3 chunks).');
    expect(element.textContent).toContain('guide.docx');
  });

  it('deletes a document after confirmation', async () => {
    vi.spyOn(window, 'confirm').mockReturnValue(true);
    await flushList([GUIDE]);

    element.querySelector<HTMLButtonElement>('button.danger')!.click();
    http.expectOne({ method: 'DELETE', url: `${environment.apiUrl}/documents/abc` }).flush(null);
    await fixture.whenStable();

    expect(element.textContent).toContain('No documents indexed yet.');
  });
});
