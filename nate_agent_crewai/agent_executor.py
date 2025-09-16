from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
    InternalError,
    InvalidParamsError,
    Part,
    TaskState,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils.errors import ServerError
from agent import SchedulingAgent


class SchedulingAgentExecutor(AgentExecutor):
    """AgentExecutor for the scheduling agent."""

    def __init__(self):
        """Initializes the SchedulingAgentExecutor."""
        self.agent = SchedulingAgent()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Executes the scheduling agent."""
        if not context.task_id or not context.context_id:
            raise ValueError("RequestContext must have task_id and context_id")
        if not context.message:
            raise ValueError("RequestContext must have a message")

        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        if not context.current_task:
            await updater.submit()
        await updater.start_work()

        if not self._validate_request(context):
            raise ServerError(error=InvalidParamsError())

        query = context.get_user_input()
        
        try:
            # Simulate streaming by sending a working status first
            working_parts = [Part(root=TextPart(text="Checking Nate's availability..."))]
            await updater.update_status(
                TaskState.working,
                message=updater.new_agent_message(working_parts),
            )
            
            # Add a small delay to simulate processing
            import asyncio
            await asyncio.sleep(1)
            
            result = self.agent.invoke(query)
            print(f"Final Result ===> {result}")
            
            # Send the final result
            parts = [Part(root=TextPart(text=result))]
            await updater.add_artifact(parts)
            await updater.complete()
            
        except Exception as e:
            print(f"Error invoking agent: {e}")
            error_parts = [Part(root=TextPart(text=f"Error: {str(e)}"))]
            await updater.add_artifact(error_parts)
            await updater.complete()

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handles task cancellation."""
        raise ServerError(error=UnsupportedOperationError())

    def _validate_request(self, context: RequestContext) -> bool:
        """Validates the request context."""
        return True
