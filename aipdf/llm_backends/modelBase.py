from abc import ABC
from typing import List


class ModelBase(ABC):
    def __init__(
        self, name: str, requires_auth: bool, supported_backends: List[str], **kwargs
    ):
        """
        A base class for models.

        Parameters
        ----------
        name : str
            The name of the model.
        requires_auth : bool
            Whether the model requires authentication.
        supported_backends : List[str]
            The supported backends for the model.
        **kwargs
            Additional arguments to pass to the model.
        """
        self.name = name
        self.requires_auth = requires_auth
        self.supported_backends = supported_backends

        for key, value in kwargs.items():
            setattr(self, key, value)

    def assert_backend_support(self, backend: str):
        """
        Asserts that the model supports the given backend.

        Parameters
        ----------
        backend : str
            The backend to check.
        """
        assert (
            backend in self.supported_backends
        ), f"Model {self.name} does not support backend {backend}."

    def default_system_message(self) -> str:
        """
        Returns the default system message for the model.

        Returns
        -------
        str
            The default system message for the model.
        """
        return "You're a helpful AI, please help the user the best you can. Be as concise and short as possible."

    def requires_auth(self) -> bool:
        return self.requires_auth

    def set_auth(self, auth: str):
        """
        Sets the authentication token for the model.

        Parameters
        ----------
        auth : str
            The authentication token to use for the model.
        """
        self.auth = auth

    def requires_post_format(self) -> bool:
        """
        Returns whether the model requires a post format.

        Returns
        -------
        bool
            Whether the model requires a post format.
        """
        return False

    def format(self, unformatted_prompt: str) -> str:
        """
        This provides a post format for the prompt if the model requires it.

        Parameters
        ----------

        unformatted_prompt : str
            The unformatted prompt.

        Returns
        -------
        str
            The formatted prompt.
        """
        return unformatted_prompt
