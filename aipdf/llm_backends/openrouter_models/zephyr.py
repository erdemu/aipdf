from ..modelBase import ModelBase

class Zephyr7b(ModelBase):
    def __init__(self, **kwargs):
        super().__init__("huggingfaceh4/zephyr-7b-beta", True, ["open-router"], **kwargs)
