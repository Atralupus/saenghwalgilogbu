text_map = {"지각": "출근", "조퇴": "퇴근"}


def build_csv(name: str, r: dict):
    sheet = ""
    for k, v in r.items():
        print(f"{k} {v}")

        m, text, stat = v

        if "부족" in text:
            sheet += f"{name},{k},,{text}\n"
        elif "지각" in stat or '조퇴' in stat:
            sheet += f"{name},{k},{text},{m}분 {stat}\n"
        else:
            sheet += f"{name},{k},{text},\n"

    return sheet.rstrip("\n")
