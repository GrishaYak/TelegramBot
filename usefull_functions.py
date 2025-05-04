def sep_by_three(arr: list) -> list:
    n = len(arr)
    res = []
    for i in range(0, n, 3):
        res.append(arr[i:i + 3])
    return res


def date_to_str(date):
    return f"{date.day:02}.{date.month:02}.{date.year:04}"
