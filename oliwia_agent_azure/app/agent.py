import random
from collections.abc import AsyncIterable
from datetime import date, datetime, timedelta
from typing import Any, Literal
import asyncio
import os

from openai import AsyncAzureOpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
from agents import Agent, Runner, set_default_openai_client, function_tool

# Load environment variables from the root .env file
import pathlib
root_dir = pathlib.Path(__file__).parent.parent.parent
env_path = root_dir / ".env"
load_dotenv(dotenv_path=env_path)

# Initialize Azure OpenAI client
client = AsyncAzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2025-03-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT") or "",
)

# Set the default OpenAI client for the Agents SDK
set_default_openai_client(client)

# Disable tracing to avoid API key issues
os.environ["OPENAI_TRACING"] = "false"


def generate_oliwias_calendar() -> dict[str, list[str]]:
    """Generates Oliwia's calendar for the next 7 days with afternoon/weekend preferences."""
    calendar = {}
    today = date.today()
    
    for i in range(7):
        current_date = today + timedelta(days=i)
        date_str = current_date.strftime("%Y-%m-%d")
        day_of_week = current_date.weekday()  # Monday is 0 and Sunday is 6

        if day_of_week < 5:  # Weekday - limited afternoon availability
            possible_times = [f"{h:02}:00" for h in range(14, 19)]  # 2 PM to 6 PM
            available_slots = sorted(
                random.sample(possible_times, random.randint(2, 3))
            )
        else:  # Weekend - more flexible afternoon availability
            possible_times = [f"{h:02}:00" for h in range(12, 20)]  # 12 PM to 8 PM
            available_slots = sorted(
                random.sample(possible_times, random.randint(4, 6))
            )

        calendar[date_str] = available_slots
    
    return calendar


OLIWIA_CALENDAR = generate_oliwias_calendar()


@function_tool
def get_availability(date_range: str) -> str:
    """Use this to get Oliwia's availability for a given date or date range.
    
    Args:
        date_range: The date or date range to check for availability, e.g., '2024-07-28' or '2024-07-28 to 2024-07-30'.
    """
    dates_to_check = [d.strip() for d in date_range.split("to")]
    start_date_str = dates_to_check[0]
    end_date_str = dates_to_check[-1]

    try:
        start = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        if start > end:
            return "Invalid date range. The start date cannot be after the end date."

        results = []
        delta = end - start
        for i in range(delta.days + 1):
            day = start + timedelta(days=i)
            date_str = day.strftime("%Y-%m-%d")
            available_slots = OLIWIA_CALENDAR.get(date_str, [])
            if available_slots:
                availability = f"Oliwia is available on {date_str} at {', '.join(available_slots)}."
                results.append(availability)
            else:
                results.append(f"Oliwia is not available on {date_str}.")

        return "\n".join(results)

    except ValueError:
        return (
            "I couldn't understand the date. "
            "Please ask to check availability for a date like 'YYYY-MM-DD'."
        )





class ResponseFormat(BaseModel):
    """Respond to the user in this format."""

    status: Literal["input_required", "completed", "error"] = "input_required"
    message: str


class OliwiaAgent:
    """OliwiaAgent - a specialized assistant for scheduling using OpenAI Agents SDK."""

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

    SYSTEM_INSTRUCTION = (
        "You are Oliwia's scheduling assistant. "
        "Your sole purpose is to use the 'get_availability' function to answer questions about Oliwia's schedule for playing pickleball. "
        "You will be provided with the current date to help you understand relative date queries like 'tomorrow' or 'next week'. "
        "Use this information to correctly call the function with a specific date (e.g., 'YYYY-MM-DD'). "
        "When you get the availability result, format your response exactly like this: 'Yes, Oliwia is available to play pickleball on [DATE] at [TIMES].' "
        "List the specific times from the availability result, separated by commas. "
        "Do not add extra commentary about preferences or flexibility. "
        "If the user asks about anything other than scheduling pickleball, "
        "politely state that you cannot help with that topic and can only assist with scheduling queries. "
        "Do not attempt to answer unrelated questions or use functions for other purposes."
    )

    def __init__(self):
        self.agent = Agent(
            name="OliwiaScheduler",
            instructions=self.SYSTEM_INSTRUCTION,
            tools=[get_availability],
            model="gpt-4o-mini"
        )

    async def invoke(self, query, context_id):
        """Invoke the agent with a query and return the response."""
        today_str = f"Today's date is {date.today().strftime('%Y-%m-%d')}."
        augmented_query = f"{today_str}\n\nUser query: {query}"
        
        try:
            result = await Runner.run(self.agent, augmented_query)
            return {
                "is_task_complete": True,
                "require_user_input": False,
                "content": result.final_output
            }
        except Exception as e:
            return {
                "is_task_complete": False,
                "require_user_input": True,
                "content": f"Sorry, I encountered an error: {str(e)}"
            }

    async def stream(self, query, context_id) -> AsyncIterable[dict[str, Any]]:
        """Stream the agent's response to a given query."""
        today_str = f"Today's date is {date.today().strftime('%Y-%m-%d')}."
        augmented_query = f"{today_str}\n\nUser query: {query}"
        
        try:
            # First, yield a processing message
            yield {
                "is_task_complete": False,
                "require_user_input": False,
                "content": "Checking Oliwia's availability...",
            }
            
            await asyncio.sleep(1)  # Simulate processing time
            
            # Use the async invoke method and simulate streaming
            result = await self.invoke(query, context_id)
            
            # Simulate streaming by yielding the result
            yield {
                "is_task_complete": result["is_task_complete"],
                "require_user_input": result["require_user_input"],
                "content": result["content"]
            }
            
        except Exception as e:
            yield {
                "is_task_complete": False,
                "require_user_input": True,
                "content": f"Sorry, I encountered an error: {str(e)}"
            }
