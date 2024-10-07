from datetime import datetime
from functools import lru_cache

from models.domain import Currency, CurrencyRate


# todo
class CurrencyRateFetcher:
    @lru_cache
    def fetch(self, c_from: Currency, c_to: Currency, dt: datetime) -> CurrencyRate:
        if c_from == c_to:
            return 1.0
        return 1 / 2.74
