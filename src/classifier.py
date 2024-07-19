from enum import Enum

from models.domain import Category


class ExpenseClassifier:
    @staticmethod
    def classify(entry: str) -> Category | str:
        for name, category in Recipient:
            if name.lower() in entry.lower():
                return category
        return entry


class Recipient(tuple[str, Category], Enum):
    FRESCO = 'FRESCO', Category.FOOD
    PHARMADEPOT = 'PHARMADEPOT', Category.HEALTH
    YANDEX_GO = 'Yandex Go', Category.TRANSPORT

    # Misc
    EXCHANGE = 'Exchange', Category.EXCHANGE
