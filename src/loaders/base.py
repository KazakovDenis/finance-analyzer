from models.domain import InputRow


class AbstractLoader:
    def load(self, *args, **kwargs) -> list[InputRow]:
        raise NotImplementedError
