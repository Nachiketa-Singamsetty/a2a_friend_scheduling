#!/usr/bin/env python3
"""
Simple test script for Oliwia Agent
"""
import asyncio
import os
from dotenv import load_dotenv
from app.agent import OliwiaAgent

load_dotenv()

async def test_oliwia_agent():
    """Test the Oliwia agent with sample queries."""
    agent = OliwiaAgent()
    
    test_queries = [
        "Are you free to play pickleball tomorrow?",
        "What's your availability for this weekend?",
        "Can you play pickleball next Tuesday at 3pm?",
        "What's your schedule like for the next few days?"
    ]
    
    print("Testing Oliwia Agent...")
    print("=" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nTest {i}: {query}")
        print("-" * 30)
        
        try:
            result = await agent.invoke(query, f"test_context_{i}")
            print(f"Response: {result['content']}")
            print(f"Task Complete: {result['is_task_complete']}")
        except Exception as e:
            print(f"Error: {e}")
        
        print()

if __name__ == "__main__":
    # Check required environment variables
    required_vars = ["AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please create a .env file with the required Azure OpenAI configuration.")
        exit(1)
    
    asyncio.run(test_oliwia_agent())
