from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Union


class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class Message:
    role: Role
    content: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ToolCall:
    name: str
    arguments: dict


@dataclass
class ToolResult:
    tool_name: str
    output: str
    success: bool
    error: Union[str, None] = None
