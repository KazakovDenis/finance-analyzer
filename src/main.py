from models.domain import Verbosity, Currency
from src.calculator import Calculator
from src.classifier import ExpenseClassifier
from src.converters.csv import CSVConverter
from src.loaders.base import AbstractLoader
from src.loaders.auto import AutoLoader
from src.rate_fetcher import CurrencyRateFetcher


class Config:
    use_unknown = False
    to_currency = Currency.USD
    verbosity = Verbosity.YEAR


def run(
    loader: AbstractLoader,
    calculator: Calculator,
    converter: CSVConverter,
):
    input_data = loader.load()
    output_data = calculator.calc(input_data)
    converter.convert(output_data)


if __name__ == '__main__':
    run(
        loader=AutoLoader(
            classifier=ExpenseClassifier(use_unknown=Config.use_unknown),
        ),
        calculator=Calculator(
            fetcher=CurrencyRateFetcher(),
            to_currency=Config.to_currency,
            verbosity=Config.verbosity,
        ),
        converter=CSVConverter(),
    )
