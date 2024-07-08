from datetime import datetime
from zoneinfo import ZoneInfo

from src.domain import Report


class Builder:
    def build(self, data) -> Report:
        dt = datetime.now(ZoneInfo('UTC'))
        return Report(data=data, created_at=dt)
