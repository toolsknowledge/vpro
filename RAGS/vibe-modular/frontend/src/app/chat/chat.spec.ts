import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';

import { environment } from '../../environments/environment';
import { Chat } from './chat';

describe('Chat', () => {
  let fixture: ComponentFixture<Chat>;
  let http: HttpTestingController;
  let element: HTMLElement;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Chat],
      providers: [provideHttpClient(), provideHttpClientTesting()],
    }).compileComponents();
    fixture = TestBed.createComponent(Chat);
    http = TestBed.inject(HttpTestingController);
    element = fixture.nativeElement;
    await fixture.whenStable();
  });

  afterEach(() => http.verify());

  async function ask(question: string): Promise<void> {
    const textarea = element.querySelector('textarea')!;
    textarea.value = question;
    textarea.dispatchEvent(new Event('input'));
    element.querySelector('form')!.dispatchEvent(new Event('submit'));
    await fixture.whenStable();
  }

  it('disables the ask button for blank questions', async () => {
    await ask('   ');
    expect(element.querySelector<HTMLButtonElement>('button[type=submit]')!.disabled).toBe(true);
    http.expectNone(`${environment.apiUrl}/chat`);
  });

  it('shows the answer and its sources', async () => {
    await ask('Where do orders ship from?');
    expect(element.textContent).toContain('Thinking…');

    http.expectOne(`${environment.apiUrl}/chat`).flush({
      answer: 'From Berlin.',
      sources: [{ document_id: 'a', filename: 'guide.docx', chunk_index: 0, score: 0.8123, text: 'Berlin warehouse' }],
    });
    await fixture.whenStable();

    expect(element.textContent).toContain('From Berlin.');
    expect(element.textContent).toContain('guide.docx · chunk 1 · score 0.81');
    expect(element.textContent).toContain('Berlin warehouse');
  });

  it('shows API errors and keeps earlier exchanges', async () => {
    await ask('First?');
    http.expectOne(`${environment.apiUrl}/chat`).flush({ answer: 'One.', sources: [] });
    await fixture.whenStable();

    await ask('Second?');
    http
      .expectOne(`${environment.apiUrl}/chat`)
      .flush({ error: { code: 'llm_error', message: 'The language model request failed.' } }, {
        status: 502,
        statusText: 'Bad Gateway',
      });
    await fixture.whenStable();

    expect(element.textContent).toContain('One.');
    expect(element.querySelector('[role=alert]')!.textContent).toContain('The language model request failed.');
  });
});
