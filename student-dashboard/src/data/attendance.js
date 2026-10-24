// Most recent first.
export const attendanceRecords = [
  { id: 'r1', date: '2026-10-23', courseId: 'py-fs', topic: 'Serializers introduction', status: 'present' },
  { id: 'r2', date: '2026-10-23', courseId: 'genai', topic: 'Retrieval concepts', status: 'present' },
  { id: 'r3', date: '2026-10-22', courseId: 'java-fs', topic: 'Spring Boot project setup', status: 'present' },
  { id: 'r4', date: '2026-10-21', courseId: 'mern', topic: 'useState patterns', status: 'absent' },
  { id: 'r5', date: '2026-10-21', courseId: 'py-fs', topic: 'Django REST overview', status: 'present' },
  { id: 'r6', date: '2026-10-20', courseId: 'java-fs', topic: 'Dependency injection', status: 'present' },
  { id: 'r7', date: '2026-10-19', courseId: 'genai', topic: 'Prompt patterns lab', status: 'absent' },
  { id: 'r8', date: '2026-10-17', courseId: 'mern', topic: 'Component composition', status: 'present' },
  { id: 'r9', date: '2026-10-16', courseId: 'py-fs', topic: 'Django ORM queries', status: 'present' },
  { id: 'r10', date: '2026-10-15', courseId: 'java-fs', topic: 'Maven and project structure', status: 'present' },
  { id: 'r11', date: '2026-10-14', courseId: 'mern', topic: 'Props and children', status: 'present' },
  { id: 'r12', date: '2026-10-13', courseId: 'py-fs', topic: 'Django admin customisation', status: 'present' },
]

// Totals for the whole programme so far, including older sessions not listed above.
export const attendanceTotals = {
  attended: 58,
  total: 66,
  byCourse: [
    { courseId: 'py-fs', attended: 22, total: 24 },
    { courseId: 'java-fs', attended: 15, total: 17 },
    { courseId: 'mern', attended: 13, total: 15 },
    { courseId: 'genai', attended: 8, total: 10 },
  ],
  minimumRequired: 75,
}
