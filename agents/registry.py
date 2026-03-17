def register(name: str):
    from agents.base import Agent

    def decorator(cls: type[Agent]) -> type[Agent]:
        Agent.registry[name] = cls
        return cls

    return decorator
