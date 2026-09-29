import os
import requests
import json
from typing import Dict, Any, Optional

class LLMClient:
    """
    Cliente universal para conexão com modelos de linguagem:
    - Locais (offline) via Ollama (ex: qwen2.5:7b, qwen2.5:32b, deepseek-r1:32b, llama3.3:70b)
    - Online de alta potência via Google Gemini (ex: gemini-1.5-pro, gemini-2.0-flash)
    - Online via OpenAI (ex: gpt-4o, gpt-4o-mini)
    """

    def __init__(
        self,
        model_name: str = "qwen2.5:7b",
        provider: str = "ollama",
        base_url: str = "http://localhost:11434",
        api_key: Optional[str] = None
    ):
        self.provider = provider.lower().strip()
        self.model_name = model_name
        self.base_url = base_url.rstrip("/")
        
        # Recupera chave de API conforme provedor ou variável de ambiente
        if api_key:
            self.api_key = api_key
        elif self.provider in ["gemini", "google"]:
            self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        elif self.provider in ["openai", "chatgpt"]:
            self.api_key = os.getenv("OPENAI_API_KEY")
        else:
            self.api_key = None

    def check_connection(self) -> bool:
        """Verifica a conexão com o provedor selecionado."""
        if self.provider in ["gemini", "google"]:
            if not self.api_key:
                print("❌ Erro: Chave de API do Gemini não encontrada.")
                print("Defina a variável GEMINI_API_KEY ou use --api-key.")
                return False
            return True
        elif self.provider in ["openai", "chatgpt"]:
            if not self.api_key:
                print("❌ Erro: Chave de API da OpenAI não encontrada.")
                print("Defina a variável OPENAI_API_KEY ou use --api-key.")
                return False
            return True
        else:  # Ollama local
            try:
                res = requests.get(f"{self.base_url}/api/tags", timeout=5)
                if res.status_code == 200:
                    models = [m.get("name") for m in res.json().get("models", [])]
                    if any(self.model_name in m or m in self.model_name for m in models):
                        return True
                    if models:
                        print(f"⚠️ Modelo '{self.model_name}' não encontrado diretamente. Modelos disponíveis: {models}")
                        return True
                return False
            except Exception:
                return False

    def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.3) -> str:
        """
        Envia a requisição de geração para o provedor selecionado (Ollama, Gemini ou OpenAI).
        """
        if self.provider in ["gemini", "google"]:
            return self._generate_gemini(prompt, system_prompt, temperature)
        elif self.provider in ["openai", "chatgpt"]:
            return self._generate_openai(prompt, system_prompt, temperature)
        else:
            return self._generate_ollama(prompt, system_prompt, temperature)

    def _generate_ollama(self, prompt: str, system_prompt: Optional[str], temperature: float) -> str:
        endpoint = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_ctx": 16384
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
            raise RuntimeError(f"Falha ao gerar resposta com Ollama '{self.model_name}': {e}")

    def _generate_gemini(self, prompt: str, system_prompt: Optional[str], temperature: float) -> str:
        if not self.api_key:
            raise ValueError("Chave de API do Gemini não configurada.")
        
        # Formata endpoint oficial da API REST v1beta do Gemini
        model = self.model_name if "gemini" in self.model_name else "gemini-1.5-pro"
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
        
        contents = [{"parts": [{"text": prompt}]}]
        payload: Dict[str, Any] = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": 8192
            }
        }
        if system_prompt:
            payload["systemInstruction"] = {
                "parts": [{"text": system_prompt}]
            }

        try:
            response = requests.post(endpoint, json=payload, timeout=300)
            if response.status_code == 200:
                data = response.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "").strip()
                return ""
            else:
                raise RuntimeError(f"Erro na API Gemini (Status {response.status_code}): {response.text}")
        except Exception as e:
            raise RuntimeError(f"Falha na comunicação com o Gemini ({model}): {e}")

    def _generate_openai(self, prompt: str, system_prompt: Optional[str], temperature: float) -> str:
        if not self.api_key:
            raise ValueError("Chave de API da OpenAI não configurada.")
        
        endpoint = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model_name if self.model_name != "qwen2.5:7b" else "gpt-4o",
            "messages": messages,
            "temperature": temperature
        }

        try:
            response = requests.post(endpoint, headers=headers, json=payload, timeout=300)
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
            else:
                raise RuntimeError(f"Erro na API OpenAI (Status {response.status_code}): {response.text}")
        except Exception as e:
            raise RuntimeError(f"Falha na comunicação com a OpenAI: {e}")

# Compatibilidade retroativa com código existente
LocalLLMClient = LLMClient
