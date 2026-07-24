from state.state import ProcurementState

def error_handler_node(state: ProcurementState):
    print("Workflow failed.")

    for error in state.get("errors", []):
        print(error)

    return state

