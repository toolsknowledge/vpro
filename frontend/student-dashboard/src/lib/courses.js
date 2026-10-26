export function nextLesson(course) {
  return course.queue[0] ?? { title: `Lesson ${course.completedLessons + 1}`, duration: 40 }
}

export function overallProgress(courses) {
  const done = courses.reduce((sum, c) => sum + c.completedLessons, 0)
  const total = courses.reduce((sum, c) => sum + c.totalLessons, 0)
  return { done, total, percent: Math.round((done / total) * 100) }
}
