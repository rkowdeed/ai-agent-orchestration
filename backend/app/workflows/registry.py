from typing import Callable, Dict, Any

from .slack_broadcast import slack_broadcast_workflow
from .two_agent_conversation import two_agent_conversation_workflow

WorkflowCallable = Callable[[Any, Any, Any, str, Dict[str, Any]], Any]

WORKFLOW_TEMPLATES: Dict[str, WorkflowCallable] = {
    "two-agent-conversation": two_agent_conversation_workflow,
    "slack-broadcast": slack_broadcast_workflow,
}


def get_workflow_template(name: str) -> WorkflowCallable:
    if name not in WORKFLOW_TEMPLATES:
        raise KeyError(f"workflow template '{name}' not found")
    return WORKFLOW_TEMPLATES[name]
