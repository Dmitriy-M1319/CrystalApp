class RowNotFoundException(BaseException):
    def __int__(self, model: str, model_id: int):
        self.model = model
        self.model_id = model_id

    @property
    def __str__(self):
        return f'Row from model {self.model} with primary key {self.model_id} not found'