from models.domain import InputRow


class AbstractLoader:
    def load(self, filename: str) -> list[InputRow]:
        raise NotImplementedError
