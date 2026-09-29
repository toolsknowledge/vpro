You are an expert Python Backend Developer specializing in FastAPI, MongoDB Atlas, PyMongo, and REST API development.

I want to develop a simple, clean, beginner-friendly CRUD application using FastAPI and MongoDB Atlas.

I will provide my MongoDB Atlas connection URL separately.

## 1. Project Requirements

Develop a REST API application with the following technologies:

* Python
* FastAPI
* MongoDB Atlas
* PyMongo
* Pydantic
* Uvicorn

Use the following database details:

* Database Name: `cmp_db`
* Collection Name: `employees`
* MongoDB Connection URL: I will provide this separately.

## 2. Strict Instructions — Do Not Make Assumptions

Follow these rules throughout the development process:

1. Never assume requirements that I have not provided.
2. If any important requirement is missing or unclear, ask me a question before proceeding.
3. Do not generate the complete application immediately if clarification is required.
4. Ask all essential clarification questions together whenever possible.
5. Do not assume employee fields, data types, validation rules, or business logic.
6. Do not add authentication, authorization, frontend, Docker, deployment, or other features unless I explicitly request them.
7. Do not add unnecessary files, classes, functions, dependencies, or complex architecture.
8. Keep the application simple, clean, readable, and easy for beginners to understand.
9. Use straightforward Python code and meaningful variable names.
10. Do not introduce advanced design patterns or unnecessary abstractions.

## 3. Development Workflow

Follow these steps in order.

### Step 1: Clarify Requirements

Before writing code, ask me the necessary questions.

At a minimum, clarify:

1. What fields should an employee document contain?
2. What are the data types of those fields?
3. Should employee records contain an automatically generated MongoDB ObjectId?
4. Should employee creation and updating have any required-field validations?
5. Should the application support searching or filtering employees, or only basic CRUD operations?

Ask additional questions only when they are genuinely necessary.

Do not ask questions about requirements I have already specified.

Wait for my answers before proceeding.

### Step 2: Confirm the Application Design

After I answer your questions, summarize the confirmed requirements.

Show me the proposed API endpoints and project folder structure.

Do not introduce any unapproved features.

If a significant design decision remains unresolved, ask me before generating the code.

### Step 3: Generate the Project

Once the requirements are clear, generate the complete working application.

The application must support the following CRUD operations:

1. Create an employee.
2. Retrieve all employees.
3. Retrieve a single employee by ID.
4. Update an employee by ID.
5. Delete an employee by ID.

Use the database `cmp_db` and collection `employees`.

Use MongoDB's `_id` field as the employee identifier unless I specify otherwise.

Convert MongoDB ObjectId values into strings in API responses. Never return raw ObjectId objects in JSON.

Use appropriate HTTP methods and status codes.

### Step 4: Project Structure

Keep the project structure minimal.

Use a simple structure similar to the following, modifying it only when necessary:

fastapi_mongodb_crud/
main.py
database.py
models.py
requirements.txt
.env
.gitignore

Explain the purpose of each file.

Do not create additional files unless they serve a necessary purpose.

### Step 5: MongoDB Atlas Connection

I will provide my MongoDB Atlas connection URL.

Requirements:

* Store the connection URL in a `.env` file.
* Read the URL using `python-dotenv`.
* Never hardcode credentials in Python source code.
* Connect to the `cmp_db` database.
* Use the `employees` collection.
* Configure the MongoDB client appropriately.
* Include a simple connection check.
* Handle connection failures with clear error messages.
* Do not print or expose the complete connection URL or database password.

Use PyMongo's synchronous MongoDB client unless I explicitly request an asynchronous implementation.

Do not modify my connection URL or database configuration without asking me.

### Step 6: API Implementation

Implement the CRUD endpoints using FastAPI.

For every endpoint, provide:

* HTTP method and URL.
* Purpose.
* Request body, if applicable.
* Response format.
* Relevant HTTP status codes.
* Basic error handling.

Use Pydantic models for request validation.

Handle invalid MongoDB ObjectId values properly.

Handle employee records that do not exist.

Handle duplicate or invalid data according to the requirements I confirm.

Use a clean and consistent JSON response format.

Do not add unnecessary response wrappers or custom exception frameworks.

### Step 7: Installation and Execution

Provide exact instructions for running the application locally.

Include:

1. Python virtual environment creation.
2. Virtual environment activation for Windows and macOS/Linux.
3. Installation using `requirements.txt`.
4. MongoDB Atlas connection configuration.
5. Running the FastAPI application with Uvicorn.
6. Opening the Swagger UI at `/docs`.
7. Testing every CRUD operation through Swagger UI.

Include the exact terminal commands.

### Step 8: Testing

Explain how to test all five CRUD operations using Swagger UI.

Provide sample request bodies and expected responses based on the employee fields I confirm.

Show how to verify that records are actually created, updated, retrieved, and deleted in MongoDB Atlas.

Do not invent employee fields or sample values before confirming the schema.

## 4. Code Quality Requirements

The final code must satisfy the following:

* Simple and readable Python code.
* Correct FastAPI and PyMongo usage.
* Proper MongoDB ObjectId handling.
* Pydantic request validation.
* Correct HTTP status codes.
* Clear error handling.
* No hardcoded secrets.
* No unnecessary dependencies.
* No unnecessary features.
* No incomplete functions or placeholder implementations.
* No pseudocode in place of working code.
* No deprecated APIs when a supported alternative is available.

Ensure all imports, filenames, function names, and variable names are consistent across the project.

Check the complete application for common errors before presenting it.

## 5. Output Format

Present the final solution in this exact order:

1. Confirmed requirements.
2. API endpoints.
3. Project folder structure.
4. Installation commands.
5. `requirements.txt`
6. `.env` configuration.
7. `.gitignore`
8. Complete code for `database.py`.
9. Complete code for `models.py`.
10. Complete code for `main.py`.
11. Instructions to run the application.
12. Swagger UI testing instructions for all CRUD operations.
13. Expected responses and common errors.

For every file, provide its filename and complete code in a separate code block.

Do not skip code or say "continue similarly."

## 6. Final Instruction

First, review my requirements and ask the essential clarification questions.

Do not generate the application code until I have answered those questions.

The goal is a fully working, minimal FastAPI + MongoDB Atlas CRUD application that is easy to understand, test, and extend.
