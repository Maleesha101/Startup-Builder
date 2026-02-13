import json
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel


class AgentResult(BaseModel):
    agent_name: str
    output: Any
    artifact_type: str
    artifact_content: str  # String representation for saving to file


class BaseAgent:
    def __init__(self, model_name: str = "gemini-2.0-flash-001"):
        self.llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.7)

    async def run(self, context: Dict[str, Any]) -> AgentResult:
        raise NotImplementedError


# --- Specialized Agents ---


class ProductAgent(BaseAgent):
    """
    Elicits product vision, defines features, user flows, and personas.
    """

    async def run(self, context: Dict[str, Any]) -> AgentResult:
        idea = context.get("idea", "")
        prompt = ChatPromptTemplate.from_template(
            """
            You are a rigorous Product Manager. 
            Analyze the following startup idea: "{idea}"
            
            Produce a prioritized feature list for an MVP.
            Return ONLY valid JSON with this structure:
            {{
                "features": [
                    {{
                        "id": "F-01",
                        "title": "Feature Name",
                        "description": "Description of the feature",
                        "priority": "MUST",
                        "acceptance_criteria": ["Criteria 1", "Criteria 2"]
                    }}
                ]
            }}
            """
        )
        chain = prompt | self.llm | StrOutputParser()
        result = await chain.ainvoke({"idea": idea})
        # Clean JSON markdown if present
        clean_json = result.replace("```json", "").replace("```", "").strip()
        return AgentResult(
            agent_name="Product Agent",
            output=json.loads(clean_json),
            artifact_type="prioritized_features.json",
            artifact_content=clean_json,
        )


class ArchitectureAgent(BaseAgent):
    """
    Chooses tech stack and creates project structure.
    """

    async def run(self, context: Dict[str, Any]) -> AgentResult:
        features = context.get("product_features", {})
        prompt = ChatPromptTemplate.from_template(
            """
            You are a Senior System Architect.
            Based on these product features: {features}
            
            1. Recommend a tech stack (Frontend, Backend, Database, Cloud).
            2. specific python packages for backend.
            3. project structure.

            Return a valid JSON object:
            {{
                "tech_stack": {{ "frontend": "...", "backend": "...", "database": "..." }},
                "architecture_diagram_description": "...",
                "file_structure": ["api/main.py", "frontend/App.tsx", ...]
            }}
            """
        )
        chain = prompt | self.llm | StrOutputParser()
        result = await chain.ainvoke({"features": json.dumps(features)})
        clean_json = result.replace("```json", "").replace("```", "").strip()
        return AgentResult(
            agent_name="Architecture Agent",
            output=json.loads(clean_json),
            artifact_type="architecture.json",
            artifact_content=clean_json,
        )


class TimelineAgent(BaseAgent):
    """
    Breaks product into tasks and estimates time.
    """

    async def run(self, context: Dict[str, Any]) -> AgentResult:
        features = context.get("product_features", {})
        arch = context.get("architecture", {})
        prompt = ChatPromptTemplate.from_template(
            """
            You are a Project Manager.
            Features: {features}
            Architecture: {arch}
            
            Break this down into development tasks.
            Return a CSV string (header: id,task,role,hours,dependency).
            """
        )
        chain = prompt | self.llm | StrOutputParser()
        result = await chain.ainvoke(
            {"features": json.dumps(features), "arch": json.dumps(arch)}
        )
        return AgentResult(
            agent_name="Timeline Agent",
            output=result,  # CSV string
            artifact_type="tasks.csv",
            artifact_content=result,
        )


class FinanceAgent(BaseAgent):
    """
    Estimates costs.
    """

    async def run(self, context: Dict[str, Any]) -> AgentResult:
        timeline = context.get("timeline", "")
        prompt = ChatPromptTemplate.from_template(
            """
            You are a Startup CFO.
            Based on this task list/timeline:
            {timeline}
            
            Estimate monthly burn and one-time costs.
            Return a CSV string (header: item,type,cost_low,cost_high,notes).
            """
        )
        chain = prompt | self.llm | StrOutputParser()
        result = await chain.ainvoke({"timeline": timeline})
        return AgentResult(
            agent_name="Finance Agent",
            output=result,
            artifact_type="cost_estimate.csv",
            artifact_content=result,
        )


class MarketingAgent(BaseAgent):
    """
    Creates launch strategy.
    """

    async def run(self, context: Dict[str, Any]) -> AgentResult:
        features = context.get("product_features", {})
        idea = context.get("idea", "")
        prompt = ChatPromptTemplate.from_template(
            """
            You are a Growth Marketer.
            Idea: {idea}
            Features: {features}
            
            Create a launch plan in Markdown.
            Include: Target Audience, Channels, tagline, and 4-week launch calendar.
            """
        )
        chain = prompt | self.llm | StrOutputParser()
        result = await chain.ainvoke({"idea": idea, "features": json.dumps(features)})
        return AgentResult(
            agent_name="Marketing Agent",
            output=result,
            artifact_type="launch_plan.md",
            artifact_content=result,
        )
