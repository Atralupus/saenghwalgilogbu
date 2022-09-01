from saenghwalgilogbu.builder import build_csv


def test_build_csv():
    data = {
        "2022-08-01 14:47:39": (10, "지각"),
        "2022-08-02 14:47:39": (10, "지각"),
    }
    r = build_csv("test", data)

    assert (
        r
        == "test,2022-08-01 14:47:39,출근,10분 지각\ntest,2022-08-02 14:47:39,출근,10분 지각"
    )


def test_build_csv_minus():
    data = {
        "2022-08-01 17:47:39": (10, "출근 기록 부족"),
        "2022-08-02 10:47:39": (10, "퇴근 기록 부족"),
    }
    r = build_csv("test", data)

    assert (
        r
        == "test,2022-08-01 17:47:39,,출근 기록 부족\ntest,2022-08-02 10:47:39,,퇴근 기록 부족"
    )
