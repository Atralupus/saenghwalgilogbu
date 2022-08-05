import os

from saenghwalgilogbu.parser import CSVParser
from tests.constants import DATA_DIR


cav_sample = os.path.join(DATA_DIR, "parser/csv_sample.csv")


def test_parse():
    parser = CSVParser()

    for row in parser.parse(cav_sample):
        assert row["이름"] == "홍길동"
