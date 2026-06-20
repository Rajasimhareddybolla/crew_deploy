from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class ResearchToolInput(BaseModel):
    """Input schema for ResearchTool."""
    query: str = Field(..., description="The query topic to search for in the database.")


class ResearchTool(BaseTool):
    name: str = "Knowledge Base Search"
    description: str = (
        "Useful for searching facts and information about a topic in the local knowledge base."
    )
    args_schema: Type[BaseModel] = ResearchToolInput

    def _run(self, query: str) -> str:
        # Mock database of facts
        data = {
            "crewai": (
                "CrewAI is a leading framework for orchestrating role-playing, autonomous AI agents. "
                "It enables agents to collaborate, share tasks, and execute complex workflows seamlessly. "
                "Key features include role playing, memory, guardrails, and tool integration."
            ),
            "gemini": (
                "Google Gemini is a family of highly capable multimodal AI models developed by Google. "
                "It includes models like Gemini 1.5 Flash (optimized for speed and efficiency), "
                "Gemini 1.5 Pro (optimized for complex reasoning), and the Gemini 2.0/2.5 series."
            ),
            "uv": (
                "uv is an extremely fast Python package installer and resolver written in Rust. "
                "It is designed to replace pip, pip-tools, virtualenv, and poetry. "
                "It is developed by Astral and is known for being 10-100x faster than traditional pip."
            )
        }
        
        normalized_query = query.lower()
        results = []
        for key, description in data.items():
            if key in normalized_query or normalized_query in key:
                results.append(f"[{key.upper()} FACT]: {description}")
        
        if results:
            return "\n\n".join(results)
        
        return f"No specific facts found for '{query}' in the local knowledge base. Please generic research instead."
