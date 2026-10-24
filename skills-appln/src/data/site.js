import { Atom, Bot, Coffee, Database, Cloud, Layers } from 'lucide-react'

export const navLinks = [
  { label: 'Courses', href: '#courses' },
  { label: 'How it works', href: '#path' },
  { label: 'Student stories', href: '#stories' },
  { label: 'FAQ', href: '#faq' },
]

// Track colours map to the timetable blocks so a course reads the same everywhere.
export const tracks = {
  frontend: { label: 'Frontend', chip: 'bg-cobalt-tint text-cobalt-deep', bar: 'bg-cobalt' },
  fullstack: { label: 'Full Stack', chip: 'bg-brand-tint text-[#9a4b00]', bar: 'bg-brand' },
  data: { label: 'Data & AI', chip: 'bg-mint-tint text-[#0d6b55]', bar: 'bg-mint' },
  cloud: { label: 'Cloud', chip: 'bg-rose-tint text-[#a72649]', bar: 'bg-rose' },
}

export const courses = [
  {
    id: 'react',
    title: 'React with Modern JavaScript',
    track: 'frontend',
    icon: Atom,
    level: 'Beginner',
    weeks: 10,
    mode: 'Live online',
    nextBatch: '2 Nov',
    seatsLeft: 6,
    fee: 14999,
    modules: ['JSX & components', 'Props & state', 'Hooks', 'Context & Redux', 'Routing & APIs'],
  },
  {
    id: 'vibe',
    title: 'Vibe Coding: Build Apps with AI',
    track: 'data',
    icon: Bot,
    level: 'All levels',
    weeks: 6,
    mode: 'Live online',
    nextBatch: '9 Nov',
    seatsLeft: 12,
    fee: 9999,
    modules: ['Prompting for code', 'Claude Code workflow', 'Design skills', 'Shipping a project'],
  },
  {
    id: 'mern',
    title: 'MERN Full Stack Developer',
    track: 'fullstack',
    icon: Layers,
    level: 'Intermediate',
    weeks: 16,
    mode: 'Live + lab',
    nextBatch: '16 Nov',
    seatsLeft: 4,
    fee: 29999,
    modules: ['React', 'Node & Express', 'MongoDB', 'Auth & security', 'Capstone'],
  },
  {
    id: 'java',
    title: 'Java Full Stack with Spring Boot',
    track: 'fullstack',
    icon: Coffee,
    level: 'Beginner',
    weeks: 20,
    mode: 'Live + lab',
    nextBatch: '23 Nov',
    seatsLeft: 9,
    fee: 32999,
    modules: ['Core Java', 'JDBC & SQL', 'Spring Boot', 'REST APIs', 'React frontend'],
  },
  {
    id: 'python',
    title: 'Python for Data Analytics',
    track: 'data',
    icon: Database,
    level: 'Beginner',
    weeks: 12,
    mode: 'Live online',
    nextBatch: '30 Nov',
    seatsLeft: 15,
    fee: 17999,
    modules: ['Python basics', 'Pandas', 'SQL', 'Dashboards', 'Case studies'],
  },
  {
    id: 'aws',
    title: 'DevOps on AWS',
    track: 'cloud',
    icon: Cloud,
    level: 'Intermediate',
    weeks: 12,
    mode: 'Weekend live',
    nextBatch: '7 Dec',
    seatsLeft: 8,
    fee: 24999,
    modules: ['Linux & Git', 'Docker', 'CI/CD', 'AWS core', 'Terraform'],
  },
]

// One cohort week, as shown in the hero. start/length are in hours from 7 AM.
export const week = [
  { day: 'Mon', slots: [{ track: 'frontend', title: 'useEffect & APIs', start: 12, length: 1.5 }] },
  { day: 'Tue', slots: [{ track: 'fullstack', title: 'Express routes', start: 12, length: 1.5 }] },
  {
    day: 'Wed',
    slots: [
      { track: 'data', title: 'Doubt clearing', start: 6, length: 1.5 },
      { track: 'frontend', title: 'Code review', start: 12.5, length: 1 },
    ],
  },
  { day: 'Thu', slots: [{ track: 'data', title: 'Prompt lab', start: 12, length: 1.5 }] },
  { day: 'Fri', slots: [{ track: 'cloud', title: 'Lab hour', start: 10.5, length: 1.5 }] },
  {
    day: 'Sat',
    slots: [
      { track: 'frontend', title: 'Live: Custom hooks', start: 1, length: 1.5, live: true },
      { track: 'cloud', title: 'Mock interview', start: 4, length: 1 },
    ],
  },
  { day: 'Sun', slots: [{ track: 'fullstack', title: 'Project sprint', start: 2, length: 2.5 }] },
]

export const pathSteps = [
  {
    title: 'Attend a free demo class',
    body: 'Sit in on a real Saturday session and talk to the mentor before you pay anything.',
  },
  {
    title: 'Learn live, in a small batch',
    body: 'Batches are capped at 30 so mentors can review your code, not just present slides.',
  },
  {
    title: 'Build three portfolio projects',
    body: 'Every course ends in deployed apps you can show an interviewer, with your own Git history.',
  },
  {
    title: 'Prepare for interviews',
    body: 'Mock interviews, resume reviews and referrals to our hiring partners after you finish.',
  },
]

export const stories = [
  {
    quote:
      'The Saturday live sessions were the first time someone looked at my React code line by line. Three months later I was explaining hooks in my own interview.',
    name: 'Harika Reddy',
    role: 'Frontend Developer, Hyderabad',
    course: 'React with Modern JavaScript',
  },
  {
    quote:
      'I came from a mechanical background. The capstone project gave me something real to talk about, and the mock interviews took the fear out of it.',
    name: 'Praveen Kumar',
    role: 'Associate Engineer, Bengaluru',
    course: 'Java Full Stack with Spring Boot',
  },
  {
    quote:
      'Vibe coding changed how I work. I ship side projects in a weekend now, and I actually understand the code the AI writes.',
    name: 'Sneha Joshi',
    role: 'Final-year B.Tech student',
    course: 'Vibe Coding: Build Apps with AI',
  },
]

export const faqs = [
  {
    q: 'I have no coding background. Where should I start?',
    a: 'Start with React with Modern JavaScript or Python for Data Analytics. Both begin from fundamentals, and the free demo class will tell you if the pace suits you.',
  },
  {
    q: 'What if I miss a live class?',
    a: 'Every session is recorded and posted within a few hours. Your mentor also holds a weekly doubt-clearing slot for anything you missed.',
  },
  {
    q: 'Can I pay in instalments?',
    a: 'Yes. Courses above ₹15,000 can be paid in three monthly instalments with no extra charge.',
  },
  {
    q: 'Do you offer placement support?',
    a: 'We provide resume reviews, mock interviews and referrals to partner companies. We do not promise a job, but we prepare you properly for one.',
  },
]
