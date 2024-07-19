import csv

from src.converters.base import AbstractConverter
from models.domain import Report


class CSVConverter(AbstractConverter):
    extension = 'csv'

    def convert(self, report: Report, output: str = 'result') -> None:
        filename = f'{output}_{report.created_at.isoformat()}.{self.extension}'

        with open(filename, 'w') as f:
            writer: csv.DictWriter = csv.DictWriter(f, fieldnames=report.fields())
            writer.writeheader()

            for row in report.data:
                writer.writerow(row.to_dict())
