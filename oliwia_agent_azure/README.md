# Oliwia Agent - Azure OpenAI Implementation

Oliwia is a friendly and flexible scheduling assistant for pickleball games, implemented using Azure OpenAI's GPT-4o-mini model. She prefers afternoons and weekends, avoids mornings, and collaborates to resolve conflicts.

## Features

- **Azure OpenAI Integration**: Uses GPT-4o-mini model via AsyncAzureOpenAI client
- **A2A Protocol Support**: Full compatibility with Agent-to-Agent communication
- **Streaming Support**: Real-time response streaming
- **Push Notifications**: Supports push notification capabilities
- **Cloud-Ready**: Designed for cloud deployment with configurable endpoints

## Scheduling Preferences

Oliwia has the following scheduling preferences:
- **Preferred Times**: 14:00-18:00 (2 PM - 6 PM)
- **Avoid Times**: Before 10:00 AM
- **Preferred Days**: Saturday, Sunday
- **Personality**: Collaborative, flexible, friendly

## Environment Variables

Create a `.env` file in the `oliwia_agent_azure` directory with the following variables:

```env
# Required Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://vwo-divyanshu-resource.openai.azure.com
AZURE_OPENAI_API_VERSION=2025-03-01-preview
AZURE_OPENAI_DEPLOYMENT=gpt-4.1-mini

# Optional Configuration
PORT=10005
AGENT_HOST_URL=https://your-deployed-agent-url.com
```

## Local Development

### Setup and Installation

```bash
cd oliwia_agent_azure
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### Running the Agent

```bash
uv run --active app/__main__.py
```

### Testing

Test the agent locally before deployment:

```bash
python test_agent.py
```

## Cloud Deployment

The agent is designed to run on cloud platforms with multiple deployment options:

### Option 1: Azure Container Instances

1. Build and push the container to Azure Container Registry:
   ```bash
   docker build -t oliwia-agent .
   docker tag oliwia-agent your-registry.azurecr.io/oliwia-agent
   docker push your-registry.azurecr.io/oliwia-agent
   ```

2. Deploy using Azure Container Instances with environment variables configured

### Option 2: Azure App Service

1. Create a new App Service
2. Configure environment variables in App Service settings
3. Deploy the code using Azure CLI or GitHub Actions

### Option 3: Azure Functions

1. Convert the agent to use Azure Functions runtime
2. Deploy as a serverless function

### Docker Deployment

The project includes a `Dockerfile` for containerized deployment:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
# ... (see Dockerfile for complete configuration)
EXPOSE 10005
CMD [".venv/bin/python", "-m", "app"]
```

## Agent Card

The agent advertises the following capabilities:
- **Name**: Oliwia Agent
- **Description**: Friendly and flexible scheduling assistant for pickleball games
- **Capabilities**: Streaming, Push Notifications
- **Framework**: Azure OpenAI 4.1-mini
- **Port**: 10005 (configurable)

## Integration with Host Agent

The Host Agent has been updated to include Oliwia's endpoint. To integrate Oliwia with the Host Agent, add her endpoint to the friend agent URLs in the Host Agent configuration:

```python
friend_agent_urls = [
    "http://localhost:10002",  # Karley's Agent
    "http://localhost:10003",  # Nate's Agent
    "http://localhost:10004",  # Kaitlynn's Agent
    "https://vwo-divyanshu-resource.openai.azure.com/openai/deployments/gpt-4.1-mini",  # Oliwia's Agent
]
```

## Health Check

The agent exposes a health check endpoint at `/health` for monitoring purposes.

## Project Structure

```
oliwia_agent_azure/
├── app/
│   ├── __init__.py
│   ├── agent.py              # Core agent logic with Azure OpenAI
│   ├── agent_executor.py     # A2A protocol adapter
│   └── __main__.py          # Server entry point
├── __init__.py
├── pyproject.toml           # Dependencies (Azure OpenAI, A2A SDK)
├── Dockerfile              # Container deployment
├── test_agent.py           # Test script
└── README.md              # This file
```

## Dependencies

- **a2a-sdk**: Agent-to-Agent communication protocol
- **openai**: Azure OpenAI client
- **pydantic**: Data validation
- **uvicorn**: ASGI server
- **httpx**: HTTP client
- **python-dotenv**: Environment variable management

## Troubleshooting

### Common Issues

1. **Deployment Not Found (404)**: Ensure the Azure OpenAI deployment `gpt-4.1-mini` exists in your Azure resource
2. **Missing API Key**: Verify `AZURE_OPENAI_API_KEY` is set correctly
3. **Connection Timeout**: Check network connectivity and endpoint URL

### Testing

Use the provided `test_agent.py` script to verify the agent works correctly before deployment. The script will test various scheduling queries and show Oliwia's calendar generation.