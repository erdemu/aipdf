from abc import ABC, abstractmethod
from typing import Optional


class LLMBase(ABC):
    @abstractmethod
    def completion(
        self,
        prompt: str,
        max_tokens: int = 2048,
        temperature: float = 0.8,
        override_system_message: Optional[str] = None,
        **kwargs
    ):
        """
        Generates text from a prompt using a large language model, designed to be a common interface for all backends.

        This method should be implemented by any backend.

        Parameters:
        -----------
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
        pass
