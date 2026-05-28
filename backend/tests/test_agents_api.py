import os
import tempfile
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_agent_and_run_workflow():
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    try:
        os.environ['AIAGENT_DB_PATH'] = db_path
        resp = client.post('/api/v1/agents', json={'agent_id': 'api-bot', 'config': {'role': 'assistant'}})
        assert resp.status_code == 200
        assert resp.json()['agent_id'] == 'api-bot'

        run_resp = client.post('/api/v1/agents/api-bot/run', json={'channel': 'web', 'text': 'execute'})
        assert run_resp.status_code == 200
        data = run_resp.json()
        assert data['status'] == 'ok'
        assert data['agent'] == 'api-bot'
        assert data['message'] == 'execute'

        history_resp = client.get('/api/v1/messages')
        assert history_resp.status_code == 200
        assert any(msg['agent_id'] == 'api-bot' for msg in history_resp.json())

        delete_resp = client.delete('/api/v1/agents/api-bot')
        assert delete_resp.status_code == 200
        assert delete_resp.json()['status'] == 'deleted'

        get_resp = client.get('/api/v1/agents/api-bot')
        assert get_resp.status_code == 404
    finally:
        del os.environ['AIAGENT_DB_PATH']
        try:
            os.remove(db_path)
        except PermissionError:
            pass
