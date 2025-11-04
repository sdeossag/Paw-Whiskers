from django.utils.translation import gettext as _
import os
from groq import Groq
from abc import ABC, abstractmethod

class LLMAdapter(ABC):
    @abstractmethod
    def complete(self, messages: list[dict]) -> str:
        pass

class GroqAdapter(LLMAdapter):
    def __init__(self, model=None, api_key=None):
        self.client = Groq(api_key=api_key or os.getenv(_("GROQ_API_KEY")))
        self.model = model or os.getenv(_("GROQ_MODEL"), _("llama-3.1-8b-instant"))

    def complete(self, messages: list[dict]) -> str:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=300
        )
        return resp.choices[0].message.content.strip()

def get_llm_instance():
    try:
        return GroqAdapter()
    except Exception as e:
        print(f"Error inicializando LLM: {e}")
        return None