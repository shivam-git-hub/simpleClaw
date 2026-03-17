import os
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()

    from llm.factory import LLMFactory

    llm = LLMFactory.create("gemini", model = "gemini-2.5-flash")


    systemprompt = "You are a friendly assistant"
    query = "what is 2+2"

    response = llm.call(systemprompt = systemprompt, content = query)

    print(response.text)
