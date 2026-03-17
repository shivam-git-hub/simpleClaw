from pathlib import Path

from agents.types import Message, Role


class ConversationHistory:
    def __init__(self, max_messages: int = 50):
        self.messages: list[Message] = []
        self.max_messages = max_messages

    def add(self, role: Role, content: str) -> None:
        self.messages.append(Message(role=role, content=content))
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)

    def get_messages(self) -> list[Message]:
        return self.messages

    def clear(self) -> None:
        self.messages.clear()

    def to_dict_list(self) -> list[dict]:
        return [{"role": m.role.value, "content": m.content} for m in self.messages]


class LongTermMemory:
    def __init__(self, memory_file: str = "history.md"):
        self.memory_file = Path(memory_file)
        if not self.memory_file.exists():
            self.memory_file.touch()

    def read(self) -> str:
        return self.memory_file.read_text()

    def write(self, content: str) -> None:
        self.memory_file.write_text(content)

    def append(self, content: str) -> None:
        existing = self.read()
        new_content = f"{existing}\n{content}" if existing else content
        self.write(new_content)

    def search(self, query: str) -> list[str]:
        content = self.read().lower()
        query_lower = query.lower()
        lines = content.split("\n")
        return [line for line in lines if query_lower in line]

    def clear(self) -> None:
        self.write("")
