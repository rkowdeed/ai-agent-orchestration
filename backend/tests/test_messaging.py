from app.services.messaging import InMemoryMessenger


def test_send_and_get_messages():
    m = InMemoryMessenger()
    assert m.get_messages() == []
    m.send_message("chan1", "hello", sender="user", role="user", agent_id="bot1")
    msgs = m.get_messages()
    assert len(msgs) == 1
    assert msgs[0]["channel"] == "chan1"
    assert msgs[0]["text"] == "hello"
    assert msgs[0]["sender"] == "user"
    assert msgs[0]["role"] == "user"
    assert msgs[0]["agent_id"] == "bot1"


def test_message_filters():
    m = InMemoryMessenger()
    m.send_message("chan1", "hello", sender="user", role="user", agent_id="bot1")
    m.send_message("chan2", "world", sender="bot2", role="assistant", agent_id="bot2")
    assert len(m.get_messages(agent_id="bot1")) == 1
    assert len(m.get_messages(channel="chan2")) == 1
