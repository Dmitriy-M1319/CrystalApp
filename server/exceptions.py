class RowNotFoundException(BaseException):
    def __int__(self, model: str, key: str):
        self.model = model
        self.model_key = key

    @property
    def __str__(self):
        return f'Row from model {self.model} with key {self.model_key} not found'
