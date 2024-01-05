from ..modelBase import ModelBase

class GPT4_Turbo(ModelBase):
    def __init__(self, **kwargs):
        super().__init__("openai/gpt-4-1106-preview", True, ["open-router"], **kwargs)
