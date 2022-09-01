from datetime import datetime, date

from typing import Dict, Tuple, List


NameDict = Dict[str, List[Tuple[datetime, str]]]
ExceptionDict = Dict[str, Tuple[datetime, datetime]]
ResultDict = Dict[str, Tuple[int, str]]


class StopLoop(Exception):
    pass


def append_dict_list(k, v, *, d: dict):
    try:
        d[k].append(v)
    except KeyError:
        d[k] = []
        d[k].append(v)


class TardyChecker:
    def __init__(self, exception_map: ExceptionDict = {}):
        self._name_dict: NameDict = dict()
        self.exception_map: ExceptionDict = exception_map

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
        raw_issued_datetime = row["발생시각"]
        status = row["상태"]

        issued_datetime = datetime.strptime(
            raw_issued_datetime, "%Y-%m-%d %H:%M:%S"
        )

        append_dict_list(
            name,
            (issued_datetime, status),
            d=self._name_dict,
        )

    def check(self, name: str) -> ResultDict:
        """
        Start tardy check

        Args:
            name (str): target name
        """

        v = self.name_dict[name]

        intermediate: Dict[date, List[Tuple[datetime, str]]] = {}
        for issued_datetime, status in v:
            append_dict_list(
                issued_datetime.date(),
                (
                    issued_datetime,
                    status,
                ),
                d=intermediate,
            )

        result: ResultDict = {}

        for k in intermediate.keys():
            try:
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

                issued_date = k.strftime("%Y-%m-%d")
                if not start:
                    result[end.strftime("%Y-%m-%d %H:%M:%S")] = (
                        -1,
                        "출근 기록 부족",
                    )
                elif not end:
                    result[start.strftime("%Y-%m-%d %H:%M:%S")] = (
                        -1,
                        "퇴근 기록 부족",
                    )
                else:
                    exception_time = self.exception_map.get(issued_date)

                    if exception_time:
                        (
                            exception_start_time,
                            exception_end_time,
                        ) = exception_time
                        if (
                            exception_start_time is None
                            or exception_end_time is None
                        ):
                            raise StopLoop

                        required_start_time = start.replace(
                            hour=exception_start_time.hour,
                            minute=exception_start_time.minute,
                        )
                        required_end_time = start.replace(
                            hour=exception_start_time.hour,
                            minute=exception_start_time.minute,
                        )
                    else:
                        required_start_time = start.replace(hour=10, minute=0)
                        required_end_time = start.replace(hour=19, minute=0)

                    start_tardy = (
                        start - required_start_time
                    ).total_seconds() / 60
                    end_tardy = (required_end_time - end).total_seconds() / 60

                    if start_tardy > 0:
                        result[start.strftime("%Y-%m-%d %H:%M:%S")] = (
                            int(start_tardy),
                            "지각",
                        )

                    if end_tardy > 0:
                        result[end.strftime("%Y-%m-%d %H:%M:%S")] = (
                            int(end_tardy),
                            "조퇴",
                        )
            except StopLoop:
                pass

        return result

    def _row_validation(self, row: dict):
        keys = set(row.keys())

        if not {"발생시각", "이름", "상태"} & keys:
            raise ValueError("Required 발생시각, 이름, 상태 in header")
