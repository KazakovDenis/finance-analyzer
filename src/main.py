from models.domain import Verbosity
from src.calculator import Calculator
from src.classifier import ExpenseClassifier
from src.converters.csv import CSVConverter
from src.loaders.base import AbstractLoader
from src.loaders.auto import AutoLoader


def run(
    loader: AbstractLoader,
    calculator: Calculator,
    converter: CSVConverter,
    verbosity: Verbosity,
):
    input_data = loader.load()
    output_data = calculator.calc(input_data, verbosity)
    converter.convert(output_data)


if __name__ == '__main__':
    run(
        loader=AutoLoader(
            classifier=ExpenseClassifier(),
        ),
        calculator=Calculator(),
        converter=CSVConverter(),
        verbosity=Verbosity.MONTH,
    )
