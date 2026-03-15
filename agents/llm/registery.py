from agents.llm.factory import LLM

def register(name):

    def decorator(cls):
        LLM.registry[name] = cls
        return cls
    return decorator

        