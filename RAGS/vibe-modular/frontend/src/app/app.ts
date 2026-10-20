import { Component } from '@angular/core';

import { Chat } from './chat/chat';
import { Documents } from './documents/documents';

@Component({
  selector: 'app-root',
  imports: [Chat, Documents],
  template: `
    <header>
      <h1>RAGS Vibe Modular</h1>
      <p class="muted">Upload DOCX documents and ask questions answered from their content.</p>
    </header>
    <main>
      <app-documents />
      <app-chat />
    </main>
  `,
  styles: `
    main {
      display: grid;
      grid-template-columns: minmax(280px, 1fr) 2fr;
      gap: 1.5rem;
      align-items: start;
    }

    @media (max-width: 800px) {
      main {
        grid-template-columns: 1fr;
      }
    }
  `,
})
export class App {}
