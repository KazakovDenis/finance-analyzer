from src.domain import Report


class AbstractConverter:
    extension: str

    def convert(self, report: Report):
        raise NotImplementedError
