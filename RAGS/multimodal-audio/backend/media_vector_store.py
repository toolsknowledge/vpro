"""The three ChromaDB collections that hold media knowledge.

    vpro_document_knowledge  (existing)  PDF / Excel / Word / TXT chunks
    vpro_audio_transcripts               transcript chunks of audio uploads
    vpro_video_transcripts               transcript chunks of the audio track of videos
    vpro_video_frames                    text descriptions of selected video keyframes

All four use the same embedding model, so one question vector can be compared
with every collection. Each collection still checks that it never receives
vectors from a different model or dimension (see VectorStore.check_compatible).
"""

from __future__ import annotations

from pathlib import Path

from backend.transcript_chunker import MEDIA_AUDIO, MEDIA_VIDEO_FRAME, MEDIA_VIDEO_TRANSCRIPT
from backend.vector_store import VectorStore

MEDIA_TYPES = (MEDIA_AUDIO, MEDIA_VIDEO_TRANSCRIPT, MEDIA_VIDEO_FRAME)


class MediaStores:
    def __init__(self, persist_directory: Path, audio_collection: str, video_transcript_collection: str, frame_collection: str):
        self.stores: dict[str, VectorStore] = {
            MEDIA_AUDIO: VectorStore(persist_directory, audio_collection),
            MEDIA_VIDEO_TRANSCRIPT: VectorStore(persist_directory, video_transcript_collection),
            MEDIA_VIDEO_FRAME: VectorStore(persist_directory, frame_collection),
        }

    def __getitem__(self, media_type: str) -> VectorStore:
        return self.stores[media_type]

    def items(self):
        return self.stores.items()

    def counts(self) -> dict[str, int]:
        return {media_type: store.count() for media_type, store in self.stores.items()}

    def total(self) -> int:
        return sum(self.counts().values())

    def count_for_document(self, document_id: str) -> dict[str, int]:
        return {media_type: store.count_for_document(document_id) for media_type, store in self.stores.items()}

    def check_compatible(self, embedding_model: str) -> None:
        for store in self.stores.values():
            store.check_compatible(embedding_model)

    def replace(self, media_type: str, document_id: str, ids, texts, metadatas, embeddings, embedding_model: str) -> int:
        """Swap one media file's records in one collection; old records are restored on failure."""
        store = self.stores[media_type]
        store.replace_document(document_id, ids, texts, metadatas, embeddings, embedding_model)
        return store.count_for_document(document_id)

    def delete_media(self, document_id: str) -> int:
        return sum(store.delete_document(document_id) for store in self.stores.values())
