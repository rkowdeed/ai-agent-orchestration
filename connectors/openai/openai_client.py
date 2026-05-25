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
