from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from one_agent_crew.tools.custom_tool import ResearchTool
import os
from dotenv import load_dotenv

load_dotenv()

@CrewBase
class OneAgentCrew():
    """OneAgentCrew crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    def __init__(self) -> None:
        # Load API key and Model from env or use defaults
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            api_key = api_key.strip('"').strip("'")
            
        model = os.getenv("MODEL", "gemini/gemini-1.5-flash")
        if model:
            model = model.strip('"').strip("'")
        
        self.gemini_llm = LLM(
            model=model,
            api_key=api_key
        )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True,
            llm=self.gemini_llm,
            tools=[ResearchTool()] # Assign custom tool to this agent
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the OneAgentCrew crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
