from models.domain import Verbosity
from src.calculator import Calculator
from src.classifier import ExpenseClassifier
from src.converters.csv import CSVConverter
from src.loaders.credo import CredoBankLoader


def run(
    loader: CredoBankLoader,
    calculator: Calculator,
    converter: CSVConverter,
    verbosity: Verbosity,
):
    input_data = loader.load('filename.csv')
    output_data = calculator.calc(input_data, verbosity)
    converter.convert(output_data)


if __name__ == '__main__':
    run(
        loader=CredoBankLoader(
            classifier=ExpenseClassifier(),
        ),
        calculator=Calculator(),
        converter=CSVConverter(),
        verbosity=Verbosity.MONTH,
    )
