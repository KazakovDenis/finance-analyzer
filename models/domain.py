from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import TypeAlias, Union

Amount: TypeAlias = float
Entry: TypeAlias = tuple[datetime, Union['Category', str], 'Currency']


class Category(str, Enum):
    ANIMAL = 'Животные'
    BEAUTY = 'Красота'
    CHILD = 'Ребёнок'
    COMMISSION = 'Комиссии'
    EXCHANGE = 'Обмен валют'
    FOOD = 'Продукты'
    GOODS = 'Покупки'
    HEALTH = 'Здоровье'
    RECREATION = 'Отдых'
    TRANSFER = 'Переводы'
    TRANSPORT = 'Транспорт'
    UNKNOWN = 'Остальное'
    UTILITY = 'Коммунальные услуги'


class Currency(str, Enum):
    GEL = 'GEL'
    RUB = 'RUB'
    TRY = 'TRY'
    USD = 'USD'


class TransferType(str, Enum):
    INCOMING = 'INCOMING'
    OUTGOING = 'OUTGOING'
    EXCHANGE = 'EXCHANGE'


class Verbosity(str, Enum):
    TRANSACTION = 'TRANSACTION'
    DAY = 'DAY'
    MONTH = 'MONTH'
    YEAR = 'YEAR'


@dataclass(order=True)
class ReportRow:
    timestamp: datetime
    category: Category | str
    currency: Currency
    amount: Amount

    def to_dict(self) -> dict:
        return self.__dict__

    def to_entry(self) -> Entry:
        return (
            self.timestamp,
            self.category,
            self.currency,
        )


@dataclass
class InputRow(ReportRow):
    source: str
    description: str
    type: TransferType

    def to_report(self, verbosity: Verbosity) -> ReportRow:
        return ReportRow(
            timestamp=self._round_timestamp(verbosity),
            category=self.category,
            currency=self.currency,
            amount=self.amount,
        )

    def _round_timestamp(self, verbosity: Verbosity) -> datetime:
        match verbosity:
            case Verbosity.DAY:
                return datetime(
                    year=self.timestamp.year,
                    month=self.timestamp.month,
                    day=self.timestamp.day,
                )
            case Verbosity.MONTH:
                return datetime(
                    year=self.timestamp.year,
                    month=self.timestamp.month,
                    day=1,
                )
            case Verbosity.YEAR:
                return datetime(
                    year=self.timestamp.year,
                    month=1,
                    day=1,
                )
        return self.timestamp


@dataclass
class Report:
    data: list[InputRow] | list[ReportRow]
    created_at: datetime

    @classmethod
    def fields(cls) -> list[str]:
        return list(ReportRow.__dataclass_fields__.keys())
