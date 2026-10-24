export const projects = [
  {
    id: 'p1',
    title: 'Campus events portal',
    courseId: 'py-fs',
    status: 'in-progress',
    due: '2026-11-20',
    stack: ['Django', 'DRF', 'PostgreSQL', 'React'],
    summary: 'A portal where college clubs publish events and students register, with an admin view for approvals.',
    milestones: [
      { title: 'Data model and admin', done: true },
      { title: 'Event and registration APIs', done: true },
      { title: 'Authentication and roles', done: false },
      { title: 'React front end', done: false },
      { title: 'Deployment and demo', done: false },
    ],
  },
  {
    id: 'p2',
    title: 'Hospital appointment system',
    courseId: 'java-fs',
    status: 'in-progress',
    due: '2026-12-10',
    stack: ['Spring Boot', 'JPA', 'MySQL', 'Angular'],
    summary: 'Doctors publish slots and patients book them. Includes email reminders mocked in the service layer.',
    milestones: [
      { title: 'Domain model', done: true },
      { title: 'Slot and booking APIs', done: false },
      { title: 'Front end screens', done: false },
      { title: 'Testing and demo', done: false },
    ],
  },
  {
    id: 'p3',
    title: 'Student notes search assistant',
    courseId: 'genai',
    status: 'not-started',
    due: '2027-01-15',
    stack: ['Python', 'Embeddings', 'Vector store'],
    summary: 'Ask questions over your own course notes and get answers with links back to the source pages.',
    milestones: [
      { title: 'Collect and chunk notes', done: false },
      { title: 'Embedding and retrieval', done: false },
      { title: 'Answer generation with citations', done: false },
    ],
  },
  {
    id: 'p4',
    title: 'Library management database',
    courseId: 'sql',
    status: 'approved',
    due: '2026-09-25',
    stack: ['MySQL', 'ER modelling'],
    summary: 'Normalised schema with stored procedures for issue and return, plus reporting queries.',
    milestones: [
      { title: 'ER diagram', done: true },
      { title: 'Schema and seed data', done: true },
      { title: 'Procedures and reports', done: true },
    ],
  },
]

export const projectStatusLabels = {
  'not-started': 'Not started',
  'in-progress': 'In progress',
  approved: 'Approved',
}
