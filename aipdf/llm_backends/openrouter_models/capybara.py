from ..modelBase import ModelBase

class Capybara7b(ModelBase):
    def __init__(self, **kwargs):
        super().__init__("nousresearch/nous-capybara-7b", True, ["open-router"], **kwargs)
