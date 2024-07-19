from models.domain import Report


class AbstractConverter:
    extension: str

    def convert(self, report: Report, output: str) -> None:
        raise NotImplementedError
