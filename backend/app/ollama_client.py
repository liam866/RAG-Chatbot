import httpx
import json
import logging

logger = logging.getLogger(__name__)

class OllamaError(Exception):
    pass

class OllamaClient:
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model
        self.http_client = httpx.Client(timeout=60.0)

    def generate(self, prompt: str) -> str:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,  # We'll get the full response at once
        }
        
        try:
            logger.info(f"Sending request to Ollama: {url}")
            response = self.http_client.post(url, json=payload)
            response.raise_for_status()
            
            response_data = response.json()
            
            if "response" in response_data:
                return response_data["response"].strip()
            else:
                logger.error(f"Unexpected Ollama response format: {response_data}")
                raise OllamaError("Ollama response did not contain 'response' field.")

        except httpx.RequestError as e:
            logger.error(f"Could not connect to Ollama at {self.base_url}. Error: {e}")
            raise OllamaError(f"Could not connect to Ollama. Please ensure it is running and accessible at {self.base_url}")
        except httpx.HTTPStatusError as e:
            logger.error(f"Ollama returned an error status {e.response.status_code}: {e.response.text}")
            raise OllamaError(f"Ollama returned an error: {e.response.status_code}")
