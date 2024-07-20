import json
import os
from pathlib import Path
from typing import TypeAlias

from models.domain import Category


ExpensesToCategories: TypeAlias = dict[str, str]


class ExpenseClassifier:
    _categories: ExpensesToCategories = {}
    _directory = Path('categories')

    def classify(self, entry: str) -> Category | str:
        temp = entry.lower()
        for name, category in self.categories.items():
            if name.lower() in temp:
                return Category(category)
        return entry

    @property
    def categories(self) -> ExpensesToCategories:
        if not self._categories:
            self._categories = self._load()
        return self._categories

    def _load(self) -> ExpensesToCategories:
        categories: ExpensesToCategories = {}

        for filename in os.listdir(self._directory):
            if not filename.endswith('.json'):
                continue

            with open(self._directory / filename) as f:
                categories |= json.load(f)

        return categories
