import logging
import os
import sys

import httpx
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryPushNotifier, InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from app.agent import OliwiaAgent
from app.agent_executor import OliwiaAgentExecutor
from dotenv import load_dotenv

# Load environment variables from the root .env file
import pathlib
root_dir = pathlib.Path(__file__).parent.parent.parent
env_path = root_dir / ".env"
load_dotenv(dotenv_path=env_path)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MissingAPIKeyError(Exception):
    """Exception for missing API key."""


def main():
    """Starts Oliwia's Agent server."""
    host = os.getenv("HOST", "0.0.0.0")  # Listen on all interfaces for cloud deployment
    port = int(os.getenv("PORT", 10005))  # Default to 10005, configurable via env
    
    try:
        # Check for required Azure OpenAI environment variables
        required_env_vars = ["AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT"]
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        
        if missing_vars:
            raise MissingAPIKeyError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

        capabilities = AgentCapabilities(streaming=True, pushNotifications=True)
        skill = AgentSkill(
            id="schedule_pickleball",
            name="Pickleball Scheduling Tool",
            description="Helps with finding Oliwia's availability for pickleball games. Oliwia prefers afternoons and weekends, avoids mornings.",
            tags=["scheduling", "pickleball", "azure"],
            examples=[
                "Are you free to play pickleball on Saturday afternoon?",
                "Can you play pickleball next week?",
                "What's your availability for this weekend?"
            ],
        )
        
        # Use environment variable for the agent URL or default to localhost
        # For local development, always use localhost in the agent card URL
        agent_host_url = os.getenv("AGENT_HOST_URL") or f"http://localhost:{port}/"
        
        agent_card = AgentCard(
            name="Oliwia Agent",
            description="Oliwia is a friendly and flexible scheduling assistant for pickleball games. She prefers afternoons and weekends, avoids mornings, and collaborates to resolve conflicts.",
            url=agent_host_url,
            version="1.0.0",
            defaultInputModes=OliwiaAgent.SUPPORTED_CONTENT_TYPES,
            defaultOutputModes=OliwiaAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[skill],
        )

        httpx_client = httpx.AsyncClient()
        request_handler = DefaultRequestHandler(
            agent_executor=OliwiaAgentExecutor(),
            task_store=InMemoryTaskStore(),
            push_notifier=InMemoryPushNotifier(httpx_client),
        )
        server = A2AStarletteApplication(
            agent_card=agent_card, http_handler=request_handler
        )

        # Show localhost for local development, actual host for cloud
        display_host = "localhost" if host == "0.0.0.0" else host
        logger.info(f"Starting Oliwia Agent server on {display_host}:{port}")
        logger.info(f"Agent Card: {agent_card.name} - {agent_card.description}")
        logger.info(f"Azure OpenAI Endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
        logger.info(f"Deployment: {os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4.1-mini')}")
        
        uvicorn.run(server.build(), host=host, port=port)

    except MissingAPIKeyError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An error occurred during server startup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
