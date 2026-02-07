# LLM Engineering: Best Practices & Production Thinking

This document summarizes the key architectural patterns and production considerations from the 8-week course.

## 1. Prompt Engineering & Structured Outputs
- **Be Specific:** LLMs need clear instructions. Use "System Prompts" to define persona and constraints.
- **Structured Outputs (JSON/Pydantic):** Always use structured outputs (e.g., `response_format={"type": "json_object"}` or `client.beta.chat.completions.parse`) for programmatically consuming LLM responses. This is critical for reliable agents.
- **Chain of Thought:** For complex tasks, ask the model to "explain its reasoning" before giving the answer.

## 2. Retrieval Augmented Generation (RAG)
- **Chunking Matters:** 
    - Naive chunking (fixed size) breaks context.
    - Semantic chunking (grouping by meaning) is better but slower.
    - Recursive chunking is a good middle ground.
- **Hybrid Search:** Combine Vector Search (Semantic) with Keyword Search (BM25) for best results.
- **Re-ranking:** Use a Cross-Encoder (e.g., Cohere Rerank) to re-order retrieved results before sending to the LLM.

## 3. Agents & Tool Use
- **ReAct Pattern:** The standard loop: `Reason` -> `Act` (Call Tool) -> `Observe` (Result) -> `Repeat`.
- **Planning:** For complex goals, use a "Planner Agent" to break down the task into steps first.
- **Error Handling (Reflexion):** Agents should read their own error messages and attempt to fix their code/actions.

## 4. Evaluation & Ops
- **LLM-as-a-Judge:** Use a strong model (GPT-4) to grade the outputs of a faster model (GPT-4o-mini).
- **Hard Metrics:** Track latency, cost per token, and pass@k (for code).
- **Safety:** Always implement input/output guardrails. Never run generated code in a production environment without sandboxing (e.g., Docker, E2B, Modal).

## 5. Deployment (Modal/Cloud)
- **Serverless:** LLMs are bursty. Serverless (Modal, AWS Lambda) is often cheaper than always-on GPUs for erratic workloads.
- **Secrets Management:** Never commit `.env` files. Use cloud secret managers.

## 6. Where to go from here?
- **LangChain / LlamaIndex:** Good for rapid prototyping, but "building from scratch" (as done in this course) gives you more control and understanding.
- **DSPy:** The future of "compiling" prompts instead of hand-writing them.
