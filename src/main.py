from src.builder import Builder
from src.converters.csv import CSVConverter
from src.loaders.credo import CredoBankLoader


def main():
    loader = CredoBankLoader()
    data = loader.load('report.csv')

    builder = Builder()
    report = builder.build(data)

    converter = CSVConverter()
    converter.convert(report)


if __name__ == '__main__':
    main()
