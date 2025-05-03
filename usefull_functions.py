def sep_by_three(arr: list) -> list:
    n = len(arr)
    res = []
    for i in range(0, n, 3):
        res.append(arr[i:i + 3])
    return res
