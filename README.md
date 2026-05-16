# AgentForge

Turn plain-English descriptions of multi-agent AI systems into complete, production-ready codebases.

AgentForge uses IBM Bob (a CLI-based AI coding agent) to generate full-stack multi-agent systems — including backend APIs, vector search (RAG), agent orchestration, authentication, audit logging, and a chat frontend — from a single natural language prompt.

---

## Architecture

```
User (Browser) → Frontend (Next.js 16, :3000) → Backend (FastAPI, :8001) → IBM Bob CLI
```

### Backend (`backend/`)

- **FastAPI** server with 3 endpoints:
  - `POST /generate` — accepts `{description, auth, audit, frontend, llm}`, runs Bob, returns generated files as JSON
  - `POST /generate/download-files` — takes `{files}` dict, returns a ZIP download (skips re-generation)
  - `GET /` — health check
- **`prompt_builder.py`** — constructs a detailed engineering prompt instructing Bob to generate a multi-agent system with specific tech stack and file requirements
- **`bob_runner.py`** — shells out to `bob --yolo --chat-mode code`, collects generated files from disk
- **`file_parser.py`** — fallback parses `=== filename ===` markers from Bob's stdout
- **`zipper.py`** — creates in-memory ZIP archives

### Frontend (`frontend/`)

- **Next.js 16.2.6** + **React 19.2.4** + **TypeScript 5** + **Tailwind CSS 4** + **shadcn/ui** (Radix)
- Single-page UI with:
  - 3 quick-start template buttons (sales agent, customer support, research agent)
  - Textarea for custom descriptions
  - Toggle switches: JWT auth, audit logging, web chat UI, LLM provider (Gemini / Featherless)
  - Generate button → file browser with sidebar + code preview pane
  - ZIP download button
  - Dark theme with navy/blue gradient background

### What Bob Generates

| Component | Technology |
|-----------|-----------|
| Backend | FastAPI (Python) |
| Database | PostgreSQL |
| Vector store / RAG | ChromaDB (gemini-embedding-001) |
| Agent orchestration | CrewAI |
| LLM | Gemini / OpenAI / Featherless (configurable) |
| Auth | JWT (admin/visitor roles, optional) |
| Audit | PostgreSQL audit log (optional) |
| Frontend | Next.js web chat (optional) |
| Containerization | Docker Compose |

**13 required files**: `docker-compose.yml`, `backend/requirements.txt`, `backend/Dockerfile`, `backend/main.py`, `backend/database.py`, `backend/models.py`, `backend/orchestrator.py`, `backend/agents/{researcher,sales,guardrails}.py`, `backend/rag/{ingest,retriever}.py`, `backend/routers/chat.py`, `.env.example`, `README.md`

---

## Setup

### Prerequisites

- Node.js v22+ and npm
- Python 3.12+
- IBM Bob CLI (`npm install -g bobshell` or via fnm) with authentication configured

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8001
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# → http://localhost:3000
```

Open `http://localhost:3000` in your browser, describe your agent system, and click **Generate with IBM Bob**.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI, Uvicorn |
| Frontend | Next.js 16, React 19, TypeScript 5, Tailwind CSS 4, shadcn/ui |
| Generation engine | IBM Bob CLI v1 |
| Infrastructure | Docker Compose (generated projects) |
