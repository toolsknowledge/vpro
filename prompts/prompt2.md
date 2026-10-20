# Master Prompt: Generate UML Diagrams for VPro Skills

Act as a professional Business Analyst and UML Designer.

## Project Context

Project Name: **VPro Skills – Upcoming Training Batches Web Page**

VPro Skills is an education technology company. The web page will display upcoming training batches such as:

- Forward Deployed Engineer (FDE)
- Agentic AI
- Generative AI

The purpose is to help students explore upcoming courses and view relevant batch information.

Use the existing BRD and SRD documents as the primary reference for creating UML diagrams.

## Your Task

Analyze the BRD and SRD and generate the following four diagrams:

### 1. Use Case Diagram

Show the interaction between users and the VPro Skills web page.

Include:
- Actors relevant to the documented requirements.
- Viewing available courses.
- Exploring course details.
- Viewing upcoming batch information.
- Other use cases only if explicitly supported by the BRD or SRD.

Clearly show actors, use cases, and their relationships.

### 2. Flow Diagram

Create a flow diagram showing the user's journey through the web page.

Include:
- Start
- Open the VPro Skills web page.
- View available courses.
- Select a course.
- View its batch information.
- Return to the course list or continue exploring.
- End.

Use decision nodes only where required. Keep the flow simple and easy to understand.

### 3. Class Diagram

Create a UML class diagram representing the main entities required for the web page.

Consider the following classes, subject to the BRD and SRD:

- Course
- Batch
- CourseCatalog or CourseService, only if justified by the documented scope.

Show relevant attributes, data types, relationships, multiplicities, and methods where appropriate.

Do not introduce unnecessary classes, authentication, databases, payment systems, or backend components that are outside the documented scope.

### 4. Activity Diagram

Create an activity diagram representing the process of exploring upcoming training batches.

Include:
- Initial node.
- Opening the web page.
- Displaying available courses.
- Selecting a course.
- Displaying the selected course's batch details.
- Returning to the course list when the user wants to explore another course.
- Final node.

Use decision nodes, action nodes, and control-flow arrows correctly.

## Diagram Creation Rules

- Use standard UML notation wherever applicable.
- Use simple English labels.
- Keep diagrams clean, readable, and professional.
- Avoid unnecessary complexity.
- Ensure all diagrams represent the same system and scope.
- Do not add features that are not documented in the BRD or SRD.
- If the BRD or SRD does not define a detail, mark it as TBD or omit it rather than inventing requirements.
- Make the diagrams understandable to beginners and suitable for professional project documentation.

## Technical Output Requirements

Generate all four diagrams using **Mermaid syntax** wherever suitable.

Use the appropriate Mermaid diagram types:

- Use Case Diagram: Use a valid UML-compatible notation supported by the selected rendering tool; if Mermaid does not support the required UML notation directly, use PlantUML for this diagram.
- Flow Diagram: `flowchart TD`
- Class Diagram: `classDiagram`
- Activity Diagram: `flowchart TD`, using activity-style nodes and decision branches.

For each diagram, provide:

1. Diagram title.
2. A short explanation in simple English.
3. Complete diagram source code.
4. A brief explanation of the actors, classes, actions, or relationships.

## Expected Output

Create four separate Markdown files:

1. `VPro_Skills_Use_Case_Diagram.md`
2. `VPro_Skills_Flow_Diagram.md`
3. `VPro_Skills_Class_Diagram.md`
4. `VPro_Skills_Activity_Diagram.md`

Save the files in the project documentation folder if one exists; otherwise, use a clearly named `docs` folder.

Before finalizing, verify that all diagrams are syntactically correct, consistent with the BRD and SRD, and limited to the VPro Skills upcoming training batches web page.