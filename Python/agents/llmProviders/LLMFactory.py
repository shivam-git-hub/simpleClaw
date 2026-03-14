class LLMFactory:

    registry = {}

    @staticmethod
    def useLLM(llmName_):
        llm = LLMFactory.registry[llmName_]
        return llm()    