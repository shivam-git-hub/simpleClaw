from abc import ABC, abstractmethod

class LLM(ABC):

    registry = {}

    @abstractmethod
    def call(self):
        pass
