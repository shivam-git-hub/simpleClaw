import inspect
from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar, Union

from agents.types import ToolResult

T = TypeVar("T")


class Tool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def execute(self, **kwargs: Any) -> ToolResult:
        pass

    def to_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        }


class FunctionTool(Tool):
    def __init__(
        self,
        name: str,
        description: str,
        func: Callable[..., str],
    ):
        self._name = name
        self._description = description
        self._func = func

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    def execute(self, **kwargs: Any) -> ToolResult:
        try:
            result = self._func(**kwargs)
            return ToolResult(
                tool_name=self.name,
                output=str(result),
                success=True,
            )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                output="",
                success=False,
                error=str(e),
            )

    def to_schema(self) -> dict:
        sig = inspect.signature(self._func)
        properties = {}
        required = []

        for param_name, param in sig.parameters.items():
            if param_name in ("self", "cls"):
                continue

            param_type = "string"
            if param.annotation is not inspect.Parameter.empty:
                if param.annotation is int:
                    param_type = "integer"
                elif param.annotation is float:
                    param_type = "number"
                elif param.annotation is bool:
                    param_type = "boolean"

            properties[param_name] = {"type": param_type}

            if param.default is inspect.Parameter.empty:
                required.append(param_name)

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            },
        }


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def register_function(
        self,
        name: Union[str, None] = None,
        description: str = "",
    ) -> Callable[[Callable[..., str]], FunctionTool]:
        def decorator(func: Callable[..., str]) -> FunctionTool:
            tool_name = name or func.__name__
            tool_desc = description or func.__doc__ or ""
            tool = FunctionTool(tool_name, tool_desc, func)
            self.register(tool)
            return tool

        return decorator

    def get(self, name: str) -> Union[Tool, None]:
        return self._tools.get(name)

    def get_schemas(self) -> list[dict]:
        return [tool.to_schema() for tool in self._tools.values()]

    def execute(self, name: str, **kwargs: Any) -> ToolResult:
        tool = self.get(name)
        if tool is None:
            return ToolResult(
                tool_name=name,
                output="",
                success=False,
                error=f"Tool '{name}' not found",
            )
        return tool.execute(**kwargs)

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())
