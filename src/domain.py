from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import TypeAlias


class Category(str, Enum):
    FOOD = 'Продукты'
    HEALTH = 'Здоровье'
    RECREATION = 'Отдых'
    TRANSPORT = 'Транспорт'


class Currency(str, Enum):
    GEL = 'GEL'
    RUB = 'RUB'
    TRY = 'TRY'
    USD = 'USD'


class TransferType(str, Enum):
    EXCHANGE = 'EXCHANGE'
    PAYMENT = 'PAYMENT'
    P2P = 'P2P'


@dataclass
class ReportRow:
    transferred_at: datetime
    amount: float
    currency: Currency
    description: str
    type: TransferType | None  # detected later


ReportData: TypeAlias = list[ReportRow]


@dataclass
class Report:
    data: ReportData
    created_at: datetime
