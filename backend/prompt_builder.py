def build_prompt(
    description: str,
    auth: bool = True,
    audit: bool = True,
    frontend: str = "webchat",
    llm: str = "gemini"
) -> str:
    auth_req = "Include JWT authentication with admin and visitor roles." if auth else "No authentication needed."
    audit_req = "Include a full audit log of every agent decision stored in PostgreSQL." if audit else "No audit logging needed."
    frontend_req = "Include a Next.js web chat interface." if frontend == "webchat" else "API only, no frontend."
    llm_req = {
        "gemini": "Use Google Gemini API (google-genai package, model: gemini-2.5-flash-lite) as the LLM.",
        "openai": "Use OpenAI API as the LLM.",
        "featherless": "Use Featherless AI API (OpenAI-compatible) with model google/gemma-3-12b-it."
    }.get(llm, "Use Google Gemini API as the LLM.")

    return f"""You are a senior software engineer specializing in AI agent systems.
Generate a complete, production-ready multi-agent AI system based on this description:

{description}

Technical requirements:
- {auth_req}
- {audit_req}
- {frontend_req}
- {llm_req}
- Use FastAPI for the backend
- Use ChromaDB for vector storage and RAG
- Use CrewAI for agent orchestration
- Use PostgreSQL for persistent storage
- Use Docker Compose for containerization
- Use Gemini embedding API for embeddings (model: gemini-embedding-001)

Generate ALL of these files, clearly separated by filename headers exactly like this:
=== filename ===
[file content]

Required files:
- docker-compose.yml
- backend/requirements.txt
- backend/Dockerfile
- backend/main.py
- backend/database.py
- backend/models.py
- backend/orchestrator.py
- backend/agents/researcher.py
- backend/agents/sales.py
- backend/agents/guardrails.py
- backend/rag/ingest.py
- backend/rag/retriever.py
- backend/routers/chat.py
- .env.example
- README.md

Every file must be complete, functional, and ready to run.
Do not use placeholder comments like "# add your code here".
The system should work with docker-compose up after filling in the .env file."""