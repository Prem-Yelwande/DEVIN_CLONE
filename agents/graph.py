from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from rich import print
from pydantic import BaseModel

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

user_prompt = "build a scientific calculator web application"


class Plan(BaseModel):
    project_objective: str
    core_features: list[str]
    user_interactions: list[str]
    components: list[str]
    technologies: list[str]
    dependencies: list[str]
    implementation_steps: list[str]
    edge_cases: list[str]


planner_prompt = f"""
You are the Planner Agent in an autonomous AI software engineering system.

Your job is to analyze the user's request and create a clear implementation
plan for the software project.

User Request:
{user_prompt}

Create a practical plan that the Architect Agent can directly use.

Include:
1. Project objective
2. Core features
3. User interactions
4. Required pages/components
5. Required technologies/frameworks
6. Data/state requirements
7. Important dependencies
8. Step-by-step implementation tasks
9. Potential edge cases

Rules:
- Do NOT write actual code.
- Do NOT explain your reasoning.
- Do NOT add unnecessary features.
- Keep the plan specific and implementation-ready.
- Make reasonable technical decisions when the user does not specify them.
- If this is a modification to an existing project, focus only on the requested changes.
"""

structured_llm = llm.with_structured_output(
    Plan,
    method="function_calling"
)

response = structured_llm.invoke(planner_prompt)

print(response)
