from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-3-pro-preview',
    name='root_agent',
    description="Greet agent",
    instruction="You are a helpful assistant",    
)