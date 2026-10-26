# Master Prompt: Build Audio & Video RAG Application Using OpenAI + ChromaDB

## 1. Role

Act as a Senior AI Engineer, Python Developer, Multimodal RAG Architect, and UI/UX Engineer.

Extend my existing VPro Skills EduTech document-based RAG application into a complete **Audio and Video RAG Assistant**.

The existing application already supports PDF, Excel, Word, and TXT files. Preserve all existing functionality and add audio/video ingestion without breaking the current implementation.

The application must help students upload recorded classes, meetings, tutorials, and educational videos, then ask questions and receive answers grounded in the actual media content.

## 2. Technology Stack

Use:

- Python 3.11 or compatible version
- Streamlit for the UI
- OpenAI API for speech transcription, embeddings, and LLM responses
- ChromaDB for persistent vector storage
- FFmpeg for audio/video processing
- `openai` Python SDK
- `python-dotenv`
- `pydantic` where useful
- `pytest` for testing

Use the existing project's architecture and dependencies wherever practical.

Configure all model names, file limits, and processing settings using environment variables.

Do not hardcode API keys.

## 3. Supported Media Files

Support these file formats where the underlying decoder and installed FFmpeg build allow them:

**Audio**
- `.mp3`
- `.wav`
- `.m4a`
- `.aac`
- `.ogg`
- `.flac`
- `.webm`

**Video**
- `.mp4`
- `.mov`
- `.mkv`
- `.avi`
- `.webm`

Validate actual file content where practical, not just the filename extension.

Provide clear errors for unsupported codecs, corrupted files, empty files, and media with no detectable audio track.

Configure maximum upload size, maximum duration, and processing limits. Do not load large media files entirely into memory unnecessarily.

## 4. Audio RAG — Complete Processing Pipeline

Implement the following workflow.

### Step 1: Upload Audio

Allow users to upload a recording of a lecture, meeting, training session, or tutorial.

Display:

- Filename
- File size
- Duration
- Audio format
- Processing status

Use FFprobe or an equivalent supported FFmpeg utility to inspect the media.

### Step 2: Preprocess Audio

Use FFmpeg to prepare audio for transcription when needed.

- Detect the audio stream.
- Convert incompatible formats to an appropriate supported format.
- Preserve the original recording.
- Split long recordings into manageable segments.
- Avoid cutting off speech where practical.
- Track the start and end timestamps of every segment.

Respect the current transcription endpoint's documented upload and duration limits. Do not assume every model accepts unlimited audio length.

### Step 3: Speech-to-Text Transcription

Use an appropriate OpenAI transcription model configured through `.env`.

Generate transcripts containing the spoken words.

Where supported by the selected API and model, preserve:

- Segment start time
- Segment end time
- Speaker information
- Language information

Do not fabricate speaker labels or word-level timestamps if the selected model does not provide them.

If the API returns only text without timestamps, use a clearly documented fallback strategy or report the missing timestamp capability.

Store the original transcript and the associated media metadata.

### Step 4: Transcript Cleaning

Clean the transcript without changing its meaning.

- Normalize whitespace.
- Preserve technical terminology.
- Preserve important numbers and names.
- Avoid removing meaningful repetitions or spoken explanations.
- Retain timestamps and segment boundaries.
- Record the transcription model used.

Optionally allow users to inspect the raw and cleaned transcript side by side.

### Step 5: Transcript Chunking

Create searchable transcript chunks.

Default configuration:

- Chunk size: approximately 800 tokens
- Overlap: approximately 120 tokens

Make both settings configurable.

Prefer splitting at sentence, utterance, or transcript-segment boundaries.

Each chunk must include:

- `chunk_id`
- `document_id`
- `media_type`
- `source_file`
- `chunk_index`
- `text`
- `start_time_seconds`
- `end_time_seconds`
- `transcript_segment_ids`
- `transcription_model`
- `language`, when known

Ensure that chunks do not combine unrelated recordings.

### Step 6: Generate Embeddings

Use the configured OpenAI embedding model to convert transcript chunks into numerical vectors.

Use the same embedding model and vector dimensions as the existing ChromaDB collection, or create a separate compatible collection if the current architecture requires it.

Store the transcript chunk text and metadata with the vectors.

Display:

- Number of transcript chunks
- Number of embeddings created
- Vector dimension
- Embedding model
- Processing failures

## 5. Video RAG — Complete Processing Pipeline

### Step 1: Upload Video

Accept supported video files.

Extract and display:

- Duration
- Resolution
- Frame rate
- Audio availability
- Video format

Show a video preview if supported by the UI.

### Step 2: Extract Audio From Video

Use FFmpeg to extract the video's audio track.

Pass the extracted audio through the audio transcription pipeline described above.

Every transcript chunk must retain the original video filename and its corresponding timestamp range.

If the video has no audio, do not fail the entire process. Continue with visual processing if a valid video stream exists.

### Step 3: Extract Video Keyframes

Use FFmpeg to extract representative frames at a configurable interval.

Suggested initial interval: one frame every 10 seconds.

Allow the user to adjust the interval before processing.

Also consider scene-change detection as an optional enhancement.

For each frame, record:

- `frame_id`
- `document_id`
- `source_file`
- `timestamp_seconds`
- `frame_path`
- `frame_index`
- `extraction_method`

Do not extract every frame by default because this can consume excessive storage, processing time, and API credits.

Limit the number of frames per video according to configuration.

### Step 4: Analyze Frames

Use a compatible OpenAI vision-capable model to generate a concise description of each selected frame.

Capture useful visual information such as:

- Slide titles
- Visible text
- Diagrams
- Code shown on screen
- Tables
- Charts
- Objects and actions relevant to the lesson

Use OCR or a vision model when appropriate.

Clearly distinguish observed content from uncertain interpretation.

Do not claim that every frame has been analyzed if only selected frames were processed.

Store each frame description alongside its timestamp and source filename.

If frame analysis fails, retain the transcript and continue when possible.

### Step 5: Create Visual Chunks

Convert frame descriptions into searchable text records.

Example:

`Video: Python_Lecture.mp4 | Timestamp: 00:02:10 | Frame description: A slide explains Python list comprehensions with a code example.`

Each visual record should include:

- `chunk_id`
- `document_id`
- `media_type: video_frame`
- `source_file`
- `timestamp_seconds`
- `frame_path` or a safe relative frame reference
- `frame_description`
- `frame_index`

Generate embeddings from the textual frame descriptions.

Do not pretend that text embeddings are image embeddings. The vector represents the generated frame description unless a genuine multimodal embedding model is implemented.

### Step 6: Store Video and Audio Content

Store transcript chunks and visual description chunks in ChromaDB.

Use separate collections or clearly defined metadata filters for audio transcripts, video transcripts, and visual descriptions.

Maintain stable IDs and prevent duplicate records during re-indexing.

The user must be able to find both:

- What the instructor said.
- What appeared on the screen at a given timestamp.

## 6. ChromaDB Architecture

Preserve the existing document collection.

Use compatible collections, for example:

- `vpro_document_knowledge`
- `vpro_audio_transcripts`
- `vpro_video_transcripts`
- `vpro_video_frames`

The exact design may be simplified if the existing project uses another sound architecture.

Use a persistent ChromaDB directory.

Maintain document-level records that allow the application to:

- List indexed media.
- Identify failed processing jobs.
- Remove all records associated with one media file.
- Re-index changed media.
- Preserve the relationship between transcript segments and visual frames.

Never mix incompatible embedding dimensions in one collection.

## 7. Unified Multimodal RAG Question Answering

Extend the existing chat page to search documents, audio transcripts, video transcripts, and visual frame descriptions.

Users should be able to select:

- Search all indexed sources.
- Search documents only.
- Search audio only.
- Search video only.

Example questions:

1. What topics did the instructor explain in the Python lecture?
2. At what time did the instructor explain list comprehensions?
3. Summarize the lecture between 10 and 20 minutes.
4. What did the instructor say about embeddings?
5. Which timestamp shows the slide explaining ChromaDB?
6. What code is visible on the screen at 00:12:30?
7. Compare the instructor's explanation with the displayed slide.
8. Which recorded session discusses RAG evaluation?
9. Summarize all uploaded classes about vector databases.
10. What is shown in the video when the instructor discusses chunk overlap?

### Retrieval Workflow

1. Accept the user question.
2. Generate the query embedding.
3. Search the relevant ChromaDB collections.
4. Retrieve the most relevant transcript and frame-description chunks.
5. Optionally rerank the results.
6. Combine the retrieved content with its source metadata.
7. Build a context-aware prompt.
8. Generate the answer using the configured OpenAI LLM.
9. Return citations and timestamps.
10. Allow users to inspect the supporting chunks.

Support configurable top-K retrieval.

Use appropriate distance handling and filters.

If no useful context is found, tell the user that the indexed content does not provide enough information.

Do not invent timestamps, quotations, or visual details.

### Citation Examples

Audio citation:

`Source: Python_Lecture.mp3 | 00:12:15–00:13:05`

Video transcript citation:

`Source: Python_Lecture.mp4 | Transcript: 00:12:15–00:13:05`

Video frame citation:

`Source: Python_Lecture.mp4 | Frame timestamp: 00:12:20`

Document citation:

`Source: sample_rag_architecture_notes.pdf | Page 1`

When possible, provide a clickable control to preview the relevant frame or play the media near the cited timestamp.

Ensure that citations reference actual indexed metadata.

## 8. Streamlit UI Pages

Add these pages to the existing application.

### A. Media Dashboard

Display:

- Total audio files.
- Total video files.
- Total transcript chunks.
- Total frame descriptions.
- Total embeddings.
- Last processing status.
- Processing errors.

### B. Audio and Video Upload

Include:

- Drag-and-drop upload.
- File validation.
- Media preview.
- Duration and size.
- Processing options.
- Start processing button.
- Progress indicators.

### C. Transcript Explorer

Allow users to:

- View the full transcript.
- Search transcript text.
- Filter by source file.
- Jump to a timestamp.
- Inspect segment boundaries.
- Download the transcript as TXT or SRT when sufficient timing information is available.

Never create misleading SRT timing data when reliable timestamps are unavailable.

### D. Video Frame Explorer

Show extracted frames in chronological order.

For each frame, display:

- Preview image.
- Timestamp.
- Frame description.
- Related transcript text, if available.
- Embedding status.

Allow users to inspect the frame and its associated ChromaDB record.

### E. Audio and Video Chat

Create a conversational interface that returns answers with timestamped citations.

Where technically supported, provide controls to open the original video at the cited time.

### F. Retrieval Diagnostics

Show:

- Query embedding information.
- Retrieved chunks.
- Transcript timestamps.
- Frame timestamps.
- ChromaDB distance values.
- Source metadata.
- Final context sent to the LLM.

## 9. Suggested Project Structure

Integrate these modules into the existing application. Do not replace working files unnecessarily.

```text
backend/
├── audio_processor.py
├── transcription_service.py
├── transcript_cleaner.py
├── transcript_chunker.py
├── video_processor.py
├── frame_extractor.py
├── frame_analyzer.py
├── media_embeddings.py
├── media_vector_store.py
├── media_retrieval.py
└── unified_rag.py

ui/
├── media_dashboard.py
├── media_upload_page.py
├── transcript_explorer.py
├── video_frame_explorer.py
└── media_chat_page.py

data/
├── uploads/
├── extracted_audio/
├── video_frames/
├── transcripts/
└── chroma_db/

tests/
├── test_audio_processor.py
├── test_transcription.py
├── test_video_processor.py
├── test_frame_extractor.py
├── test_media_chunking.py
└── test_media_retrieval.py
```

Adapt the structure to match the actual existing project.

## 10. Environment Configuration

Update `.env.example` without overwriting existing configuration unnecessarily.

Include settings similar to:

```dotenv
OPENAI_API_KEY=your_openai_api_key_here

OPENAI_CHAT_MODEL=gpt-4.1-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_TRANSCRIPTION_MODEL=gpt-4o-mini-transcribe
OPENAI_VISION_MODEL=gpt-4.1-mini

CHROMA_PERSIST_DIRECTORY=./data/chroma_db

AUDIO_CHUNK_SECONDS=300
VIDEO_FRAME_INTERVAL_SECONDS=10
MAX_UPLOAD_SIZE_MB=200
MAX_MEDIA_DURATION_MINUTES=180
MAX_FRAMES_PER_VIDEO=500

MEDIA_TOP_K=5
```

Treat these values as configurable examples, not universal API limits.

Verify that the selected transcription and vision models support the required capabilities through the current OpenAI API. If a model is unavailable, report the configuration error rather than silently substituting an incompatible model.

Use the same embedding configuration as the existing application unless a deliberate migration is implemented.

## 11. Reliability, Security, and Cost Controls

Implement:

- File-size and duration limits.
- Temporary-file cleanup.
- Safe filenames.
- FFmpeg subprocess timeouts.
- API error handling.
- Bounded retries for transient errors.
- Rate-limit handling.
- Processing status tracking.
- Duplicate detection.
- Partial-failure recovery.
- Persistent indexing.
- Safe media deletion.
- Progress indicators.
- Cost-conscious frame extraction.
- Configurable transcription and vision models.

Do not send every video frame to a vision model.

Do not re-transcribe or re-analyze unchanged media unnecessarily.

Track processing stages so failed jobs can be retried without repeating every successful stage.

Keep API keys out of logs and the UI.

Do not expose local filesystem paths to users when they could reveal sensitive information.

## 12. Tests and Documentation

Create automated tests for:

- Audio metadata extraction.
- Video metadata extraction.
- Transcript chunking.
- Timestamp preservation.
- Frame extraction.
- Stable record IDs.
- Duplicate media detection.
- ChromaDB storage and deletion.
- Retrieval across media types.
- Missing API credentials.
- Unsupported media formats.
- Failed transcription and frame analysis.

Mock OpenAI API calls in unit tests.

Document FFmpeg installation for macOS, Windows, and Linux.

Explain the complete architecture in beginner-friendly English, including the difference between:

- Audio transcription.
- Video audio extraction.
- Keyframe extraction.
- Vision-based frame descriptions.
- Text chunking.
- Embeddings.
- ChromaDB retrieval.
- LLM answer generation.

Include a Mermaid architecture diagram.

## 13. Implementation Workflow

1. Inspect the existing project and identify its current RAG architecture.
2. Preserve the existing PDF, Excel, Word, and TXT functionality.
3. Implement audio ingestion and transcription.
4. Implement transcript chunking and embeddings.
5. Implement video metadata extraction and audio extraction.
6. Implement keyframe extraction and frame descriptions.
7. Implement ChromaDB storage and media metadata.
8. Integrate unified retrieval and answer generation.
9. Build the media dashboard, transcript explorer, and frame explorer.
10. Add tests, documentation, and error handling.
11. Run available tests and verify the actual implementation.
12. Fix integration errors before reporting completion.

Do not stop after proposing an architecture. Create and implement the files.

Do not claim successful execution unless the relevant commands and tests were actually run.

## 14. Acceptance Criteria

The finished application must let me:

1. Upload an audio recording.
2. Generate and inspect its transcript.
3. View transcript timestamps.
4. Split the transcript into chunks.
5. Generate embeddings and inspect their dimensions.
6. Store transcript chunks in persistent ChromaDB.
7. Upload a video.
8. Extract its audio and selected frames.
9. Generate searchable frame descriptions.
10. Search both spoken content and visual descriptions.
11. Ask questions about recorded classes.
12. Receive answers with accurate source filenames and timestamps.
13. Inspect the retrieved chunks that support each answer.
14. Restart the application without losing indexed data.
15. Continue using the existing PDF, Excel, Word, and TXT RAG functionality.

Build a complete, modular, testable educational application suitable for demonstrating Audio RAG and Video RAG to students at VPro Skills EduTech.