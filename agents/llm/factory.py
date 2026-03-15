from agents.llm.base import LLM

class LLMFactory:

    @staticmethod
    def create(llmName_, **kwargs):
        llm = LLM.registry[llmName_]
        return llm(**kwargs)    