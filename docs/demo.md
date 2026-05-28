# Demo: Run the AI Agent Orchestration End-to-End

This guide shows how to run the backend, frontend, and sample workflows using
real agent execution and persisted message history.

## Requirements

- Python 3.10+
- Node 18+ / npm
- OpenAI API key
- Optional: Slack bot token for Slack workflow delivery

## 1. Start the backend

From the repository root:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
set OPENAI_API_KEY=<your-key>
set SLACK_BOT_TOKEN=<your-slack-token>
python -m uvicorn app.main:app --app-dir backend --reload --port 8000
```

If you run this command from inside the `backend/` folder instead, omit `--app-dir backend`:

```bash
python -m uvicorn app.main:app --reload --port 8000
```

- `OPENAI_API_KEY` enables actual LLM execution.
- `SLACK_BOT_TOKEN` enables Slack delivery for the `slack-broadcast` template.

## 2. Start the frontend

In a second terminal:

```bash
cd frontend
npm install --legacy-peer-deps
npm run dev
```

Open the Vite frontend URL shown in the terminal.

## 3. Create an agent in the UI

In the frontend, use the `Create an Agent` panel:

- Agent ID: `bot1`
- Agent name: `AssistantBot`
- Channel: `default`

This creates a persisted agent config stored in SQLite.

## 4. Run a real agent workflow

Use the `Run openai workflow` button with a prompt such as:

> Explain the next step in this scenario.

Expected behavior:

- The backend sends the prompt to OpenAI.
- The generated response is persisted in message history.
- The UI updates the history panel with the agent response.

## 5. Run a built-in workflow template

### Two-agent conversation

This workflow demonstrates asynchronous agent-to-agent handoff.

- Create two agents, e.g. `bot1` and `bot2`.
- Select one of them in the UI.
- Click `Run two-agent conversation template`.

Expected behavior:

- The selected agent sends an initial message.
- The second agent receives the handoff and replies through the OpenAI runtime.
- Both messages are persisted and visible in history.

### Slack broadcast

This workflow generates a Slack post and sends it through Slack if
`SLACK_BOT_TOKEN` is configured.

- Create an agent with channel `slack:#general`.
- Click `Run Slack broadcast template`.

Expected behavior:

- The workflow uses the OpenAI runtime to compose the broadcast.
- The frontend persists the message history.
- Slack receives a message in the configured channel.

## 6. Inspect message history

The UI shows persisted history for all messages, including:

- user prompts
- assistant responses
- Slack broadcast messages
- agent handoff replies

You can also query the backend directly:

```bash
curl http://127.0.0.1:8000/api/v1/messages
```

Or filter by agent:

```bash
curl http://127.0.0.1:8000/api/v1/agents/bot1/messages
```

## API Examples

Create an agent:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/agents \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"bot1","config":{"name":"AssistantBot","role":"assistant","system_prompt":"You are a helpful assistant.","model":"gpt-4o-mini","channels":["default"]}}'
```

Run an OpenAI workflow for an existing agent:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/agents/bot1/run \
  -H "Content-Type: application/json" \
  -d '{"channel":"default","text":"What should I do next?","runtime":"openai"}'
```

Update an existing agent's configuration:

```bash
curl -X PUT http://127.0.0.1:8000/api/v1/agents/bot1 \
  -H "Content-Type: application/json" \
  -d '{"config":{"name":"AssistantBot","role":"assistant","system_prompt":"You are an even more helpful assistant.","model":"gpt-4o-mini","channels":["default","slack:#general"]}}'
```

Run a built-in template:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/agents/bot1/run \
  -H "Content-Type: application/json" \
  -d '{"template":"two-agent-conversation","channel":"default","text":"Start a conversation."}'
```

## 7. Troubleshooting

- If the frontend fails to load, ensure `npm install --legacy-peer-deps` succeeded.
- If OpenAI calls fail, verify `OPENAI_API_KEY` is present and valid.
- If Slack delivery fails, verify `SLACK_BOT_TOKEN` and the `slack:#channel` format.

## Notes

- Message history is persisted in `backend/aiagent.db` by default.
- Workflows are executed by the runtime connector, not a UI mockup.
- The demo demonstrates real agent execution with persisted history and optional
  Slack integration.
