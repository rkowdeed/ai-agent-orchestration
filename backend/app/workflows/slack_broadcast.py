from typing import Any, Dict

async def slack_broadcast_workflow(
    agent_manager: Any,
    messenger: Any,
    runtime_connector: Any,
    agent_id: str,
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    channel = payload.get("channel", "slack:#general")
    prompt = payload.get("prompt") or payload.get("text") or "Compose a short announcement for Slack."

    agent_config = agent_manager.get_agent(agent_id).config
    runtime_result = await runtime_connector.execute(
        "openai",
        agent_id,
        {"prompt": prompt, "runtime": "openai"},
        agent_config=agent_config,
    )
    text = runtime_result.get("result", {}).get("text", "")
    messenger.send_message(
        channel,
        text,
        sender=agent_id,
        role="assistant",
        agent_id=agent_id,
    )

    return {
        "status": "ok",
        "agent": agent_id,
        "message": "Slack broadcast created",
        "runtime_result": runtime_result,
    }
