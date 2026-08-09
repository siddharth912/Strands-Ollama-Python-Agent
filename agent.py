from strands import Agent
from strands.models.ollama import OllamaModel
from strands_tools import http_request

# Create an Ollama model instance
ollama_model = OllamaModel(
    host="http://localhost:11434",  # Ollama server address
    model_id="llama3.2"              # Specify which model to use
)

system_prompt = (
    "you can use the tools you need and make api calls "
    "to free api that dosen't needs api key"
)

agent = Agent(
    model=ollama_model,
    tools=[http_request],
    system_prompt=system_prompt
)

user_input = input("Pucho: ")
agent(user_input)
