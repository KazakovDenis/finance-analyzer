import csv
from enum import Enum
from os import PathLike
from typing import TypedDict

from dateutil.parser import parse

from models.domain import Amount, Currency, InputRow, TransferType
from src.classifier import ExpenseClassifier
from src.loaders.base import AbstractLoader


class _Field(str, Enum):
    DATE = 'თარიღი'
    TYPE = 'ოპერაცია'
    AMOUNT = 'ბრუნვა (დებ)'
    UNKNOWN = 'ბრუნვა (კრ)'
    REMAINS = 'ნაშთი'
    DESCRIPTION = 'დანიშნულება'
    BENEFICIARY = 'ბენეფიციარის სახელი'
    BNF_ACCOUNT = 'ბენეფიციარის ანგარიშის ნომერი'


class CsvRow(TypedDict):
    category: str
    currency: str
    amount: str
    type: str


class CredoBankLoader(AbstractLoader):
    source = 'CredoBank'
    fields = (
        _Field.DATE,
        _Field.TYPE,
        _Field.AMOUNT,
        _Field.UNKNOWN,
        _Field.REMAINS,
        _Field.DESCRIPTION,
        _Field.BENEFICIARY,
        _Field.BNF_ACCOUNT,
    )

    def __init__(self, classifier: ExpenseClassifier):
        self._classifier = classifier

    def load(self, filename: PathLike) -> list[InputRow]:
        with open(filename) as f:
            reader: csv.DictReader = csv.DictReader(f, fieldnames=self.fields, delimiter=';')
            next(reader)  # skip header
            data = self._transform(reader)
        return data

    def _transform(self, input_data: csv.DictReader[dict]) -> list[InputRow]:
        output_data = []
        currency = self._detect_currency(input_data)

        for row in input_data:
            trx_type = self._classifier.classify(descr := row[_Field.DESCRIPTION])

            # TODO: currency, type
            output_data.append(
                InputRow(
                    source=self.source,
                    timestamp=parse(row[_Field.DATE]),
                    amount=Amount(row[_Field.AMOUNT]),
                    currency=currency,
                    description=descr,
                    category=trx_type,
                    type=TransferType.OUTGOING,
                )
            )
        return output_data

    def _detect_currency(self, input_data: csv.DictReader[dict]) -> Currency:
        return Currency.GEL
