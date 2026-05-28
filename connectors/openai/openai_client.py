import os
import httpx

class OpenAIClient:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.base = 'https://api.openai.com/v1'
        self._client = httpx.AsyncClient()

    async def list_models(self):
        headers = {'Authorization': f'Bearer {self.api_key}'}
        r = await self._client.get(f'{self.base}/models', headers=headers)
        r.raise_for_status()
        return r.json()

    async def create_completion(
        self,
        messages: list[dict[str, str]],
        model: str = 'gpt-4o-mini',
    ):
        if not self.api_key:
            raise ValueError('OpenAI API key is required')
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        data = {
            'model': model,
            'messages': messages,
            'max_tokens': 300,
        }
        r = await self._client.post(f'{self.base}/chat/completions', headers=headers, json=data)
        r.raise_for_status()
        return r.json()
