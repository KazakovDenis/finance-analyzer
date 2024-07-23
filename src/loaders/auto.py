import os
from functools import cached_property
from pathlib import Path

from models.domain import InputRow
from src.classifier import ExpenseClassifier
from src.loaders.base import AbstractLoader
from src.loaders.credo import CredoBankLoader


class AutoLoader(AbstractLoader):
    _directory = Path('inputs')

    def __init__(self, classifier: ExpenseClassifier):
        self._classifier = classifier

    def load(self) -> list[InputRow]:
        data = []

        for path, _, filenames in os.walk(self._directory):
            for filename in filenames:
                if 'credo' in filename.lower():
                    data.extend(
                        self._credo_loader.load(Path(path) / filename),
                    )

        return data

    @cached_property
    def _credo_loader(self) -> CredoBankLoader:
        return CredoBankLoader(classifier=self._classifier)
