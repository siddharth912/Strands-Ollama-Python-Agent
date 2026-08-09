# Strands Agents with Ollama – Local LLM Setup

This README documents the setup used to run a **Strands Agent locally with Ollama and the Llama 3.2 model**.

The agent was tested successfully and worked as expected, including making API calls through the configured HTTP request tool.

---

## 1. Prerequisites

The setup requires:

- Python 3.11
- Ollama
- Llama 3.2 model
- A Python virtual environment
- Strands Agents
- Strands Agents Tools

---

## 2. Install Python 3.11

Install Python 3.11 on the system.

Verify the installation:

```bash
python3.11 --version
```

Expected output:

```text
Python 3.11.x
```

---

## 3. Create a Python Virtual Environment

Create a virtual environment using Python 3.11:

```bash
python3.11 -m venv venv311
```

Activate the virtual environment:

```bash
source venv311/bin/activate
```

After activation, verify:

```bash
python --version
pip --version
```

---

## 4. Install Strands Packages

With the virtual environment activated, install the required packages:

```bash
pip install 'strands-agents[ollama]' strands-agents-tools
```

This installs:

- `strands-agents` – framework for creating and running agents
- `strands-agents[ollama]` – Ollama model integration
- `strands-agents-tools` – additional tools such as HTTP request functionality

---

## 5. Install and Configure Ollama

Verify that Ollama is installed:

```bash
ollama --version
```

Pull the Llama 3.2 model:

```bash
ollama pull llama3.2
```

Start the Ollama server:

```bash
ollama serve
```

By default, Ollama exposes its API at:

```text
http://localhost:11434
```

Keep the Ollama server running while using the agent.

---

## 6. Create `agent.py`

Create a file named:

```text
agent.py
```

Use the following code:

```python
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
```

---

## 7. How the Code Works

### Ollama Model

```python
ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2"
)
```

This configures Strands to use the locally running Ollama server and the `llama3.2` model.

### HTTP Request Tool

```python
from strands_tools import http_request
```

The HTTP request tool allows the agent to make HTTP/API requests when required.

The system prompt tells the agent that it can use tools and call free APIs that do not require an API key.

### Agent

```python
agent = Agent(
    model=ollama_model,
    tools=[http_request],
    system_prompt=system_prompt
)
```

This creates the Strands Agent and provides:

- The Ollama LLM
- The HTTP request tool
- The system instructions

---

## 8. Run the Agent

Make sure the virtual environment is active:

```bash
source venv311/bin/activate
```

Make sure Ollama is running in another terminal:

```bash
ollama serve
```

Then run:

```bash
python agent.py
```

You should see:

```text
Pucho:
```

Enter a question or request.

Example:

```text
Pucho: What is the current weather in Delhi?
```

The agent can decide when it needs to use the configured HTTP request tool to retrieve information from an API.

---

## 9. Architecture

The setup works approximately like this:

```text
                   User
                    |
                    v
                agent.py
                    |
                    v
            Strands Agent
              /         \
             /           \
            v             v
      Ollama Model     HTTP Tool
            |             |
            v             v
        Llama 3.2      Free APIs
            |
            v
     Ollama Server
     localhost:11434
```

---

## 10. Important Note About Bedrock

The initial Strands Agent examples commonly use Amazon Bedrock as the model provider.

In this setup, however, the agent is explicitly configured with:

```python
model=ollama_model
```

Therefore, this implementation uses the **local Ollama server and Llama 3.2 model** rather than relying on Amazon Bedrock for the model inference.

---

## 11. Useful Commands

### Activate virtual environment

```bash
source venv311/bin/activate
```

### Deactivate virtual environment

```bash
deactivate
```

### Check Python version

```bash
python --version
```

### Check installed Strands packages

```bash
pip list | grep strands
```

### Check Ollama models

```bash
ollama list
```

### Pull/update Llama 3.2

```bash
ollama pull llama3.2
```

### Start Ollama

```bash
ollama serve
```

### Run the agent

```bash
python agent.py
```

---

## 12. Troubleshooting

### `python: command not found`

Make sure the virtual environment is activated:

```bash
source venv311/bin/activate
```

Or use:

```bash
python3.11 -m venv venv311
source venv311/bin/activate
```

### Ollama connection error

Make sure Ollama is running:

```bash
ollama serve
```

Check that the server is listening on:

```text
http://localhost:11434
```

### Model not found

Check installed models:

```bash
ollama list
```

If `llama3.2` is missing:

```bash
ollama pull llama3.2
```

### Strands package not found

Make sure the virtual environment is active:

```bash
source venv311/bin/activate
```

Then reinstall:

```bash
pip install 'strands-agents[ollama]' strands-agents-tools
```

---

## 13. Current Status

The setup was successfully completed and tested.

### Status

- [x] Python 3.11 installed
- [x] Python 3.11 virtual environment created
- [x] Virtual environment activated
- [x] `strands-agents[ollama]` installed
- [x] `strands-agents-tools` installed
- [x] Ollama installed/configured
- [x] Llama 3.2 downloaded
- [x] Ollama server started
- [x] Strands Agent configured
- [x] HTTP request tool configured
- [x] Agent tested successfully

The local Strands Agent worked successfully as expected.
