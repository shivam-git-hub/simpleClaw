from typing import Union

from llm.base import LLM

from agents.base import Agent
from agents.tools import ToolRegistry


class AgentFactory:
    @staticmethod
    def create(
        agent_name: str,
        llm: LLM,
        system_prompt: str,
        tools: Union[ToolRegistry, None] = None,
        **kwargs,
    ) -> Agent:
        if agent_name not in Agent.registry:
            raise ValueError(
                f"Agent '{agent_name}' not found. "
                f"Available: {list(Agent.registry.keys())}"
            )

        agent_class = Agent.registry[agent_name]
        return agent_class(
            name=agent_name,
            llm=llm,
            system_prompt=system_prompt,
            tools=tools,
            **kwargs,
        )
