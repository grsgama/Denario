import requests
import json
from typing import Dict, Any, Optional

class LocalLLMClient:
    """
    Cliente para conexão com modelos de linguagem locais (offline) via Ollama ou API compatível.
    """

    def __init__(self, model_name: str = "qwen2.5:7b", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url.rstrip("/")

    def check_connection(self) -> bool:
        """Verifica se o servidor Ollama está acessível e se o modelo está carregado."""
        try:
            res = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if res.status_code == 200:
                models = [m.get("name") for m in res.json().get("models", [])]
                # Aceita correspondência exata ou parcial do modelo
                if any(self.model_name in m or m in self.model_name for m in models):
                    return True
                # Se Ollama responder mas o modelo exato não estiver listado, tenta usar o primeiro disponível
                if models:
                    print(f"⚠️ Modelo '{self.model_name}' não encontrado diretamente. Modelos disponíveis: {models}")
                    return True
            return False
        except Exception:
            return False

    def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.3) -> str:
        """
        Envia uma requisição de geração para o Ollama local e retorna a resposta de texto.
        """
        endpoint = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_ctx": 8192  # Janela de contexto ampliada para leitura de seções longas
            }
        }
        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(endpoint, json=payload, timeout=600)
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            else:
                raise RuntimeError(f"Erro na API Ollama (Status {response.status_code}): {response.text}")
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Não foi possível conectar ao Ollama em '{self.base_url}'. "
                f"Certifique-se de que o servidor esteja em execução com 'ollama serve'."
            )
        except Exception as e:
            raise RuntimeError(f"Falha ao gerar resposta com a LLM local '{self.model_name}': {e}")
