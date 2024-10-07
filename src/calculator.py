from datetime import datetime
from zoneinfo import ZoneInfo

from models.domain import Entry, Report, InputRow, ReportRow, Verbosity, Currency
from src.rate_fetcher import CurrencyRateFetcher


class Calculator:
    def __init__(self, fetcher: CurrencyRateFetcher, to_currency: Currency, verbosity: Verbosity):
        self._fetcher = fetcher
        self._target = to_currency
        self._verbosity = verbosity

    def calc(self, input_data: list[InputRow]) -> Report:
        dt = datetime.now(ZoneInfo('UTC'))

        if self._verbosity == Verbosity.TRANSACTION:
            return Report(data=input_data, created_at=dt)

        data: dict[Entry, ReportRow] = {}

        for row in input_data:
            report_row = row.to_report(self._verbosity)
            self._update_amount(report_row)
            entry = report_row.to_entry()

            if entry not in data:
                data[entry] = report_row
            else:
                data[entry].amount += report_row.amount

        output_data = sorted(list(data.values()))
        return Report(data=output_data, created_at=dt)

    def _update_amount(self, row: ReportRow) -> None:
        if row.currency == self._target:
            return

        rate = self._fetcher.fetch(row.currency, self._target, row.timestamp)
        row.amount *= rate
        row.currency = self._target
