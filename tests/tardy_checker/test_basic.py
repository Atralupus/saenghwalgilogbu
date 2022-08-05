from saenghwalgilogbu.tardy_checker import TardyChecker
from datetime import datetime


def test_append():
    checker = TardyChecker()

    v = {"발생시각": "2022-08-03 15:03:48", "상태": "출입", "이름": "홍길동"}
    checker.append(v)

    assert checker.name_dict == {
        "홍길동": [
            (
                datetime.strptime("2022-08-03 15:03:48", "%Y-%m-%d %H:%M:%S"),
                "출입",
            )
        ]
    }


def test_check():
    checker = TardyChecker()

    v = {"발생시각": "2022-08-02 10:03:48", "상태": "출근", "이름": "홍길동"}
    checker.append(v)
    v = {"발생시각": "2022-08-02 19:00:48", "상태": "퇴근", "이름": "홍길동"}
    checker.append(v)

    r = checker.check("홍길동")

    assert r == {"2022-08-02": 3}


def test_check_no_tardy():
    checker = TardyChecker()

    v = {"발생시각": "2022-08-01 09:59:00", "상태": "출근", "이름": "홍길동"}
    checker.append(v)
    v = {"발생시각": "2022-08-01 19:00:48", "상태": "퇴근", "이름": "홍길동"}
    checker.append(v)

    r = checker.check("홍길동")

    assert r == {}


def test_check_ten2seven():
    checker = TardyChecker()

    v = {"발생시각": "2022-08-05 10:00:00", "상태": "출근", "이름": "홍길동"}
    checker.append(v)
    v = {"발생시각": "2022-08-05 19:00:00", "상태": "퇴근", "이름": "홍길동"}
    checker.append(v)

    r = checker.check("홍길동")

    assert r == {}


def test_check_nine2six():
    checker = TardyChecker()

    v = {"발생시각": "2022-08-10 09:00:00", "상태": "출근", "이름": "홍길동"}
    checker.append(v)
    v = {"발생시각": "2022-08-10 18:00:00", "상태": "퇴근", "이름": "홍길동"}
    checker.append(v)

    r = checker.check("홍길동")

    assert r == {"2022-08-10": 60}


def test_check_start_tardy():
    checker = TardyChecker()

    v = {"발생시각": "2022-08-10 10:30:00", "상태": "출근", "이름": "홍길동"}
    checker.append(v)
    v = {"발생시각": "2022-08-10 19:00:00", "상태": "퇴근", "이름": "홍길동"}
    checker.append(v)

    r = checker.check("홍길동")

    assert r == {"2022-08-10": 30}


def test_check_end_tardy():
    checker = TardyChecker()

    v = {"발생시각": "2022-08-10 10:00:00", "상태": "출근", "이름": "홍길동"}
    checker.append(v)
    v = {"발생시각": "2022-08-10 18:40:00", "상태": "퇴근", "이름": "홍길동"}
    checker.append(v)

    r = checker.check("홍길동")

    assert r == {"2022-08-10": 20}
