from src.domain import ReportData


class AbstractLoader:

    def load(self, *args, **kwargs) -> ReportData:
        raise NotImplementedError
