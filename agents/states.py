from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class File(BaseModel):
    path: str = Field(
        description=(
            "The exact relative path where this file should be created "
            "inside the generated project, including the filename and extension."
        )
    )

    purpose: str = Field(
        description=(
            "Clearly describe the purpose and responsibility of this file "
            "in the project, including what functionality or logic it will contain."
        )
    )


class Plan(BaseModel):
    project_objective: str
    core_features: list[str]
    user_interactions: list[str]
    components: list[str]
    technologies: list[str]
    data_state_requirements: list[str]
    dependencies: list[str]
    implementation_steps: list[str]
    edge_cases: list[str]

    files: list[File] = Field(
        description=(
            "A complete list of all files required to build the project, "
            "including the exact file path and purpose of each file."
        )
    )

class ImplementationTask(BaseModel):
    filepath: str = Field(
        description=(
            "The exact relative path of the file that this implementation "
            "task applies to. Example: 'src/components/Calculator.tsx'."
        )
    )

    task_description: str = Field(
        description=(
            "A detailed description of what the Coder Agent must implement "
            "in this file. Include the required logic, components, functions, "
            "classes, variables, imports, and how this file connects with "
            "other files. Do not provide the actual code."
        )
    )

class TaskPlan(BaseModel):
    implementation_steps: list[ImplementationTask] = Field(description="A list of steps to be taken to implement the task")
    model_config = ConfigDict(extra="allow")

class CoderState(BaseModel):
    task_plan: TaskPlan = Field(description="The plan for the task to be implemented")
    current_step_idx: int = Field(0, description="The index of the current step in the implementation steps")
    current_file_content: Optional[str] = Field(None, description="The content of the file currently being edited or created")