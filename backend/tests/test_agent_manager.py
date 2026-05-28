import os
import tempfile
from app.services.agent_manager import AgentManager


def test_create_and_get_agent():
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    try:
        os.environ['AIAGENT_DB_PATH'] = db_path
        m = AgentManager()
        a = m.create_agent("bot1", {"role": "assistant"})
        assert a.agent_id == "bot1"
        fetched = m.get_agent("bot1")
        assert fetched.agent_id == "bot1"
        assert fetched.config == {"role": "assistant"}
    finally:
        m.persistence.close()
        del os.environ['AIAGENT_DB_PATH']
        os.remove(db_path)


def test_create_duplicate_raises():
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    try:
        os.environ['AIAGENT_DB_PATH'] = db_path
        m = AgentManager()
        m.create_agent("bot1")
        try:
            m.create_agent("bot1")
            assert False, "expected ValueError"
        except ValueError:
            pass
    finally:
        m.persistence.close()
        del os.environ['AIAGENT_DB_PATH']
        os.remove(db_path)
