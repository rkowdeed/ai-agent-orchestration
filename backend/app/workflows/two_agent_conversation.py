import asyncio
from typing import Any, Dict

async def two_agent_conversation_workflow(
    agent_manager: Any,
    messenger: Any,
    runtime_connector: Any,
    agent_id: str,
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    agents = agent_manager.list_agents()
    target_id = payload.get("target_agent_id")
    if not target_id or target_id == agent_id:
        target_id = next((aid for aid in agents if aid != agent_id), None)
    if target_id is None:
        raise KeyError("no second agent available for two-agent conversation")

    initial_text = payload.get("text", f"Start conversation from {agent_id}")
    messenger.send_message(
        payload.get("channel", "default"),
        initial_text,
        sender=agent_id,
        role="user",
        agent_id=agent_id,
    )

    agent_config = agent_manager.get_agent(target_id).config
    task = asyncio.create_task(
        runtime_connector.execute(
            "openai",
            target_id,
            {"prompt": f"Reply to: {initial_text}", "runtime": "openai"},
            agent_config=agent_config,
        )
    )

    runtime_result = await task
    result_text = runtime_result.get("result", {}).get("text", "")
    messenger.send_message(
        payload.get("channel", "default"),
        result_text,
        sender=target_id,
        role="assistant",
        agent_id=target_id,
    )

    return {
        "status": "ok",
        "agent": agent_id,
        "message": f"{agent_id} and {target_id} exchanged messages",
        "runtime_result": runtime_result,
    }
