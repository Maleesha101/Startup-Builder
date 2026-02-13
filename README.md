# Multi-Agent Startup Builder

An AI-powered system that takes a product idea and spawns specialized agents (Product, Architecture, Finance, Timeline, Marketing) to generate a complete project prototype and plan.

## Features

- **Orchestrator**: Manages the agent workflow.
- **Specialized Agents**: 
  - 🧠 Product Agent: Defines features and requirements.
  - 🏗 Architecture Agent: Designs the tech stack.
  - 💰 Finance Agent: Estimates costs.
  - 📅 Timeline Agent: Plans tasks and milestones.
  - 📢 Marketing Agent: Creates a launch strategy.
- **Artifact Generation**: Produces JSON/Markdown/CSV plans and a project skeleton.

## Prerequisites

- Python 3.9+
- Google Gemini API Key

## Setup

1.  Navigate to the directory:
    ```bash
    cd startup_builder
    ```

2.  Install dependencies using `uv`:
    ```bash
    uv sync
    ```
    
    Or using pip (legacy):
    ```bash
    pip install .
    ```

3.  Set up environment variables:
    Create a `.env` file in `startup_builder/` with:
    ```env
    GOOGLE_API_KEY=your_api_key_here
    ```

## Running the App

4.  Start the backend:
    ```bash
    uv run uvicorn api.main:app --reload
    ```
2.  Open your browser to:
    `http://localhost:8000` (or the frontend URL provided in logs).

## Testing

Run tests with pytest:
```bash
pytest tests/
```
