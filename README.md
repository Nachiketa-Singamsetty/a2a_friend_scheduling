# A2A Friend Scheduling Demo

A multi-agent application demonstrating how to orchestrate conversations between different agents to schedule pickleball games among friends.

## Overview

This application contains four specialized agents that work together to coordinate scheduling:

- **Host Agent**: The primary orchestrator that coordinates the scheduling task
- **Karley Agent**: Manages Karley's calendar and availability preferences  
- **Nate Agent**: Handles Nate's schedule using CrewAI framework
- **Kaitlynn Agent**: Manages Kaitlynn's availability using LangGraph
- **Oliwia Agent**: Handles Oliwia's schedule using Azure OpenAI and Agents SDK

## Features

- **Multi-Agent Communication**: Agents communicate using the A2A (Agent-to-Agent) protocol
- **Different AI Frameworks**: Demonstrates integration of various AI frameworks:
  - Google ADK (Agent Development Kit)
  - CrewAI
  - LangGraph
  - OpenAI Agents SDK with Azure OpenAI
- **Real-time Scheduling**: Agents check availability and coordinate optimal meeting times
- **Court Booking**: Integrated pickleball court availability and booking system

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Host Agent    │◄──►│  Karley Agent   │    │   Nate Agent    │
│   (Orchestrator)│    │   (Google ADK)  │    │   (CrewAI)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐    ┌─────────────────┐
         └──────────────►│ Kaitlynn Agent  │    │  Oliwia Agent   │
                        │  (LangGraph)    │    │ (Azure OpenAI)  │
                        └─────────────────┘    └─────────────────┘
```

## Setup and Installation

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager
- API keys for:
  - Google AI (for most agents)
  - Azure OpenAI (for Oliwia agent)

### Environment Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Nachiketa-Singamsetty/a2a_friend_scheduling.git
   cd a2a_friend_scheduling
   ```

2. **Create environment file:**
   Create a `.env` file in the root directory with your API keys:
   ```env
   # Google API Key (required for most agents)
   GOOGLE_API_KEY=your_google_api_key_here

   # Azure OpenAI Configuration (required for Oliwia agent)
   AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
   AZURE_OPENAI_API_VERSION=2025-03-01-preview
   AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
   ```

## Running the Agents

You need to run each agent in a separate terminal window:

### Terminal 1: Karley Agent (Port 10002)
```bash
cd karley_agent_adk
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv run --active .
```

### Terminal 2: Nate Agent (Port 10003)
```bash
cd nate_agent_crewai
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv run --active .
```

### Terminal 3: Kaitlynn Agent (Port 10004)
```bash
cd kaitlynn_agent_langgraph
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv run --active app/__main__.py
```

### Terminal 4: Oliwia Agent (Port 10005)
```bash
cd oliwia_agent_azure
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv run --active app/__main__.py
```

### Terminal 5: Host Agent (Port 8000)
```bash
cd host_agent_adk
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv run --active adk web
```

## Usage

Once all agents are running, the host agent will be available at `http://localhost:8000`. You can interact with it to:

1. **Schedule a pickleball game** by asking it to find a time when all friends are available
2. **Check individual availability** by asking about specific friends
3. **Book courts** once a time is agreed upon

### Example Interaction

```
User: "Can you help me schedule a pickleball game with my friends for this weekend?"

Host Agent: "I'll check everyone's availability for this weekend and find the best time for all of you to play pickleball."
```

## Agent Personalities

- **Karley**: Available most times, very flexible
- **Nate**: Prefers evenings on weekdays, more free on weekends  
- **Kaitlynn**: Available evenings on weekdays, flexible on weekends
- **Oliwia**: Prefers afternoons and weekends, avoids mornings

## Technical Details

### Frameworks Used

- **Google ADK**: For Karley and Host agents
- **CrewAI**: For Nate's agent with structured task management
- **LangGraph**: For Kaitlynn's agent with graph-based workflows
- **OpenAI Agents SDK**: For Oliwia's agent with Azure OpenAI integration

### Communication Protocol

All agents communicate using the A2A (Agent-to-Agent) protocol, enabling:
- Real-time message streaming
- Task coordination
- Status updates
- Error handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with all agents running
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

### Common Issues

1. **Port conflicts**: Make sure each agent is running on its designated port
2. **API key errors**: Verify your `.env` file has correct API keys
3. **Connection errors**: Ensure all agents are running before starting the host agent

### Getting Help

If you encounter issues:
1. Check the agent logs for error messages
2. Verify all environment variables are set correctly
3. Ensure all dependencies are installed with `uv pip install -e .`

## Future Enhancements

- [ ] Add more sophisticated scheduling algorithms
- [ ] Implement calendar integration
- [ ] Add notification systems
- [ ] Support for recurring games
- [ ] Mobile app interface