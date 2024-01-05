from ..modelBase import ModelBase

class Mixtral8x7bInstructBeta(ModelBase):
    def __init__(self, **kwargs):
        super().__init__("mistralai/mixtral-8x7b-instruct", True, ["open-router"], **kwargs)
