import csv
from enum import Enum
from os import PathLike
from typing import TypedDict

from dateutil.parser import parse

from exceptions import EmptyReport
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
            input_data = list(reader)

        if not input_data:
            raise EmptyReport(filename)

        return self._transform(input_data)

    def _transform(self, input_data: list[dict]) -> list[InputRow]:
        # Credo provides separate report for each currency
        currency = self._detect_currency(input_data)
        output_data = []

        for row in input_data:
            descr = row[_Field.DESCRIPTION]
            output_data.append(
                InputRow(
                    source=self.source,
                    timestamp=parse(row[_Field.DATE]),
                    amount=Amount(row[_Field.AMOUNT]),
                    currency=currency,
                    description=descr,
                    category=self._classifier.classify(descr),
                    type=self._detect_type(descr),
                )
            )
        return output_data

    @staticmethod
    def _detect_currency(input_data: list[dict]) -> Currency:
        if ' GEL ' in input_data[0][_Field.DESCRIPTION]:
            return Currency.GEL
        return Currency.USD

    @staticmethod
    def _detect_type(description: str) -> TransferType:
        # TODO
        return TransferType.OUTGOING
