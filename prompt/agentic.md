You are an expert Agentic AI developer.

I want to build an Agentic AI application.

Application:
[Describe the problem you want the agent to solve]

Goal:
[Clearly describe the final goal]

Available tools:
[List the tools the agent can use]

The agent must:

1. Understand the user's request.
2. Decide what information is required.
3. Decide which tool should be used.
4. Use the required tool.
5. Check the tool result.
6. Decide whether another action is required.
7. Continue until the task is completed.
8. Give the final answer to the user.

Rules:

* Do not invent information.
* Do not invent tool results.
* Use tools when real information is required.
* Do not use a tool unnecessarily.
* If required information is missing, ask the user.
* If a tool fails, clearly report the failure.
* Do not claim that an action was completed unless it actually succeeded.
* Do not assume that a tool, API, database, or function exists unless it is provided.
* Clearly separate tool results from the final response.
* Keep the final response simple and clear.

Development requirements:

* Use Python.
* Use [LangGraph / LangChain / other framework].
* Provide the project architecture.
* Provide the project structure.
* Provide complete working code.
* Explain each agent, tool, and workflow.
* Provide API endpoints if required.
* Provide test commands.
* Provide sample user requests and expected results.

Before writing the code:

1. Explain the agent's workflow.
2. Identify the agents and tools required.
3. Explain when each tool will be used.
4. Identify any missing information.
5. Then develop the application step-by-step.


ROLE       → Who is the AI?
GOAL       → What should it achieve?
TOOLS      → What can it use?
STEPS      → What should it do?
DECISION   → When should it use a tool?
RULES      → What must it NOT do?
OUTPUT     → What should it return?