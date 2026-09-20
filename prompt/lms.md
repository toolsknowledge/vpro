You are a senior software architect and production engineer.
Build a production-ready Learning Management System called:
VPRO SKILLS LMS
The application is for VPRO Skills EduTech.
IMPORTANT:
This project must be developed PHASE BY PHASE.
PHASE 1 is the ONLY phase to implement now.
Do NOT implement assessments, exams, quizzes, assignments, certificates, payments, chat, notifications, attendance, AI features, analytics dashboards, or any other functionality not explicitly requested below.
However, design the backend architecture and database so Phase 2 can be added later WITHOUT breaking Phase 1.
==================================================
COMPANY INFORMATION
==================================================
Company:
VPRO Skills EduTech
Address:
SRNagar, Hyderabad - 500038
Phone:
9010001847
9030001847
YouTube:
@vpro.skills
Instagram:
vpro.skills
Company logo:
Use the provided logo.jpeg file.
DO NOT redesign or recolor the logo.
Primary brand color:
Orange 
#F57C00
Secondary:
Dark charcoal / black
Design should be modern, clean, professional and student friendly.
==================================================
CORE OBJECTIVE
==================================================
Build:
1. Responsive Web Application
2. Android Mobile Application
Both applications must use the SAME REST API backend.
The system must be production-ready.
Phase 1 must focus ONLY on:
ADMIN:
- Admin login
- Create batch
- View batches
- Edit batch
- Activate/deactivate batch
- Add students
- Map students to batches
- Remove student from batch
- Add YouTube video
- Organize videos inside a batch
- Publish/unpublish video
- View basic student video progress
STUDENT:
- Student login
- View assigned batches
- View courses/videos available to the student
- Open video
- Watch video inside LMS
- Resume video from previous position
- Mark video progress automatically
- Continue watching
- See completed videos
- See course/video progress
NOTHING ELSE.
==================================================
VERY IMPORTANT YOUTUBE REQUIREMENT
==================================================
Videos will be hosted on YouTube.
The LMS must NOT store large video files.
Admin will upload/publish the video on the VPRO Skills YouTube channel separately.
Inside LMS admin should enter:
- Video title
- Description
- YouTube URL
- YouTube Video ID
- Batch
- Module/section
- Video order
- Duration if required
- Published status
The system should extract the YouTube video ID from common YouTube URLs.
Examples:
https://www.youtube.com/watch?v=VIDEO_ID
https://youtu.be/VIDEO_ID
https://www.youtube.com/embed/VIDEO_ID
Store only the required YouTube information in the database.
Use the official YouTube IFrame Player API for playback and progress tracking.
DO NOT download the YouTube video.
DO NOT proxy the YouTube video through the backend.
DO NOT store video files locally.
==================================================
YOUTUBE WATCH HOURS
==================================================
The business objective is to use public YouTube videos so legitimate student viewing can also contribute to YouTube channel activity/watch metrics.
Do NOT implement artificial views.
Do NOT autoplay videos.
The student must manually start playback.
Use the YouTube IFrame Player API.
Track LMS-side learning progress separately.
IMPORTANT:
Do not claim that LMS watch time equals YouTube monetization watch hours.
The application should simply embed the legitimate YouTube player and allow students to watch the public video.
==================================================
VIDEO DOWNLOAD RESTRICTION
==================================================
The LMS UI must NOT provide:
- Download button
- Download link
- Direct video file
- Video URL download endpoint
- Backend video proxy
- Video storage endpoint
Use the YouTube embedded player.
Do NOT attempt to bypass YouTube's player restrictions.
Clearly understand that browser screen recording or other capture cannot be completely prevented when using YouTube.
The objective is:
"Students should not have a download facility inside VPRO LMS."
NOT:
"Guarantee that YouTube videos can never be copied."
==================================================
PHASE 1 USER ROLES
==================================================
Only two roles:
ADMIN
STUDENT
Use role-based authorization.
Admin cannot access student-only APIs unless explicitly allowed.
Student cannot access admin APIs.
Every protected API must validate authentication and authorization.
==================================================
ADMIN FUNCTIONALITY
==================================================
ADMIN LOGIN
Admin enters:
Email
Password
After successful login:
Admin Dashboard
Dashboard should show ONLY useful Phase-1 information:
- Total Batches
- Total Students
- Total Videos
- Active Batches
Do not add unnecessary analytics.
==================================================
BATCH MANAGEMENT
==================================================
Admin can:
Create Batch
Fields:
- Batch Name
- Course Name
- Start Date
- End Date
- Description
- Status
Status:
ACTIVE
INACTIVE
Admin can:
- View batches
- Search batches
- Edit batch
- Activate/deactivate batch
Example:
Batch:
GENAI-SEP-2026
Course:
Generative AI
==================================================
STUDENT MANAGEMENT
==================================================
Admin can:
Add Student
Fields:
- Full Name
- Email
- Mobile
- Password / temporary password
- Status
Status:
ACTIVE
INACTIVE
Admin can:
- Search students
- View student
- Edit student
- Activate/deactivate student
==================================================
BATCH-STUDENT MAPPING
==================================================
Admin can assign students to batches.
Example:
Batch:
GENAI-SEP-2026
Students:
student1@gmail.com
student2@gmail.com
student3@gmail.com
A student can belong to multiple batches.
A batch can contain multiple students.
Use a proper many-to-many relationship.
Do NOT duplicate student records.
==================================================
VIDEO MANAGEMENT
==================================================
Admin can add a video to a batch.
Fields:
- Title
- Description
- YouTube URL
- YouTube Video ID
- Module Name
- Video Order
- Thumbnail URL if needed
- Duration
- Published
- Created At
- Updated At
Example:
Module:
Introduction to Generative AI
Video 1:
What is Generative AI?
Video 2:
LLMs Introduction
Video 3:
Prompt Engineering
Admin can:
- Add video
- Edit video
- Delete video
- Publish video
- Unpublish video
- Reorder videos
Students should see only:
ACTIVE BATCH
+
PUBLISHED VIDEOS
==================================================
STUDENT EXPERIENCE
==================================================
Student logs in.
Student Dashboard should be extremely simple.
Show:
Welcome, Student Name
My Batches
For each batch:
Course Name
Batch Name
Number of Videos
Progress %
Example:
Generative AI
GENAI-SEP-2026
12 Videos
68% Completed
==================================================
COURSE / VIDEO PAGE
==================================================
When student opens a batch:
Show:
Course title
Modules
Videos
Example:
Generative AI
Module 1
    1. Introduction
       ✓ Completed
    2. What is Generative AI?
       ▶ Continue
    3. LLM Fundamentals
       ○ Not Started
Module 2
    4. Prompt Engineering
       ○ Not Started
==================================================
VIDEO PLAYER
==================================================
Use YouTube IFrame Player API.
The player must be responsive.
Place player inside a professional LMS video page.
Below player show:
Video title
Description
Module
Progress
Previous Video
Next Video
Do not show a separate download button.
Do not create a video file endpoint.
==================================================
VIDEO PROGRESS TRACKING
==================================================
Track student progress in the LMS database.
When video starts:
Create/update progress record.
Track:
- student_id
- video_id
- last_position_seconds
- watched_seconds
- progress_percentage
- completed
- first_started_at
- last_watched_at
- completed_at
Save progress periodically.
Do NOT make a database request every second.
Use a reasonable interval such as every 10-15 seconds.
Also save progress when:
- video pauses
- video ends
- student leaves page
When the student returns:
Resume from last_position_seconds where technically supported.
Mark completed when the student reaches a configurable completion threshold.
Default:
90%
Do not require the student to manually click "Complete".
==================================================
PROGRESS CALCULATION
==================================================
Video progress:
watched position / video duration * 100
Course progress:
completed videos / total published videos * 100
Display progress clearly.
Example:
Course Progress
████████████░░░░ 75%
==================================================
SECURITY
==================================================
Production-grade authentication.
Use:
JWT access token
Refresh token if required
Passwords must be hashed.
Never store plaintext passwords.
Use environment variables for:
DATABASE_URL
JWT_SECRET
JWT_EXPIRATION
CORS_ORIGINS
YOUTUBE configuration if required
Never hardcode secrets.
Never commit .env files.
Create .env.example.
==================================================
DATABASE
==================================================
Use PostgreSQL.
Use proper database relationships.
Minimum tables:
users
batches
batch_students
videos
video_progress
The architecture must allow future tables for Phase 2 without changing existing Phase-1 tables unnecessarily.
Suggested conceptual relationships:
users
  |
  | many-to-many
  |
batch_students
  |
  |
batches
  |
  | one-to-many
  |
videos
  |
  | one-to-many
  |
video_progress
  |
student
video_progress should reference:
student/user
video
Use foreign keys.
Use indexes on:
users.email
batch_students.student_id
batch_students.batch_id
videos.batch_id
videos.published
video_progress.student_id
video_progress.video_id
Prevent duplicate batch-student mappings.
Prevent duplicate video ordering conflicts where appropriate.
==================================================
BACKEND
==================================================
Use:
Python
FastAPI
PostgreSQL
SQLAlchemy
Alembic
Pydantic
Backend must be REST API based.
Use clean separation:
app/
    main.py
    core/
        config.py
        security.py
    db/
        database.py
    models/
    schemas/
    routers/
    services/
    repositories/
    dependencies/
Do not over-engineer.
Only create files that are actually required.
==================================================
API DESIGN
==================================================
Implement only Phase-1 APIs.
Authentication:
POST /api/auth/login
GET /api/auth/me
Admin:
POST /api/admin/batches
GET /api/admin/batches
GET /api/admin/batches/{id}
PUT /api/admin/batches/{id}
PATCH /api/admin/batches/{id}/status
POST /api/admin/students
GET /api/admin/students
GET /api/admin/students/{id}
PUT /api/admin/students/{id}
PATCH /api/admin/students/{id}/status
POST /api/admin/batches/{batch_id}/students/{student_id}
DELETE /api/admin/batches/{batch_id}/students/{student_id}
POST /api/admin/videos
GET /api/admin/videos
GET /api/admin/videos/{id}
PUT /api/admin/videos/{id}
DELETE /api/admin/videos/{id}
PATCH /api/admin/videos/{id}/publish
Student:
GET /api/student/batches
GET /api/student/batches/{batch_id}
GET /api/student/batches/{batch_id}/videos
GET /api/student/videos/{video_id}
GET /api/student/videos/{video_id}/progress
PUT /api/student/videos/{video_id}/progress
GET /api/student/progress
Do not create APIs for functionality not required in Phase 1.
==================================================
FRONTEND WEB
==================================================
Use:
React
Vite
TypeScript
Use a clean component architecture.
Suggested structure:
src/
    components/
    layouts/
    pages/
        auth/
        admin/
        student/
    services/
    hooks/
    context/
    types/
    utils/
Use responsive design.
The web application must work properly on:
Desktop
Tablet
Mobile browser
==================================================
DESIGN
==================================================
The application must look like a professional modern education platform.
Brand:
Orange:
#F57C00
Dark:
#222222
White:
#FFFFFF
Use the provided VPRO Skills logo.
Do not modify the logo.
Design principles:
- Clean
- Minimal
- Professional
- Student friendly
- Fast
- Modern
- Attractive
- Mobile responsive
- Large readable typography
- Clear navigation
- Excellent spacing
- Consistent cards
- Professional buttons
- Good empty states
- Good loading states
- Good error states
Do NOT create unnecessary animations.
Do NOT make the UI childish.
The application should look suitable for a professional technology training company.
==================================================
WEB LAYOUT
==================================================
ADMIN:
Left sidebar:
VPRO Skills Logo
Dashboard
Batches
Students
Videos
Profile
Logout
Top bar:
Page title
Admin name
==================================================
STUDENT:
Mobile-friendly sidebar/bottom navigation.
Navigation:
Home
My Batches
Progress
Profile
Keep it simple.
==================================================
LOGIN PAGE
==================================================
Professional VPRO Skills login screen.
Left/upper section:
VPRO Skills logo
"Learn. Build. Grow."
Right section:
Login form
Email
Password
Login
Use the company orange color.
Mobile should become a single-column layout.
==================================================
ANDROID APPLICATION
==================================================
Build Android application using:
React Native + Expo
Use the same FastAPI backend.
Do NOT create a separate backend.
Android screens:
Login
Home
My Batches
Batch Details
Video Player
Progress
Profile
Use the same branding.
Use the provided VPRO Skills logo.
Video playback should use the YouTube embedded/player approach appropriate for Android.
Do not download video files to the device.
Do not implement offline video.
==================================================
ANDROID UI
==================================================
The mobile application should feel like a professional education app.
Use:
Cards
Rounded corners
Clear typography
Large touch targets
Progress indicators
Professional icons
Orange branding
Avoid unnecessary UI.
==================================================
ADMIN VIDEO WORKFLOW
==================================================
Admin workflow:
1. Login
2. Open Batches
3. Create batch
4. Open batch
5. Add students
6. Map students
7. Open Videos
8. Add YouTube video
9. Enter YouTube URL
10. System extracts Video ID
11. Enter title/module/order
12. Save
13. Publish
14. Student can immediately see the video
==================================================
STUDENT VIDEO WORKFLOW
==================================================
Student workflow:
1. Login
2. See assigned batches
3. Select batch
4. See modules/videos
5. Select video
6. YouTube player opens inside LMS
7. Student manually starts video
8. LMS tracks progress
9. Student leaves
10. Progress saved
11. Student returns later
12. Student continues from previous position
==================================================
PHASE 1 MUST NOT CONTAIN
==================================================
Do NOT implement:
- Assessments
- MCQs
- Exams
- Question banks
- Coding tests
- Assignments
- Certificates
- Payments
- Subscriptions
- Attendance
- Chat
- Messaging
- Notifications
- AI chatbot
- RAG
- Live classes
- Zoom integration
- Email automation
- WhatsApp integration
- Gamification
- Leaderboards
- Referral system
- Affiliate system
- Instructor role
- Parent role
- Reports beyond basic video progress
- Complex analytics
- Video file upload
- Video transcoding
- Cloud video storage
- DRM
- Social login
DO NOT ADD THESE FEATURES.
==================================================
PHASE 2 ARCHITECTURE
==================================================
Do NOT implement Phase 2 now.
But make the architecture extensible for:
PHASE 2:
Assessments
Future functionality may include:
Admin:
- Create assessment
- Add questions
- Add MCQs
- Configure duration
- Configure passing score
- Assign assessment to batch
- Publish assessment
Student:
- View assessment
- Start assessment
- Answer questions
- Submit
- View result
IMPORTANT:
Phase 2 must be independently deployable.
Adding Phase 2 must NOT break:
- authentication
- batches
- students
- video management
- YouTube player
- video progress
Keep module boundaries clean.
==================================================
PRODUCTION REQUIREMENTS
==================================================
The code must be production-oriented.
Implement:
- Input validation
- Authentication
- Authorization
- Proper error handling
- API response consistency
- Database transactions
- Logging
- CORS configuration
- Environment configuration
- Database migrations
- Health endpoint
- Secure password hashing
- JWT security
- Proper HTTP status codes
Health endpoint:
GET /health
Response:
{
    "status": "ok"
}
==================================================
DOCKER
==================================================
Create production-friendly Docker configuration.
Backend Dockerfile.
Frontend Dockerfile if appropriate.
docker-compose.yml for local development:
backend
postgres
frontend
Do not put secrets directly inside docker-compose.yml.
Use .env.
==================================================
DATABASE MIGRATIONS
==================================================
Use Alembic.
The application must start from an empty PostgreSQL database using migrations.
Document:
alembic upgrade head
==================================================
TESTING
==================================================
The application must be test-proof before claiming Phase 1 complete.
Backend tests:
- Login success
- Login failure
- Unauthorized API access
- Admin authorization
- Student authorization
- Create batch
- Create student
- Map student to batch
- Prevent duplicate mapping
- Add video
- Publish video
- Student sees assigned batch
- Student cannot see unassigned batch
- Student sees published videos
- Student cannot see unpublished videos
- Save video progress
- Retrieve progress
- Completion logic
Frontend tests where practical:
- Login
- Admin navigation
- Student navigation
- Batch rendering
- Video rendering
- Progress rendering
==================================================
SEED DATA
==================================================
Provide development seed data.
Create:
Admin:
admin@vproskills.com
Student:
student@vproskills.com
Create one demo batch.
Create a few demo videos using placeholder YouTube IDs.
Clearly document development credentials.
Never use these credentials in production.
==================================================
README
==================================================
Create a professional README.md.
Include:
Project overview
Architecture
Technology stack
Folder structure
Environment variables
Local setup
Database setup
Migration commands
Seed commands
Backend start command
Frontend start command
Android start command
Testing commands
Docker commands
Production deployment instructions
Phase 1 functionality
Phase 2 future architecture
Security notes
YouTube integration notes
==================================================
PRODUCTION DEPLOYMENT
==================================================
Design the application so it can be deployed to:
Linux VPS / AWS / Azure / similar cloud
Recommended production architecture:
Internet
   |
HTTPS
   |
Reverse Proxy
   |
Frontend
   |
FastAPI
   |
PostgreSQL
YouTube is external video infrastructure.
Do not store video files on the application server.
==================================================
ERROR HANDLING
==================================================
Provide clean user-friendly messages.
Examples:
Invalid login:
"Invalid email or password."
Inactive student:
"Your account is currently inactive. Please contact VPRO Skills."
No batch:
"No batches have been assigned to you yet."
No videos:
"No sessions are available yet."
Video unavailable:
"This session is temporarily unavailable."
Do not expose database errors to users.
==================================================
IMPORTANT SECURITY RULES
==================================================
Never expose:
- Password hashes
- JWT secrets
- Database credentials
- Internal stack traces
- Environment variables
Do not log passwords.
Do not store YouTube video files.
Do not create download endpoints.
Validate YouTube URLs.
Validate all IDs.
Validate ownership/access through batch membership.
A student must only access videos belonging to batches assigned to that student.
Do not trust frontend authorization.
All authorization must be enforced on backend APIs.
==================================================
CODE QUALITY RULES
==================================================
Write clean, readable production code.
Do not generate unnecessary abstractions.
Do not create unnecessary files.
Do not create unused functions.
Do not create unused dependencies.
Do not implement speculative features.
Do not copy huge boilerplate templates.
Do not leave TODOs for Phase 1 requirements.
Do not use fake APIs.
Do not use mock APIs in production code.
Use proper database queries.
Use transactions where needed.
Use async FastAPI patterns appropriately.
==================================================
IMPORTANT DEVELOPMENT PROCESS
==================================================
Before writing code:
1. Inspect the existing project directory.
2. If a project already exists, preserve useful existing code.
3. Do not overwrite unrelated files.
4. Create a clear implementation plan.
5. Confirm the Phase-1 architecture internally.
6. Implement backend.
7. Implement database.
8. Implement frontend.
9. Implement Android.
10. Add tests.
11. Run tests.
12. Fix all errors.
13. Run the application locally.
14. Verify API endpoints.
15. Verify database migrations.
16. Verify frontend.
17. Verify authentication.
18. Verify student access restrictions.
19. Verify YouTube playback.
20. Verify progress tracking.
21. Only then declare Phase 1 complete.
==================================================
CRITICAL ACCEPTANCE TEST
==================================================
Phase 1 is considered COMPLETE only if this complete workflow works:
ADMIN
Admin Login
   ↓
Create Batch
   ↓
Create Student
   ↓
Map Student to Batch
   ↓
Add YouTube Video
   ↓
Publish Video
   ↓
Logout
STUDENT
Student Login
   ↓
My Batches
   ↓
Open Batch
   ↓
See Published Videos
   ↓
Open Video
   ↓
Watch YouTube Video
   ↓
Progress Saved
   ↓
Leave
   ↓
Login Again
   ↓
Open Same Video
   ↓
Previous Progress Available
Also verify:
Student A cannot access Student B's unrelated batch.
Student cannot access an unpublished video.
Student cannot call admin APIs.
Student cannot download a video through any VPRO LMS API.
Admin can manage batches, students and videos.
==================================================
FINAL DEVELOPMENT RULE
==================================================
KEEP PHASE 1 SMALL.
The goal is to get VPRO Skills LMS into production quickly.
Do not turn this into a giant LMS.
The first production release should be:
LOGIN
+
BATCHES
+
STUDENTS
+
YOUTUBE VIDEOS
+
VIDEO PLAYER
+
VIDEO PROGRESS
Nothing more.
After Phase 1 is stable in production, Phase 2 can be developed separately.
==================================================
BRAND
==================================================
Use the provided VPRO Skills logo.jpeg.
Company:
VPRO Skills EduTech
Address:
SRNagar Hyderabad 500038
Phone:
9010001847 | 9030001847
YouTube:
@vpro.skills
Instagram:
vpro.skills
Primary brand:
#F57C00
Final UI must look:
Professional
Modern
Clean
Premium
Student-friendly
Fast
Responsive
Do not change the logo.
Do not invent additional company information.
==================================================
START NOW
==================================================
First inspect the project.
Then provide a concise implementation plan.
Then implement Phase 1 completely.
Do not ask me to approve every individual file.
Make reasonable engineering decisions yourself.
Do not implement Phase 2.
At the end:
1. Run tests.
2. Fix failures.
3. Show the final folder structure.
4. Show environment variables required.
5. Show database migration command.
6. Show local startup commands.
7. Show production deployment steps.
8. Show the Phase-1 acceptance test result.
9. Clearly list anything that could not be verified.
Do not claim something is tested unless you actually ran it.