# AI Agent Orchestration — MVP

Monorepo scaffold for an AI agent platform MVP.

Folders:
- `backend/` — FastAPI service
- `frontend/` — React + TypeScript app (Vite)
- `connectors/` — example connector implementations (OpenAI, Slack)
- `infra/` — Docker Compose and infra helpers
- `docs/` — architecture and onboarding docs

Quick start (development):

Backend

- Create a Python virtualenv and install requirements in `backend/`.

Frontend

- `cd frontend` then `npm install` and `npm run dev` (Vite)

See `docs/getting_started.md` for more details.

## Agent Runtime Integration

This repository includes an optional scaffold for integrating an agent
orchestration runtime. The initial integration choice is **AutoGen** — a
lightweight, agent-focused orchestration framework.

- **Why AutoGen:** AutoGen is well-suited for coordinating multiple
	agents and tools, offers flexible runtime modes (local or remote), and
	interoperates easily with existing LLM connectors such as the
	OpenAI client in `connectors/openai`.
- **Opt-in usage:** The AutoGen scaffold lives in `connectors/autogen` and
	is optional. Install AutoGen with `pip install autogen` to enable
	orchestration features and follow the README in that folder.

See `connectors/autogen/README.md` for installation instructions and a
small example snippet.
