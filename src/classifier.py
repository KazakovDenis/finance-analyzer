import json
import os
from pathlib import Path
from typing import TypeAlias

from models.domain import Category


ExpensesToCategories: TypeAlias = dict[str, str]


class ExpenseClassifier:
    _categories: ExpensesToCategories = {}
    _directory = Path('categories')
    _extension = '.json'

    def __init__(self, use_unknown: bool = True):
        self._use_unknown = use_unknown

    def classify(self, entry: str) -> Category | str:
        temp = entry.lower()

        for name, category in self.categories.items():
            if name.lower() in temp:
                return Category(category)

        if self._use_unknown:
            return Category.UNKNOWN
        return entry

    @property
    def categories(self) -> ExpensesToCategories:
        if not self._categories:
            self._categories = self._load()
        return self._categories

    def _load(self) -> ExpensesToCategories:
        categories: ExpensesToCategories = {}

        for filename in os.listdir(self._directory):
            if not filename.endswith(self._extension):
                continue

            with open(self._directory / filename) as f:
                data: dict[str, list[str]] = json.load(f)

            inverted = {}
            for category, expense in data.items():
                for name in expense:
                    inverted[name] = category

            categories |= inverted

        return categories
