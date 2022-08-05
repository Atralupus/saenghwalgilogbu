import csv
from .parser import Parser


class CSVParser(Parser):
    def __init__(self):
        super().__init__()

    def parse(self, path: str):
        with open(path, newline="") as f:
            spamreader = csv.DictReader(f, delimiter=",")

            for row in spamreader:
                print(row)
