import json
from typing import Optional

import requests

from .llmBackendBase import LLMBase
from .modelBase import ModelBase
from ..secrets import get_secret

class OpenRouter(LLMBase):
    def __init__(
        self,
        model: ModelBase,
        referer: Optional[str] = None,
        x_title: Optional[str] = None,
    ):
        """
        A backend for Open Router's API.

        Parameters
        ----------
        model : ModelBase
            The model to use for the backend.
        referer : Optional[str]
            The referer to use for the backend.
        x_title : Optional[str]
            The x-title to use for the backend.
        """
        self.model = model
        self.referer = referer
        self.x_title = x_title

    def completion(
        self,
        prompt: str,
        max_tokens: int = 2048,
        temperature: float = 0.8,
        override_system_message: Optional[str] = None,
    ):
        """
        Creates and returns a completion using a provided model

        Parameters
        ----------
        prompt : str
            The prompt to send to the backend.
        max_tokens : int
            The maximum number of tokens to generate.
        temperature : float
            The temperature to use for the generation.
        override_system_message : Optional[str]
            The system message to use for the generation.
        **kwargs
            Additional arguments to pass to the backend.
        """
        # Unfortunatly the API requires a bearer token to be passed in the header, so no need to check the model for auth
        # https://openrouter.ai/docs

        base_headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + get_secret("AI_PDF_OPEN_ROUTER_API_KEY"),
        }

        # These are optional headers acording to the API docs
        # https://openrouter.ai/docs
        # Setting them I think would make your request more unique and more indexable by the API ??
        if self.referer:
            base_headers["HTTP-Referer"] = self.referer
        if self.x_title:
            base_headers["x-title"] = self.x_title

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=base_headers,
            data=json.dumps(
                {
                    "model": self.model.name,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "messages": [
                        {
                            "role": "system",
                            "content": override_system_message
                            if override_system_message
                            else "You're a helpful coding assistant, that helps with repetitive tasks. Only answer the question below, do not add any additional information. Expect output to be processed by a script and not a human. Do not add characters for lists such as '*'",
                        },
                        {"role": "user", "content": prompt},
                    ],
                }
            ),
        )
        # I don't really like this, but I don't want to write a bunch of code to handle errors on a toy project
        return response.json()["choices"][0]["message"]["content"]
