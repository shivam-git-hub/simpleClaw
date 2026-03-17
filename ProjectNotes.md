### This File includes my personal notes, thought processes, doubts and what ifs etc, that I had while writing this project

1. First we create a common interface, which handles all the incoming request, and ouputs all the responses. 
2. To ensure channel wise features segregation, we will use channel-IDs to know which request come from which channel.

#### LLM folder:
1. Using Plugin Factory Design pattern to create objects of common LLM providers.
2. Each LLM Provider class like Gemini, Claude, OpenAI, Ollama implements LLM base class and has its own implementation of Tool Calling, Structured Output Parsing, LLM Calling, Exception Handling etc.


pyright, pytests, and ruff - how to use them