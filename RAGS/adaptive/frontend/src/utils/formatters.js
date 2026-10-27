export function formatBytes(bytes) {
  if (bytes === null || bytes === undefined) return '—';
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function formatScore(score) {
  return typeof score === 'number' ? score.toFixed(2) : '—';
}

export function formatDateTime(value) {
  if (!value) return '—';
  const date = new Date(value);
  return Number.isNaN(date.getTime())
    ? '—'
    : date.toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' });
}

export function formatDuration(seconds) {
  if (typeof seconds !== 'number') return '—';
  return seconds < 1 ? `${Math.round(seconds * 1000)} ms` : `${seconds.toFixed(1)} s`;
}

export function formatStatus(status) {
  if (!status) return '—';
  const text = status.replace(/_/g, ' ');
  return text.charAt(0).toUpperCase() + text.slice(1);
}

export function pluralize(count, singular, plural = `${singular}s`) {
  return `${count} ${count === 1 ? singular : plural}`;
}

export function chunkLocation(source) {
  const parts = [];
  if (source.page != null) parts.push(`Page ${source.page}`);
  if (source.sheet) parts.push(`Sheet “${source.sheet}”`);
  if (source.row != null) parts.push(`Row ${source.row}`);
  if (source.chunk_index != null && source.total_chunks != null) {
    parts.push(`Chunk ${source.chunk_index + 1} of ${source.total_chunks}`);
  }
  return parts.join(' · ');
}

export function createSessionId() {
  if (globalThis.crypto?.randomUUID) return globalThis.crypto.randomUUID();
  return `s-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 12)}`;
}
