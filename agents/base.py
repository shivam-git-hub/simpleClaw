from abc import ABC, abstractmethod

from llm.base import LLM

from agents.memory.main import Memory
from agents.tools import ToolRegistry
from agents.types import Role


class Agent(ABC):
    registry: dict[str, type["Agent"]] = {}

    #global unique ids for each agent. Can be handy to manage memory and access levels per agent
    _agent_id = 1

    def __init__(
        self,
        name: str,
        llm: LLM,
        system_prompt: str,
        tools: ToolRegistry |  None = None,
    ):
        self.name = name
        self.llm = llm
        self.system_prompt = system_prompt
        self.tools = tools or ToolRegistry()
        self.memory = Memory()
        self.agent_id = Agent._agent_id
        Agent._agent_id +=1

    @abstractmethod
    def run(self, user_input: str) -> str:
        pass

    def add_message(self, role: Role, content: str) -> None:
        self.memory.add(role, content)

    def get_context(self) -> list[dict]:
        context = []

        ltm_content = self.ltm.read()
        if ltm_content:
            context.append({
                "role": "system",
                "content": f"Long-term memory:\n{ltm_content}"
            })

        context.extend(self.memory.to_dict_list())

        return context

    def clear_memory(self) -> None:
        self.memory.clear()

    def save_to_ltm(self, content: str) -> None:
        self.ltm.append(content)
