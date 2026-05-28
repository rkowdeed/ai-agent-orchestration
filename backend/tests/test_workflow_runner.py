import asyncio
import os
import tempfile

from app.services.agent_manager import AgentManager
from app.services.messaging import InMemoryMessenger
from app.services.workflow_runner import WorkflowRunner


def test_workflow_runs_and_sends_message():
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    try:
        os.environ['AIAGENT_DB_PATH'] = db_path
        agents = AgentManager()
        agents.create_agent("bot1")
        messenger = InMemoryMessenger(agents.persistence)
        runner = WorkflowRunner(agents, messenger)
        res = asyncio.run(runner.run_workflow("bot1", {"channel": "chanX", "text": "run"}))
        assert res["status"] == "ok"
        assert messenger.get_messages()[0]["text"] == "run"
    finally:
        agents.persistence.close()
        del os.environ['AIAGENT_DB_PATH']
        os.remove(db_path)
