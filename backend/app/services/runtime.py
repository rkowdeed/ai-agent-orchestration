import os
from typing import Any, Dict, Optional

from connectors.openai.openai_client import OpenAIClient
from connectors.autogen.autogen_client import is_available, demo_info


class RuntimeConnector:
    def __init__(self, openai_api_key: Optional[str] = None):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self._openai_client = OpenAIClient(self.openai_api_key)

    async def execute(
        self,
        runtime: str,
        agent_id: str,
        payload: Dict[str, Any],
        agent_config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if runtime == "openai":
            return await self._run_openai(agent_id, payload, agent_config)
        if runtime == "autogen":
            return self._run_autogen(agent_id, payload)
        return {"status": "skipped", "reason": "no runtime selected"}

    async def _run_openai(
        self,
        agent_id: str,
        payload: Dict[str, Any],
        agent_config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if not self.openai_api_key:
            return {"status": "error", "reason": "OpenAI API key not configured"}

        config = agent_config or {}
        system_prompt = config.get("system_prompt") or f"You are agent {agent_id}."
        model = config.get("model", "gpt-4o-mini")
        prompt = payload.get("prompt") or payload.get("text") or f"Run workflow for agent {agent_id}"
        memory = config.get("memory")

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
        if memory:
            messages.append({"role": "system", "content": f"Memory: {memory}"})

        completion = await self._openai_client.create_completion(
            messages=messages,
            model=model,
        )

        content = ""
        if completion.get("choices"):
            choice = completion["choices"][0]
            content = choice.get("message", {}).get("content", "")

        return {
            "status": "ok",
            "agent": agent_id,
            "result": {
                "text": content,
                "raw": completion,
            },
        }

    def _run_autogen(self, agent_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "status": "skipped",
            "reason": demo_info(),
            "agent": agent_id,
            "payload": payload,
        }
