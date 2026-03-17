from llm.base import LLM
from llm.loader import load_llm_plugins

load_llm_plugins()

class LLMFactory:

    @staticmethod
    def create(llmName_, **kwargs):
        llm = LLM.registry[llmName_]
        return llm(**kwargs)    