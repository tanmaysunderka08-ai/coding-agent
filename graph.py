from langgraph.graph import END, START, StateGraph

from agents.coder import run_coder
from agents.planner import run_planner
from agents.tester import run_tester
from state import AgentState


def after_test(state: AgentState):
    print(f"[graph] attempt={state.main_loop_count} exit={state.sandbox_exit_code}")
    if state.sandbox_exit_code == 0 or state.main_loop_count >= state.max_loops:
        return END
    return "planner"


# tester -> (passed or out of attempts? stop) -> planner -> coder -> tester
workflow = StateGraph(AgentState)
workflow.add_node("tester", run_tester)
workflow.add_node("planner", run_planner)
workflow.add_node("coder", run_coder)
workflow.add_edge(START, "tester")
workflow.add_edge("planner", "coder")
workflow.add_edge("coder", "tester")
workflow.add_conditional_edges("tester", after_test, {"planner": "planner", END: END})
app = workflow.compile()
