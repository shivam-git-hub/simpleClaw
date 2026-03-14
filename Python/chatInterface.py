import time
from agents import agent

def callAgent(query: str, channel_id: str) -> str:
	current_time = time.now()
	output = agent.invoke(query, channel_id, current_time)
	return output
	

