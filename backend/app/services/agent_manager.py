import os
from typing import Dict, Any

from .persistence import SQLitePersistence


class Agent:
    def __init__(self, agent_id: str, config: Dict[str, Any] | None = None):
        self.agent_id = agent_id
        self.config = config or {}


class AgentManager:
    """Agent manager with SQLite persistence by default.

    This keeps the runtime integration separate from persistence and the UI.
    """

    def __init__(self, persistence: SQLitePersistence | None = None):
        self.persistence = persistence or SQLitePersistence(
            os.getenv("AIAGENT_DB_PATH")
        )

    def create_agent(self, agent_id: str, config: Dict[str, Any] | None = None) -> Agent:
        if self.persistence.load_agent(agent_id) is not None:
            raise ValueError("agent already exists")
        config = config or {}
        self.persistence.save_agent(agent_id, config)
        return Agent(agent_id, config)

    def get_agent(self, agent_id: str) -> Agent:
        config = self.persistence.load_agent(agent_id)
        if config is None:
            raise KeyError("agent not found")
        return Agent(agent_id, config)

    def list_agents(self) -> list[str]:
        return self.persistence.list_agents()

    def update_agent(self, agent_id: str, config: Dict[str, Any]) -> Agent:
        if self.persistence.load_agent(agent_id) is None:
            raise KeyError("agent not found")
        self.persistence.update_agent(agent_id, config)
        return Agent(agent_id, config)

    def delete_agent(self, agent_id: str) -> None:
        if self.persistence.load_agent(agent_id) is None:
            raise KeyError("agent not found")
        self.persistence.delete_agent(agent_id)
