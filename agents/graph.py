from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.globals import set_verbose, set_debug
from dotenv import load_dotenv
import os
from agents.tools import PROJECT_ROOT
from rich import print
from agents.prompts import planner_prompt, architect_prompt, coder_system_prompt
from agents.states import Plan , TaskPlan, CoderState
from langgraph.graph import StateGraph
from agents.tools import *
from langgraph.constants import END

load_dotenv()

set_debug(True)
set_verbose(True)

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)

def planner_agent(state: dict) -> dict:
    users_prompt = state["user_prompt"]
    response = llm.with_structured_output(Plan).invoke(planner_prompt(users_prompt))
    if response is None:
        raise ValueError("Planner plan nai kar paya soory yawr")
    return {"plan": response}


def architect_agent(state: dict) -> dict:
    plan: Plan = state["plan"]
    response = llm.with_structured_output(TaskPlan, method="json_mode").invoke(architect_prompt(plan))
    if response is None:
        raise ValueError("Architecture architect nai kar paya soory yawr")
    response.plan = plan
    return {"task_plan": response}


def coder_agent(state: dict) -> dict:
    coder_state: CoderState = state.get("coder_state")
    if coder_state is None:
        coder_state = CoderState(
            task_plan=state["task_plan"],
            current_step_idx=0
        )
    steps = coder_state.task_plan.implementation_steps
   
    if coder_state.current_step_idx >= len(steps):
        return {
            "coder_state": coder_state,
            "status": "DONE"
        }

    current_task = steps[coder_state.current_step_idx]

    system_prompt = coder_system_prompt()

    user_prompt = (
    f"Task: {current_task.task_description}\n"
    f"File: {current_task.filepath}\n"
    "Inspect the existing project using the available tools and "
    "implement this task. Use write_file() to save your changes."
)
    coder_tools = [
        read_file,
        write_file,
        list_files,
        get_current_directory,
        run_cmd
    ]

    c_agent = create_agent(
        model=llm,
        tools=coder_tools,
        system_prompt=system_prompt
    )

    c_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    })

    # Current task is now completed
    coder_state.current_step_idx += 1

    # Check immediately after completing the task
    if coder_state.current_step_idx >= len(steps):
        status = "DONE"
    else:
        status = "CODING"

    return {
        "coder_state": coder_state,
        "status": status
    }

def has_existing_project() -> bool:
    return PROJECT_ROOT.exists() and any(PROJECT_ROOT.iterdir())

def route_entry(state: dict) -> str:
    return state.get("mode", "new")

def edit_agent(state: dict) -> dict:
    user_prompt = state["user_prompt"]
    system_prompt = coder_system_prompt()
    files_list = list_files.invoke({"directory": "."})
    task_prompt = (
        f"The user wants this change applied to the EXISTING project: {user_prompt}\n"
        f"Existing files:\n{files_list}\n"
        "Inspect the relevant file(s) with read_file(), make the necessary edits, "
        "and save changes using write_file(). Only modify files relevant to this request."
    )
    coder_tools = [read_file, write_file, list_files, get_current_directory, run_cmd]
    e_agent = create_agent(model=llm, tools=coder_tools, system_prompt=system_prompt)
    e_agent.invoke({"messages": [{"role": "user", "content": task_prompt}]})
    return {"status": "DONE"}

graph = StateGraph(dict)
graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)
graph.add_node("edit", edit_agent)
graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")
graph.add_edge("edit", END)
graph.add_conditional_edges(
    "coder",
    lambda s: "END" if s.get("status") == "DONE" else "coder",
    {"END": END, "coder": "coder"}
)
graph.set_conditional_entry_point(route_entry, {"new": "planner", "edit": "edit"})
agent = graph.compile()

if __name__ == "__main__":
    result = agent.invoke({"user_prompt": "Build a colourful modern todo app in html css and js"},
                          {"recursion_limit": 100})
    print("Final State:", result)
