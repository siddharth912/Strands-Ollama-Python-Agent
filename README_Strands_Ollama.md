# Strands Ollama Python Agent — Local AI DevOps Assistant

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Ollama](https://img.shields.io/badge/LLM-Ollama%20(Local)-black?logo=ollama)
![Anthropic](https://img.shields.io/badge/SDK-Anthropic%20Strands-purple)
![License](https://img.shields.io/badge/License-MIT-green)
![Offline](https://img.shields.io/badge/Mode-Offline%20%7C%20Air--Gapped-red)

> **A conversational AI agent that runs entirely on your local machine — query your Kubernetes clusters, AWS infrastructure, and Linux systems in plain English, with no data leaving your environment.**

---

## The Problem

DevOps engineers working in secure, air-gapped, or VPN-restricted environments (jump hosts, bastion servers, internal networks) cannot use cloud-based AI tools like ChatGPT or Claude directly — sensitive infrastructure details shouldn't leave the network boundary. Yet the cognitive load of remembering every `kubectl`, `aws cli`, and `bash` command is real.

## The Solution

This project is a **fully local, conversational AI agent** built with:
- **Anthropic Strands SDK** — for agentic tool-use and multi-turn conversation
- **Ollama** — to run a capable LLM (e.g., Llama 3, Mistral, Gemma) entirely on local hardware
- **Python shell tools** — so the agent can actually execute commands and reason about the output

The result: ask infrastructure questions in plain English on your jump host, get intelligent answers with real command execution — entirely offline.

---

## Demo

```
You: which pods in the prod namespace are not running?

Agent: Let me check that for you.
[Executing: kubectl get pods -n prod --field-selector=status.phase!=Running]

NAME                          READY   STATUS             RESTARTS   AGE
payments-api-7d9f6b-xkp2q    0/1     CrashLoopBackOff   14         2h
notification-svc-5c8d-9mnt    0/1     Pending            0          45m

I found 2 pods with issues:
1. payments-api is in CrashLoopBackOff (14 restarts in 2h) — likely an application error or misconfigured env var. Run: kubectl logs payments-api-7d9f6b-xkp2q -n prod --previous
2. notification-svc is Pending — probably a scheduling issue. Check: kubectl describe pod notification-svc-5c8d-9mnt -n prod for node/resource constraints.

Want me to pull the logs or describe either pod?
```

---

## Architecture

```
User (plain English)
        │
        ▼
  Strands Agent (Python)
        │
        ├──► Ollama (local LLM)  ──► Reasoning & response generation
        │         (Llama3 / Mistral / Gemma — runs on your machine)
        │
        └──► Shell Tool  ──► Execute kubectl / aws / bash commands
                    │
                    └──► Real cluster / infrastructure output
```

**No data leaves your machine. No API keys needed for the LLM.**

---

## Features

- **Conversational** — multi-turn dialogue, remembers context within a session
- **Executable** — actually runs shell commands and interprets output
- **Offline-capable** — LLM runs locally via Ollama, no internet needed
- **Kubernetes-aware** — `kubectl` queries, pod debugging, namespace inspection
- **AWS-aware** — works alongside AWS CLI for EC2, EKS, S3 queries
- **Extensible** — add custom tools (Prometheus queries, Helm, Terraform) easily

---

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally
- A local model pulled (e.g., `ollama pull llama3`)
- `kubectl` configured (for Kubernetes queries)
- `aws` CLI configured (for AWS queries, optional)

---

## Installation

```bash
# Clone the repo
git clone https://github.com/siddharth912/Strands-Ollama-Python-Agent.git
cd Strands-Ollama-Python-Agent

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Pull a local model via Ollama

```bash
# Recommended: Llama 3 (8B — good balance of speed and quality)
ollama pull llama3

# Lighter option for low-RAM machines
ollama pull mistral

# Verify Ollama is running
ollama list
```

---

## Usage

```bash
# Start the agent
python agent.py

# You'll see:
# DevOps AI Agent ready. Ask me anything about your infrastructure.
# Type 'exit' to quit.
#
# You:
```

### Example queries you can ask

```
# Kubernetes
"show me all pods across all namespaces"
"which deployments have less than 2 replicas running?"
"what's the resource usage of nodes in the cluster?"
"describe the failing pod in the payments namespace"
"get the last 50 lines of logs from the api-gateway pod"

# AWS
"list all EC2 instances that are stopped"
"what Auto Scaling Groups do I have and their current capacity?"
"show me S3 buckets and their sizes"

# System
"how much disk space is free on this server?"
"show me the top 10 processes by CPU usage"
"check if port 443 is open on 10.0.1.50"
```

---

## Configuration

Edit `config.py` to customize:

```python
# Model to use (must be pulled via ollama pull <model>)
OLLAMA_MODEL = "llama3"

# Ollama API endpoint (default: local)
OLLAMA_BASE_URL = "http://localhost:11434"

# Max tokens per response
MAX_TOKENS = 2048

# Default shell timeout (seconds)
SHELL_TIMEOUT = 30
```

---

## Adding Custom Tools

The Strands SDK makes it easy to add new tools. Example — add a Prometheus query tool:

```python
from strands import tool

@tool
def query_prometheus(query: str) -> str:
    """Query Prometheus metrics using PromQL."""
    import requests
    response = requests.get(
        "http://prometheus:9090/api/v1/query",
        params={"query": query}
    )
    return response.json()
```

Register it in `agent.py` and the agent will automatically use it when relevant.

---

## Why This Matters for Secure Environments

| Concern | This Solution |
|---|---|
| Data privacy | LLM runs locally — no data sent externally |
| Air-gapped networks | Works with zero internet connectivity |
| Jump host / bastion | Runs on any Linux machine with Python + Ollama |
| Audit compliance | All commands visible and logged locally |
| Cost | Free — no API costs for the LLM |

---

## Real-World Context

Built to solve a real pain point: managing EKS clusters and AWS infrastructure from a **jump host in a PCI-DSS compliant environment** where cloud AI tools are not permitted. The agent runs entirely within the network boundary, making it safe for production DevOps workflows in fintech, banking, and healthcare environments.

---

## Roadmap

- [ ] Persistent session memory across restarts
- [ ] Helm chart query support
- [ ] Terraform plan/apply integration
- [ ] Prometheus/Grafana natural language queries
- [ ] Slack bot interface for team-wide access
- [ ] Multi-cluster kubectl context switching

---

## Tech Stack

| Component | Technology |
|---|---|
| Agent framework | [Anthropic Strands SDK](https://github.com/strands-agents/sdk-python) |
| Local LLM runtime | [Ollama](https://ollama.com) |
| Language | Python 3.10+ |
| Shell execution | subprocess / Strands shell tool |
| Target platforms | Linux (RHEL, Ubuntu, Amazon Linux) |

---

## Author

**Siddharth Mishra** — Senior DevOps Engineer  
[LinkedIn](https://linkedin.com/in/siddharth-mishra-0b9311189) · [GitHub](https://github.com/siddharth912)

---

## License

MIT — free to use, modify, and distribute.
