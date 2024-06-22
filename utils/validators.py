import re


def is_correct_strtime(data: str):
    pattern = re.compile(
        r"[0-9]+d\s(0?[0-9]|1[0-9]|2[0-3])h\s(0?[0-9]|[1-5][0-9])m", re.IGNORECASE
    )
    return pattern.match(data)
