# Large Language Model Integration

## Overview

The SQL Intelligent Tutor integrates a locally hosted **Meta Llama 3 8B** model using **Ollama** to provide contextual educational assistance during SQL learning activities.

The backend communicates with Ollama through its local HTTP API, allowing the tutoring system to perform inference without relying on external cloud-based AI services.

This architecture demonstrates how open-source Large Language Models can be integrated into educational software while maintaining full control over the inference pipeline.

---

# Technology Stack

| Component | Technology |
|----------|------------|
| LLM | Meta Llama 3 8B |
| Inference Server | Ollama |
| Backend | FastAPI |
| Communication | HTTP REST API |

---

# Architecture

```text
Student
    │
    ▼
Frontend
    │
HTTP Request
    │
    ▼
FastAPI Backend
    │
Prompt Construction
    │
HTTP Request
    │
    ▼
Ollama Server
    │
Llama 3 8B
    │
Generated Response
    │
    ▼
FastAPI
    │
    ▼
Frontend
```

---

# Prompt Construction

The tutoring module does not forward the student's question directly to the model.

Instead, the backend dynamically constructs a structured prompt using contextual information such as:

- Student question
- Current SQL topic
- Lesson content
- Laboratory context
- Pedagogical instructions
- Expected tutoring behavior

Providing structured context enables the model to generate responses that are aligned with the student's current learning stage.

---

# Local Inference

The decision to execute the model locally using Ollama provides several advantages:

- No dependency on cloud AI providers
- Lower operational costs
- Reduced latency in local environments
- Full control over the inference pipeline
- Easier experimentation with different open-source models

---

# Current Limitations

The current implementation performs stateless inference.

Conversation history is not persisted between requests, and external knowledge retrieval (RAG) is not currently implemented.

---

# Future Improvements

- Retrieval-Augmented Generation (RAG)
- Conversation memory
- Adaptive prompting
- Multi-model support
- Automatic prompt optimization
- Student-specific tutoring profiles
