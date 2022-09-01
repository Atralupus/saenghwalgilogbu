from saenghwalgilogbu.tardy_checker import TardyChecker
from datetime import datetime


def test_check_exception_map():
    start = datetime(year=2022, month=8, day=3, hour=9, minute=30)
    end = datetime(year=2022, month=8, day=3, hour=18, minute=30)
    exception_map = {"2022-08-03": (start, end)}

    checker = TardyChecker(exception_map)

    v = {"발생시각": "2022-08-03 09:30:00", "상태": "출근", "이름": "홍길동"}
    checker.append(v)
    v = {"발생시각": "2022-08-03 18:30:00", "상태": "퇴근", "이름": "홍길동"}
    checker.append(v)

    r = checker.check("홍길동")

    assert r == {}


def test_check_tardy_exception_map():
    start = datetime(year=2022, month=8, day=3, hour=9, minute=30)
    end = datetime(year=2022, month=8, day=3, hour=18, minute=30)
    exception_map = {"2022-09-03": (start, end)}

    checker = TardyChecker(exception_map)

    v = {"발생시각": "2022-09-03 10:00:00", "상태": "출근", "이름": "홍길동"}
    checker.append(v)
    v = {"발생시각": "2022-09-03 19:00:00", "상태": "퇴근", "이름": "홍길동"}
    checker.append(v)

    r = checker.check("홍길동")

    assert r == {"2022-09-03 10:00:00": (30, "지각")}


def test_check_vacation_exception_map():
    start = None
    end = None
    exception_map = {"2022-09-04": (start, end)}

    checker = TardyChecker(exception_map)

    v = {"발생시각": "2022-09-04 10:00:00", "상태": "출근", "이름": "홍길동"}
    checker.append(v)
    v = {"발생시각": "2022-09-04 19:00:00", "상태": "퇴근", "이름": "홍길동"}
    checker.append(v)

    r = checker.check("홍길동")

    assert r == {}
