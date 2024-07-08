from enum import Enum

from src.domain import Category


class Recipient(tuple[str, Category], Enum):
    FRESCO = 'FRESCO', Category.FOOD
    PHARMADEPOT = 'PHARMADEPOT', Category.HEALTH
    YANDEX_GO = 'Yandex Go', Category.TRANSPORT


class ExpenseClassifier:

    @staticmethod
    def classify(entry: str) -> Recipient | str:
        for name, category in Recipient:
            if name.lower() in entry.lower():
                return category
        return entry
