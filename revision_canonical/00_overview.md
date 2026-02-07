# LLM Engineering - Canonical Revision

Welcome to the distilled, high-density revision of the LLM Engineering course.
This repository consolidates 8 weeks of material into 5 executable modules and a shared reference library.

## Modules

| Module | Notebook | Description |
| :--- | :--- | :--- |
| **1. Foundations** | [`01_foundations_and_tools.ipynb`](./01_foundations_and_tools.ipynb) | core API usage, prompt engineering, structured outputs, function calling, and building a Gradio UI. |
| **2. RAG & Audio** | [`02_rag_and_evaluation.ipynb`](./02_rag_and_evaluation.ipynb) | Retrieval Augmented Generation (RAG) pipelines, Vector DBs (Chroma), Audio processing (Whisper), and evaluation metrics. |
| **3. Code Agents** | [`03_codegen_agents.ipynb`](./03_codegen_agents.ipynb) | Building autonomous agents that write and execute code, self-correction loops, and benchmarking. |
| **4. Fine-tuning** | [`04_finetuning_and_safety.ipynb`](./04_finetuning_and_safety.ipynb) | Fine-tuning LLMs (offline), Human-in-the-loop workflows, and implementing safety guardrails. |
| **5. Capstone** | [`05_capstone_deal_agent.ipynb`](./05_capstone_deal_agent.ipynb) | The "Deal Agent" - a multi-agent framework for autonomous negotiation and pricing. |

## Reference Code
Shared utilities are refactored into `reference_code/` for clean imports.
- `deal_agents.py`, `deal_models.py`: Capstone agent logic.
- `evaluation.py`: Visualization tools for model performance.
- `styles.py`, `scraper.py`, `visualizer.py`: Foundation utilities.

## Setup
1. Copy `.env.example` to `.env` and add your keys (OPENAI_API_KEY, etc.).
2. Run notebooks in order.

## 🧠 Learnings Recap & Strategy Map

The entire 8-week curriculum is distilled into these high-leverage patterns:

| Core Concept | Where it lives | Implementation Details |
| :--- | :--- | :--- |
| **Generative UI** | `Module 1` | Using Gradio/Streamlit to wrap LLM calls for rapid prototyping. |
| **Structured Data Extraction** | `Module 1` | Enforcing schema with Pydantic and JSON mode for reliable data processing. |
| **Vector Search (RAG)** | `Module 2` | Embedding documents, indexing in ChromaDB, and semantic retrieval. |
| **Multi-Modality** | `Module 2` | Processing Audio (Whisper) alongside Text for rich context. |
| **Code Generation** | `Module 3` | "Generator -> Executor -> Reflexion" loops for self-healing code agents. |
| **Model Customization** | `Module 4` | Fine-tuning (QLoRA) vs Prompt Engineering tradeoffs. |
| **AI Safety** | `Module 4` | "LLM-as-a-Judge" patterns for evaluating outputs against safety guidelines. |
| **Multi-Agent Orchestration** | `Module 5` | Coordinating specialized agents (Scanner, Pricer, Planner) to solve complex workflows. |
| **Production Patterns** | `Reference Code` | Shared libraries, modular imports, and clean evaluation harnesses.
