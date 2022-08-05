from datetime import datetime, timedelta

from typing import Dict, Tuple, List


NameDict = Dict[str, List[Tuple[datetime, str]]]


def append_dict_list(k, v, *, d: dict):
    try:
        d[k].append(v)
    except KeyError:
        d[k] = []
        d[k].append(v)


class TardyChecker:
    def __init__(self):
        self._name_dict: NameDict = dict()

    @property
    def name_dict(self) -> NameDict:
        return self._name_dict

    def append(self, row: dict):
        """
        Append row to name dict

        Args:
            row (dict): row
        """

        self._row_validation(row)

        name = row["이름"]
        issued_datetime = row["발생시각"]
        status = row["상태"]

        issued_datetime = datetime.strptime(
            issued_datetime, "%Y-%m-%d %H:%M:%S"
        )

        append_dict_list(name, (issued_datetime, status), d=self._name_dict)

    def check(self, name: str):
        """
        Start tardy check

        Args:
            name (str): target name
        """

        v = self.name_dict[name]

        intermediate: Dict[datetime, List[Tuple[datetime, str]]] = {}
        for issued_datetime, status in v:
            append_dict_list(
                issued_datetime.date(),
                (issued_datetime, status),
                d=intermediate,
            )

        result = {}
        for k in intermediate.keys():
            v = intermediate[k]
            v.sort(key=lambda x: x[0])

            start = None
            end = None

            for issued_datetime, status in v:
                if "출근" in status:
                    if not start:
                        start = issued_datetime
                elif "퇴근" in status:
                    end = issued_datetime

            print(f"{k}일: 출근 {start} 퇴근 {end}")

            issued_date = k.strftime("%Y-%m-%d")
            if not start or not end:
                result[issued_date] = "출퇴근 기록 부족"
            else:
                required_start_time = start.replace(hour=10, minute=0)
                required_end_time = start.replace(hour=19, minute=0)

                start_tardy = (
                    start - required_start_time
                ).total_seconds() / 60
                end_tardy = (required_end_time - end).total_seconds() / 60

                tardy_time: int = 0

                if start_tardy > 0:
                    tardy_time += int(start_tardy)

                if end_tardy > 0:
                    tardy_time += int(end_tardy)

                if tardy_time > 0:
                    result[issued_date] = tardy_time

        return result

    def _row_validation(self, row: dict):
        keys = set(row.keys())

        if not {"발생시각", "이름", "상태"} & keys:
            raise ValueError("Required 발생시각, 이름, 상태 in header")
