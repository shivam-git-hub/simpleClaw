import logging
from typing import Any

from agents.base import Agent
from agents.types import Role, ToolCall, ToolResult

logger = logging.getLogger(__name__)


class AgentRunner:
    def __init__(self, agent: Agent):
        self.agent = agent

    def execute(
        self,
        user_input: str,
        max_iterations: int = 10,
    ) -> str:
        self.agent.add_message(Role.USER, user_input)

        for iteration in range(max_iterations):
            response = self._call_llm()

            if response.tool_calls:
                for tool_call in response.tool_calls:
                    result = self._execute_tool(tool_call)
                    self.agent.add_message(
                        Role.ASSISTANT,
                        f"Tool call: {tool_call.name}({tool_call.arguments})\n"
                        f"Result: {result.output}",
                    )

                    if not result.success:
                        self.agent.add_message(
                            Role.SYSTEM,
                            f"Error: {result.error}",
                        )
            else:
                content = self._extract_content(response)
                self.agent.add_message(Role.ASSISTANT, content)
                return content

        return "Max iterations reached without completing task."

    def _call_llm(self) -> Any:
        context = self.agent.get_context()
        tools = None

        if self.agent.tools.list_tools():
            tools = self.agent.tools.get_schemas()

        return self.agent.llm.call(
            systemprompt=self.agent.system_prompt,
            content=context,
            tools=tools,
        )

    def _execute_tool(self, tool_call: ToolCall) -> ToolResult:
        logger.info(f"Executing tool: {tool_call.name}")
        return self.agent.tools.execute(
            tool_call.name,
            **tool_call.arguments,
        )

    def _extract_content(self, response: Any) -> str:
        if hasattr(response, "text"):
            return response.text
        if hasattr(response, "candidates"):
            candidate = response.candidates[0]
            if hasattr(candidate, "content") and hasattr(candidate.content, "parts"):
                parts = candidate.content.parts
                if parts and hasattr(parts[0], "text"):
                    return parts[0].text
        return str(response)
