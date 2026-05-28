from typing import Any, Dict, List
import os

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.services.agent_manager import AgentManager
from app.services.messaging import InMemoryMessenger
from app.services.persistence import SQLitePersistence
from app.services.runtime import RuntimeConnector
from app.services.slack_messenger import SlackMessenger
from app.services.workflow_runner import WorkflowRunner

router = APIRouter()


def get_persistence() -> SQLitePersistence:
    return SQLitePersistence(os.getenv("AIAGENT_DB_PATH"))


def get_agent_manager() -> AgentManager:
    return AgentManager(get_persistence())


def get_messenger() -> InMemoryMessenger:
    if os.getenv("SLACK_BOT_TOKEN"):
        return SlackMessenger(get_persistence())
    return InMemoryMessenger(get_persistence())


def get_workflow_runner() -> WorkflowRunner:
    return WorkflowRunner(get_agent_manager(), get_messenger(), RuntimeConnector())


class AgentConfig(BaseModel):
    name: str | None = None
    role: str | None = None
    system_prompt: str | None = None
    model: str | None = "gpt-4o-mini"
    tools: list[str] = []
    channels: list[str] = ["default"]
    schedules: dict[str, Any] | None = None
    memory: dict[str, Any] | None = None
    skills: list[dict[str, Any]] = []
    interaction_rules: dict[str, Any] | None = None
    guardrails: dict[str, Any] | None = None


class AgentCreateRequest(BaseModel):
    agent_id: str
    config: AgentConfig = Field(default_factory=AgentConfig)


class AgentUpdateRequest(BaseModel):
    config: AgentConfig


class WorkflowRunRequest(BaseModel):
    channel: str = "default"
    text: str | None = None
    prompt: str | None = None
    runtime: str | None = None
    template: str | None = None


class WorkflowRunResponse(BaseModel):
    status: str
    agent: str
    message: str
    runtime_result: dict | None = None


class MessageResponse(BaseModel):
    id: int
    agent_id: str | None = None
    sender: str
    role: str
    channel: str
    text: str
    created_at: str


@router.post("/agents")
async def create_agent(body: AgentCreateRequest):
    try:
        config = body.config.model_dump(exclude_none=True)
        agent = get_agent_manager().create_agent(body.agent_id, config)
        return {"agent_id": agent.agent_id, "config": agent.config}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/agents")
async def list_agents():
    return {"agents": get_agent_manager().list_agents()}


@router.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    try:
        agent = get_agent_manager().get_agent(agent_id)
        return {"agent_id": agent.agent_id, "config": agent.config}
    except KeyError:
        raise HTTPException(status_code=404, detail="agent not found")


@router.put("/agents/{agent_id}")
async def update_agent(agent_id: str, body: AgentUpdateRequest):
    try:
        config = body.config.dict(exclude_none=True)
        agent = get_agent_manager().update_agent(agent_id, config)
        return {"agent_id": agent.agent_id, "config": agent.config}
    except KeyError:
        raise HTTPException(status_code=404, detail="agent not found")


@router.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str):
    try:
        get_agent_manager().delete_agent(agent_id)
        return {"status": "deleted", "agent_id": agent_id}
    except KeyError:
        raise HTTPException(status_code=404, detail="agent not found")


@router.get("/agents/{agent_id}/messages", response_model=List[MessageResponse])
async def get_agent_messages(agent_id: str):
    try:
        get_agent_manager().get_agent(agent_id)
        return get_messenger().get_messages(agent_id=agent_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="agent not found")


@router.get("/messages", response_model=List[MessageResponse])
async def list_messages(
    agent_id: str | None = Query(None), channel: str | None = Query(None)
):
    return get_messenger().get_messages(agent_id=agent_id, channel=channel)


@router.post("/agents/{agent_id}/run", response_model=WorkflowRunResponse)
async def run_agent_workflow(agent_id: str, body: WorkflowRunRequest):
    try:
        result = await get_workflow_runner().run_workflow(agent_id, {
            "channel": body.channel,
            "text": body.text or f"Executing workflow for {agent_id}",
            "prompt": body.prompt,
            "runtime": body.runtime,
            "template": body.template,
        })
        return result
    except KeyError:
        raise HTTPException(status_code=404, detail="agent not found")
