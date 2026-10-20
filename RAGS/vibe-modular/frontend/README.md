# Frontend

Angular 21 UI for uploading DOCX documents and chatting with them. See the [project README](../README.md) for setup.

```bash
npm install
npm start                      # http://localhost:4200
npm test -- --watch=false      # unit tests (Vitest)
npm run build                  # production build in dist/
```

- `src/app/services/rag-api.service.ts` handles all backend calls. The base URL comes from `src/environments/`.
- `src/app/documents/` handles upload, indexing status, the document list and deletion.
- `src/app/chat/` handles questions, answers and source references.
