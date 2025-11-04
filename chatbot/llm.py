import os
from groq import Groq
from abc import ABC, abstractmethod

class LLMAdapter(ABC):
    @abstractmethod
    def complete(self, messages: list[dict]) -> str:
        pass

class GroqAdapter(LLMAdapter):
    def __init__(self, model=None, api_key=None):
        # ✅ SIN traducir - son nombres de variables de entorno
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY no está configurada. Agrega la clave en tu archivo .env")
        
        self.client = Groq(api_key=self.api_key)
        self.model = model or os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    def complete(self, messages: list[dict]) -> str:
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=300
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error en completación LLM: {e}")
            raise

def get_llm_instance():
    """Retorna una instancia del LLM o None si hay error"""
    try:
        return GroqAdapter()
    except Exception as e:
        print(f"Error inicializando LLM: {e}")
        return None