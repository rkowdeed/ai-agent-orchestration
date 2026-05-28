import os
import tempfile

from app.services.persistence import SQLitePersistence


def test_sqlite_persistence_can_save_and_load_agent():
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    try:
        persistence = SQLitePersistence(db_path)
        persistence.save_agent('agent1', {'role': 'assistant'})
        config = persistence.load_agent('agent1')
        assert config == {'role': 'assistant'}
        assert persistence.list_agents() == ['agent1']
    finally:
        persistence.close()
        os.remove(db_path)


def test_sqlite_persistence_can_save_messages():
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    try:
        persistence = SQLitePersistence(db_path)
        persistence.save_message('chan1', 'hello', sender='user', role='user', agent_id='bot1')
        messages = persistence.list_messages()
        assert len(messages) == 1
        assert messages[0]['channel'] == 'chan1'
        assert messages[0]['text'] == 'hello'
        assert messages[0]['sender'] == 'user'
        assert messages[0]['role'] == 'user'
        assert messages[0]['agent_id'] == 'bot1'
        assert 'created_at' in messages[0]
    finally:
        persistence.close()
        os.remove(db_path)
