from google import genai
from google.genai import types
from agents.llm.base import LLM
from agents.llm.registery import register

@register("gemini")
class Gemini(LLM):

    def __init__(self, **kwargs):
        self.client = genai.Client()
        self.model = kwargs["model"]

    #can we can use builder design pattern here
    def call(self, systemprompt: str, content: str, **kwargs) -> str:
        response = self.client.models.generate_content(
            model=self.model, 
            config = types.GenerateContentConfig(
                    system_instruction=systemprompt
                    ),
            contents=content
        )
        
        return response

