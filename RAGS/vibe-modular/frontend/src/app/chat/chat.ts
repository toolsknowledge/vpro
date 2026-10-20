import { DecimalPipe } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

import { SourceReference } from '../models/api.models';
import { RagApiService, apiErrorMessage } from '../services/rag-api.service';

export const MAX_QUESTION_LENGTH = 2000;

interface ChatExchange {
  question: string;
  answer?: string;
  sources: SourceReference[];
  error?: string;
}

@Component({
  selector: 'app-chat',
  imports: [ReactiveFormsModule, DecimalPipe],
  templateUrl: './chat.html',
  styleUrl: './chat.css',
})
export class Chat {
  private readonly api = inject(RagApiService);

  protected readonly maxLength = MAX_QUESTION_LENGTH;
  protected readonly form = new FormGroup({
    question: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required, Validators.maxLength(MAX_QUESTION_LENGTH), Validators.pattern(/\S/)],
    }),
  });
  protected readonly exchanges = signal<ChatExchange[]>([]);
  protected readonly pending = signal(false);

  protected submit(): void {
    if (this.form.invalid || this.pending()) {
      return;
    }
    const question = this.form.controls.question.value.trim();
    const index = this.exchanges().length;
    this.exchanges.update((exchanges) => [...exchanges, { question, sources: [] }]);
    this.form.reset();
    this.pending.set(true);

    this.api.ask(question).subscribe({
      next: (response) => this.updateExchange(index, { answer: response.answer, sources: response.sources }),
      error: (error) => this.updateExchange(index, { error: apiErrorMessage(error) }),
    });
  }

  private updateExchange(index: number, changes: Partial<ChatExchange>): void {
    this.exchanges.update((exchanges) =>
      exchanges.map((exchange, i) => (i === index ? { ...exchange, ...changes } : exchange)),
    );
    this.pending.set(false);
  }
}
