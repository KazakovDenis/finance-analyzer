from datetime import datetime
from zoneinfo import ZoneInfo

from models.domain import Entry, Report, InputRow, ReportRow, Verbosity


class Calculator:
    def calc(self, input_data: list[InputRow], verbosity: Verbosity) -> Report:
        dt = datetime.now(ZoneInfo('UTC'))

        if verbosity == Verbosity.TRANSACTION:
            return Report(data=input_data, created_at=dt)

        data: dict[Entry, ReportRow] = {}

        for row in input_data:
            report_row = row.to_report(verbosity)
            entry = report_row.to_entry()

            if entry not in data:
                data[entry] = report_row
            else:
                data[entry].amount += report_row.amount

        output_data = sorted(list(data.values()))
        return Report(data=output_data, created_at=dt)
