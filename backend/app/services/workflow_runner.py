import asyncio
from typing import Dict, Any

from app.workflows.registry import get_workflow_template
from .agent_manager import AgentManager
from .messaging import InMemoryMessenger
from .runtime import RuntimeConnector


class WorkflowRunner:
    """Very small workflow runner to exercise critical paths in tests.

    Behavior: when executing a workflow, it looks up an agent and optionally
    invokes a runtime connector before sending a message.
    """

    def __init__(
        self,
        agents: AgentManager,
        messenger: InMemoryMessenger,
        runtime_connector: RuntimeConnector | None = None,
    ):
        self.agents = agents
        self.messenger = messenger
        self.runtime_connector = runtime_connector

    async def run_workflow(self, agent_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        agent = self.agents.get_agent(agent_id)
        channel = payload.get("channel", "default")
        text = payload.get("text", f"workflow run for {agent.agent_id}")
        self.messenger.send_message(
            channel,
            text,
            sender=agent.agent_id,
            role="user",
            agent_id=agent.agent_id,
        )

        runtime_result = None
        template = payload.get("template")
        if template:
            runtime_result = await get_workflow_template(template)(
                self.agents,
                self.messenger,
                self.runtime_connector,
                agent.agent_id,
                payload,
            )
        elif self.runtime_connector:
            runtime_result = await self.runtime_connector.execute(
                payload.get("runtime", "openai"),
                agent.agent_id,
                payload,
                agent_config=agent.config,
            )
            if runtime_result.get("status") == "ok":
                response_text = runtime_result.get("result", {}).get("text", "")
                if response_text:
                    self.messenger.send_message(
                        channel,
                        response_text,
                        sender=agent.agent_id,
                        role="assistant",
                        agent_id=agent.agent_id,
                    )

        result: Dict[str, Any] = {
            "status": "ok",
            "agent": agent.agent_id,
            "message": text,
        }
        if runtime_result is not None:
            result["runtime_result"] = runtime_result
        return result
