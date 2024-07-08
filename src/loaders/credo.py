import csv

from src.domain import ReportData
from src.loaders.base import AbstractLoader


class CredoBankLoader(AbstractLoader):
    fields = (
        'თარიღი',                          # date
        'ოპერაცია',                        # ?
        'ბრუნვა (დებ)',                    # amount
        'ბრუნვა (კრ)',                     # ?
        'ნაშთი',                           # remains დანიშნულება
        'დანიშნულება',                     # description
        'ბენეფიციარის სახელი',             # beneficiary
        'ბენეფიციარის ანგარიშის ნომერი',   # beneficiary account
    )

    def load(self, filename: str) -> ReportData:
        with open(filename) as f:
            reader: csv.DictReader = csv.DictReader(f, fieldnames=self.fields)
            next(reader)  # skip header
            data = list(reader)

        return data  # type: ignore[return-value]
