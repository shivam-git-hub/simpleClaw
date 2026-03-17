# AGENTS.md - Agentic Coding Guidelines

This document provides guidelines for agents operating in the simpleClaw repository.

## What is simpleClaw?

simpleClaw is a simple LLM orchestrator built around the idea of clawdBot. The goal is to keep it easy to understand while maintaining industry-standard functionality. The repository serves as both a tool to interact with an LLM agent and a tutorial.

**Current Aim for features:**
- Multi-channel support (Telegram, CLI)
- LLM with tools (Claude-style skills) and memory
- Heartbeat mechanism (auto-invokes LLM after a period)
- Triggers: webhooks, cron jobs (fixed intervals, persistent or temporary)
- Sub-agent spawning, coding, online research, document management

---

## Code Style Guidelines

### Imports

- **Always use absolute imports** (not relative):
  ```python
  from llm.base import LLM          # Correct
  from .base import LLM             # Avoid
  ```

- **Organize imports** in this order (separate with blank lines):
  1. Standard library (`abc`, `os`, `json`)
  2. Third-party packages (`google.genai`, `pydantic`, `dotenv`)
  3. Local application modules (`llm`, `config`)

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `LLMFactory`, `Gemini`, `AppConfig` |
| Functions / Variables | snake_case | `load_llm_plugins`, `create_llm` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRIES`, `DEFAULT_TIMEOUT` |
| Private methods | prefix with `_` | `_load_config()` |

### Type Hints

- **Required** for all function parameters and return types:
  ```python
  def call(self, systemprompt: str, content: str, **kwargs) -> str:
  ```

### Code Structure

- Follow **SOLID Principles**
- **Max function length**: ~50 lines
- **Max class length**: ~200 lines
- **One class per file** (unless tightly coupled)
- **Files named after class**: `factory.py` contains `LLMFactory`
- Comment design patterns and conscious choices to keep code readable and build the tutorial

### Error Handling

- Use **specific exceptions** with clear messages:
  ```python
  if not config_path.exists():
      raise FileNotFoundError(f"Config not found: {config_path}")
  ```

- Prefer **early returns** over deep nesting

### Docstrings & Comments

- Use **type hints** instead of documenting parameter types
- If needed, use Google style docstrings
- Avoid unnecessary comments

### Patterns Used

1. **Decorator Pattern** for plugin registration:
   ```python
   @register("gemini")
   class Gemini(LLM):
       ...
   ```

2. **Singleton Pattern** for configuration:
   ```python
   class Config:
       _instance = None
       
       def __new__(cls):
           if cls._instance is None:
               cls._instance = super().__new__(cls)
           return cls._instance
   ```

3. **Factory Pattern** for object creation:
   ```python
   llm = LLMFactory.create("gemini", model="gemini-2.0")
   ```

4. **Lazy Loading** with `lru_cache`:
   ```python
   @lru_cache()
   def get_config() -> Config:
       return Config()
   ```

---

## Project Structure

```
simpleClaw/
├── main.py              # Entry point
├── chatInterface.py     # Chat interface (WIP)
├── llm/
│   ├── __init__.py
│   ├── base.py          # Abstract LLM class
│   ├── factory.py       # LLMFactory (plugin loader)
│   ├── registery.py     # @register decorator
│   ├── loader.py        # Dynamic plugin loader
│   └── gemini.py        # Gemini implementation
├── config/
│   ├── settings.py      # Config singleton with Pydantic
│   └── config.json      # Configuration file
└── requirements.txt     # Dependencies
```

---

## What NOT To Do

- ❌ Use `print()` for debugging (use logging)
- ❌ Commit secrets or API keys to version control
- ❌ Use bare `except:` clauses
- ❌ Create circular imports
- ❌ Modify `requirements.txt` without testing
- ❌ Skip type hints for "simplicity"

---

## Important Notes

- Feel free to correct me or suggest better alternatives—I am also learning Python.
- We are collaborators. If you conclude that some decisions were wrong or can be improved, suggest changes.
- For interesting design choices, areas to explore, or notes, add them to `AgentNotes.md`.
- Dont do pip install or any other install yourself, ask me and i will do it. 

We are using python 3.12
