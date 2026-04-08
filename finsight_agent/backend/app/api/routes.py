from fastapi import APIRouter
from .. import schemas

router = APIRouter()

from ..agents import orchestrator

@router.post("/agent")
async def run_agent(request: schemas.AgentRequest):
    graph = orchestrator.create_graph()
    # Since there's no user, we can remove the email or use a placeholder if needed.
    # For now, we'll remove it from the inputs.
    inputs = {"query": request.query}

    # The graph runs asynchronously. In a real app, you might use websockets
    # or a task queue to notify the user when the run is complete.
    # For this implementation, we'll run it synchronously and return the final state.
    final_state = {}
    for output in graph.stream(inputs):
        for key, value in output.items():
            final_state[key] = value

    return {"status": "success", "final_state": final_state}
