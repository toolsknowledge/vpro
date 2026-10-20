import { DatePipe } from '@angular/common';
import { HttpEventType } from '@angular/common/http';
import { Component, OnInit, computed, inject, signal } from '@angular/core';

import { DocumentInfo } from '../models/api.models';
import { RagApiService, apiErrorMessage } from '../services/rag-api.service';

type UploadStatus =
  | { kind: 'idle' }
  | { kind: 'uploading'; percent: number }
  | { kind: 'indexing' }
  | { kind: 'success'; message: string }
  | { kind: 'error'; message: string };

@Component({
  selector: 'app-documents',
  imports: [DatePipe],
  templateUrl: './documents.html',
  styleUrl: './documents.css',
})
export class Documents implements OnInit {
  private readonly api = inject(RagApiService);

  protected readonly documents = signal<DocumentInfo[]>([]);
  protected readonly loading = signal(false);
  protected readonly listError = signal<string | null>(null);
  protected readonly selectedFile = signal<File | null>(null);
  protected readonly uploadStatus = signal<UploadStatus>({ kind: 'idle' });
  protected readonly deletingId = signal<string | null>(null);

  protected readonly isBusy = computed(() => ['uploading', 'indexing'].includes(this.uploadStatus().kind));

  protected readonly statusMessage = computed<{ text: string; tone: 'info' | 'success' | 'error' } | null>(() => {
    const status = this.uploadStatus();
    switch (status.kind) {
      case 'idle':
        return null;
      case 'uploading':
        return { text: `Uploading… ${status.percent}%`, tone: 'info' };
      case 'indexing':
        return { text: 'Indexing document…', tone: 'info' };
      case 'success':
        return { text: status.message, tone: 'success' };
      case 'error':
        return { text: status.message, tone: 'error' };
    }
  });

  ngOnInit(): void {
    this.refresh();
  }

  protected refresh(): void {
    this.loading.set(true);
    this.listError.set(null);
    this.api.listDocuments().subscribe({
      next: (documents) => {
        this.documents.set(documents);
        this.loading.set(false);
      },
      error: (error) => {
        this.listError.set(apiErrorMessage(error));
        this.loading.set(false);
      },
    });
  }

  protected onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.selectedFile.set(input.files?.[0] ?? null);
    this.uploadStatus.set({ kind: 'idle' });
  }

  protected upload(fileInput: HTMLInputElement): void {
    const file = this.selectedFile();
    if (!file) {
      return;
    }
    this.uploadStatus.set({ kind: 'uploading', percent: 0 });
    this.api.uploadDocument(file).subscribe({
      next: (event) => {
        if (event.type === HttpEventType.UploadProgress) {
          const percent = event.total ? Math.round((100 * event.loaded) / event.total) : 0;
          // Once the bytes are sent, the server is extracting, chunking and embedding.
          this.uploadStatus.set(percent < 100 ? { kind: 'uploading', percent } : { kind: 'indexing' });
        } else if (event.type === HttpEventType.Response && event.body) {
          const { filename, chunk_count } = event.body;
          this.uploadStatus.set({ kind: 'success', message: `Indexed ${filename} (${chunk_count} chunks).` });
          this.selectedFile.set(null);
          fileInput.value = '';
          this.refresh();
        }
      },
      error: (error) => this.uploadStatus.set({ kind: 'error', message: apiErrorMessage(error) }),
    });
  }

  protected remove(document: DocumentInfo): void {
    if (!confirm(`Delete "${document.filename}" and all of its indexed chunks?`)) {
      return;
    }
    this.deletingId.set(document.document_id);
    this.listError.set(null);
    this.api.deleteDocument(document.document_id).subscribe({
      next: () => {
        this.deletingId.set(null);
        this.documents.update((documents) => documents.filter((d) => d.document_id !== document.document_id));
      },
      error: (error) => {
        this.deletingId.set(null);
        this.listError.set(apiErrorMessage(error));
      },
    });
  }
}
