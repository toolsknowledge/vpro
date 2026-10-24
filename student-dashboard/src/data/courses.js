// `queue` holds the next lessons in order; the first item is the next lesson.
export const courses = [
  {
    id: 'py-fs',
    title: 'Python Full Stack Development',
    instructor: 'Sravani Reddy',
    pattern: 'python',
    totalLessons: 96,
    completedLessons: 61,
    module: 'Module 7: Django REST Framework',
    moduleLessons: 8,
    moduleCompleted: 3,
    queue: [
      { title: 'Serializers and model validation', duration: 42 },
      { title: 'Class-based API views', duration: 38 },
      { title: 'Authentication with JWT', duration: 51 },
      { title: 'Pagination and filtering', duration: 34 },
      { title: 'Testing APIs with pytest', duration: 46 },
    ],
  },
  {
    id: 'java-fs',
    title: 'Java Full Stack Development',
    instructor: 'Kiran Kumar',
    pattern: 'java',
    totalLessons: 110,
    completedLessons: 42,
    module: 'Module 4: Spring Boot Essentials',
    moduleLessons: 10,
    moduleCompleted: 6,
    queue: [
      { title: 'Spring Data JPA repositories', duration: 44 },
      { title: 'Entity relationships', duration: 48 },
      { title: 'Exception handling with @ControllerAdvice', duration: 36 },
      { title: 'Validation with Bean Validation', duration: 32 },
    ],
  },
  {
    id: 'mern',
    title: 'MERN Stack Development',
    instructor: 'Priya Nair',
    pattern: 'mern',
    totalLessons: 84,
    completedLessons: 44,
    module: 'Module 6: React State and Data',
    moduleLessons: 9,
    moduleCompleted: 5,
    queue: [
      { title: 'useReducer for complex state', duration: 39 },
      { title: 'Context without prop drilling', duration: 35 },
      { title: 'Fetching data with effects', duration: 41 },
      { title: 'Building a cart with Context', duration: 55 },
    ],
  },
  {
    id: 'genai',
    title: 'Generative AI and Agentic AI',
    instructor: 'Arjun Mehta',
    pattern: 'ai',
    totalLessons: 64,
    completedLessons: 13,
    module: 'Module 2: Prompting and Retrieval',
    moduleLessons: 7,
    moduleCompleted: 2,
    queue: [
      { title: 'Embeddings and vector search', duration: 47 },
      { title: 'Building a RAG pipeline', duration: 58 },
      { title: 'Evaluating retrieval quality', duration: 40 },
      { title: 'Tool calling basics', duration: 43 },
    ],
  },
  {
    id: 'sql',
    title: 'SQL and Database Design',
    instructor: 'Kiran Kumar',
    pattern: 'sql',
    totalLessons: 32,
    completedLessons: 32,
    module: 'All modules complete',
    moduleLessons: 0,
    moduleCompleted: 0,
    queue: [],
  },
  {
    id: 'git',
    title: 'Git and GitHub for Teams',
    instructor: 'Priya Nair',
    pattern: 'git',
    totalLessons: 18,
    completedLessons: 18,
    module: 'All modules complete',
    moduleLessons: 0,
    moduleCompleted: 0,
    queue: [],
  },
  {
    id: 'devops',
    title: 'Cloud and DevOps Essentials',
    instructor: 'Mohammed Imran',
    pattern: 'cloud',
    totalLessons: 40,
    completedLessons: 0,
    module: 'Module 1: Linux and the Command Line',
    moduleLessons: 6,
    moduleCompleted: 0,
    queue: [
      { title: 'Navigating the Linux file system', duration: 30 },
      { title: 'Permissions and users', duration: 33 },
      { title: 'Shell scripting basics', duration: 45 },
    ],
  },
]

export function courseStatus(course) {
  if (course.completedLessons >= course.totalLessons) return 'completed'
  if (course.completedLessons === 0) return 'not-started'
  return 'in-progress'
}

export function coursePercent(course) {
  return Math.round((course.completedLessons / course.totalLessons) * 100)
}

export const courseStatusLabels = {
  'in-progress': 'In progress',
  'not-started': 'Not started',
  completed: 'Completed',
}
