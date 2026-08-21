# AI Autonomous Software Engineer

An autonomous AI software engineering system that transforms natural-language software requirements into structured, functional projects through a multi-agent workflow.

The system uses LangGraph to orchestrate specialized agents for planning, architecture design, code generation, tool execution, and iterative reflection. A FastAPI backend manages requests and real-time updates, while generated projects can be previewed and downloaded through the web interface.

**Live Demo:**
https://devin-clone-oe17.onrender.com/

**Demo Video:**

---

## Overview

The AI Autonomous Software Engineer is designed to automate multiple stages of the software development lifecycle.

Instead of directly generating code from a single prompt, the system divides the development process into specialized stages:

```text
User Requirement
       |
       v
Planner Agent
       |
       v
Architect Agent
       |
       v
Coder Agent
       |
       v
Tool Execution
       |
       v
Reflection / Iteration
       |
       v
Generated Project
       |
       +----> Live Preview
       |
       +----> Project Download
```

The workflow allows the system to reason about a requirement, create a development plan, determine the required architecture, implement the project, interact with the development environment, and iterate when necessary.

---

## System Architecture and Workflow

The following diagram represents the complete system architecture and execution workflow.

<img width="1024" height="682" alt="image" src="https://github.com/user-attachments/assets/0fd9e47e-ab72-4e0a-8b2a-ded6dabe1890" />


### Workflow

1. The user submits a software requirement through the web interface.
2. The FastAPI backend receives the request through the REST API.
3. The task orchestrator initializes the LangGraph workflow and manages the execution state.
4. The Planner Agent analyzes the requirement and creates a structured development plan.
5. The Architect Agent converts the plan into a system architecture and project structure.
6. The Coder Agent generates and modifies the required source code.
7. Agents interact with development tools for file operations, command execution, and code inspection.
8. LangGraph state maintains the relevant execution context throughout the workflow.
9. The reflection loop allows the system to re-plan and modify the implementation when required.
10. WebSocket communication provides real-time execution updates to the frontend.
11. The generated application is served for live preview.
12. The completed project can be downloaded as a ZIP archive.

---

## Multi-Agent Architecture

### Planner Agent

The Planner Agent is responsible for understanding the user's requirements and converting them into an actionable development plan.

Responsibilities include:

* Understanding the software requirement
* Identifying required functionality
* Decomposing the requirement into tasks
* Creating a structured execution plan

Implementation:

```text
agents/prompts.py
agents/graph.py
```

### Architect Agent

The Architect Agent converts the development plan into a technical design.

Responsibilities include:

* Designing the system architecture
* Identifying application components
* Defining the project structure
* Determining required files and modules
* Establishing relationships between components

Implementation:

```text
agents/prompts.py
agents/graph.py
```

### Coder Agent

The Coder Agent implements the architecture produced by the previous stages.

Responsibilities include:

* Generating source code
* Creating files and directories
* Modifying existing files
* Reading project files for context
* Executing development commands
* Addressing implementation errors

Implementation:

```text
agents/graph.py
agents/tools.py
```

### Reflection and Iteration

The system includes an iterative execution loop rather than relying on a single code-generation step.

```text
Planning
   |
Architecture
   |
Implementation
   |
Tool Execution
   |
Evaluation
   |
   +---- Problem detected ----> Re-plan / Modify
   |
   +---- No problem ----------> Final Project
```

This allows the workflow to continue refining the generated project when an implementation issue is detected.

---

## Tools and Integrations

The agent system can interact with the development environment through a set of tools.

### File System Operations

The system can perform operations such as:

* Creating files
* Reading files
* Writing files
* Editing files
* Creating directories

### Command Execution

The system can execute development commands required during project generation, including:

* Installing dependencies
* Running applications
* Building projects
* Executing scripts
* Running development commands

### Code Search and Read

The agents can inspect existing project files and retrieve relevant code for contextual decision-making and modification.

### External LLM

The system uses Google Gemini as the underlying language model for agent reasoning and structured outputs.

---

## State Management

LangGraph state is used to maintain information throughout the execution workflow.

The state can contain information such as:

* User requirements
* Development plan
* Architecture information
* Agent outputs
* Execution context
* Generated project information
* Workflow status

This shared state allows the different agents to operate as part of a coordinated workflow rather than as isolated model calls.

---

## Backend

The backend is implemented using FastAPI.

It is responsible for:

* Receiving generation requests
* Initializing the agent workflow
* Managing execution
* Streaming real-time updates
* Serving generated project files
* Providing project preview and download functionality

### API Endpoints

```text
POST /generate
```

Starts a project-generation request.

```text
WebSocket /ws
```

Provides real-time workflow updates to the frontend.

---

## Real-Time Execution

The application provides real-time visibility into the agent workflow through WebSocket communication.

The frontend can receive updates as the system progresses through stages such as:

```text
Planner
   |
Architect
   |
Coder
   |
Execution
   |
Reflection
   |
Completion
```

This allows users to monitor the generation process rather than waiting for the entire workflow to complete before receiving feedback.

---

## Generated Project

The system generates a structured project based on the user's requirements.

For example:

```text
generated_project/
├── index.html
├── style.css
└── script.js
```

The generated project can then be:

* Previewed through the web interface
* Served through the backend
* Downloaded as a ZIP archive
* Further modified through the agent workflow

---

## Project Structure

```text
AI-AUTONOMOUS-SOFTWARE-ENGINEER/
|
├── agents/
│   ├── graph.py
│   ├── prompts.py
│   ├── tools.py
│   ├── states.py
│   └── __init__.py
|
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
|
├── generated_project/
│   └── Generated application files
|
├── main.py
├── server.py
├── pyproject.toml
├── uv.lock
├── .env
└── README.md
```

---

## Technology Stack

| Component               | Technology            |
| ----------------------- | --------------------- |
| Programming Language    | Python                |
| Agent Orchestration     | LangGraph             |
| Language Model          | Google Gemini         |
| Backend Framework       | FastAPI               |
| Real-Time Communication | WebSocket             |
| Data Validation         | Pydantic              |
| Dependency Management   | uv                    |
| Frontend                | HTML, CSS, JavaScript |
| Version Control         | Git, GitHub           |

---

## Installation

### Prerequisites

* Python 3.x
* uv
* Git
* Google Gemini API key

### Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd AI-AUTONOMOUS-SOFTWARE-ENGINEER
```

### Install Dependencies

The project uses `uv` for dependency management.

```bash
uv sync
```

To add a new dependency:

```bash
uv add <package-name>
```

---

## Environment Configuration

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Do not commit the `.env` file or expose API keys in the repository.

---

## Running the Application

Run the project using:

```bash
uv run python main.py
```

If the FastAPI server is started directly:

```bash
uv run uvicorn server:app --reload
```

The exact command depends on the configured application entry point.

---

## Example

A user can provide a requirement such as:

```text
Build a task management web application
with a dashboard, task creation, task deletion,
and a responsive user interface.
```

The system processes the request through the agent workflow:

```text
Requirement
     |
     v
Planner
     |
     v
Architect
     |
     v
Coder
     |
     v
Tools
     |
     v
Reflection
     |
     v
Generated Application
```

The resulting project can then be previewed and downloaded.

---

## Key Features

* Multi-agent software development workflow
* Requirement decomposition
* Automated architecture planning
* Automated code generation
* File system interaction
* Command execution
* Code inspection
* Iterative reflection
* LangGraph state management
* FastAPI backend
* WebSocket-based real-time updates
* Generated project preview
* Generated project download
* Gemini-based structured agent outputs
* `uv`-based dependency management

---

## Design Approach

The primary design goal is to separate software development responsibilities across specialized agents.

Instead of relying on one model call to perform the entire task, the system follows a structured workflow:

```text
Requirement Analysis
        |
        v
Task Planning
        |
        v
System Architecture
        |
        v
Implementation
        |
        v
Tool Interaction
        |
        v
Evaluation and Reflection
        |
        v
Final Project
```

This architecture provides clear separation of responsibilities and makes the agent workflow easier to extend with additional capabilities such as testing, code review, debugging, and deployment.

---

## Future Improvements

* Automated unit-test generation
* Automated test execution
* Automated debugging
* Dedicated code-review agent
* Git integration
* Automated dependency management
* Database-aware project generation
* Docker-based isolated execution
* Persistent project memory
* Multi-language project generation
* Deployment automation
* Improved security and command validation
* More advanced planning and reflection strategies

---

## Project Status

**Status:** Active Development

The project is currently being developed toward a more capable autonomous software engineering system with improved planning, implementation, testing, debugging, and execution capabilities.

---

## Author

**Prem Yelwande**

B.Tech Information Technology

Interests: AI/ML, Agentic AI, Software Engineering
