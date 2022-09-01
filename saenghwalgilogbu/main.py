from datetime import datetime
from typing import Optional

from saenghwalgilogbu.builder import build_csv
from saenghwalgilogbu.parser import CSVParser
from saenghwalgilogbu.tardy_checker import TardyChecker


def main(
    name: str,
    data_sheet_path: str,
    *,
    exception_map_path: Optional[str] = None,
):
    print(name, "지각 체크")

    parser = CSVParser()

    exception_dict = {}

    if exception_map_path:
        for r in parser.parse(exception_map_path):
            d = r["날짜"]
            s = (
                datetime.strptime(f"{d} {r['근무시작시간']}", "%Y-%m-%d %H:%M")
                if r["근무시작시간"] != "0"
                else None
            )
            e = (
                datetime.strptime(f"{d} {r['근무종료시간']}", "%Y-%m-%d %H:%M")
                if r["근무종료시간"] != "0"
                else None
            )

            exception_dict[d] = (s, e)

    tardy_checker = TardyChecker(exception_dict)

    for r in parser.parse(data_sheet_path):
        tardy_checker.append(r)

    r = tardy_checker.check(name)

    with open(f"./output/{name}.csv", mode="w") as f:
        f.write(build_csv(name, r))
