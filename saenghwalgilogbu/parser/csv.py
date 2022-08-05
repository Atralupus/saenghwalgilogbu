import csv
from typing import Iterator
from .parser import Parser


class CSVParser(Parser):
    def __init__(self):
        super().__init__()

    def parse(self, path: str) -> Iterator[dict]:
        with open(path, newline="") as f:
            spamreader = csv.DictReader(f, delimiter=",")

            for row in spamreader:
                yield row
