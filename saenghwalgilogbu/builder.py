text_map = {"지각": "출근", "조퇴": "퇴근"}


def build_csv(name: str, r: dict):
    sheet = ""
    for k, v in r.items():
        print(f"{k}일 {v}")

        m, text = v

        if "부족" in text:
            sheet += f"{name},{k},,{text}\n"
        else:
            sheet += f"{name},{k},{text_map[text]},{m}분 {text}\n"

    return sheet.rstrip("\n")
