from Errors import NotInList


def sep_by_three(arr: list) -> list:
    n = len(arr)
    res = []
    for i in range(0, n, 3):
        res.append(arr[i:i + 3])
    return res


def date_to_str(date):
    return f"{date.day:02}.{date.month:02}.{date.year:04}"


async def process_numbers(numbers, dicti, update):
    numbers = numbers.split(',')
    ids = []
    for el in numbers:
        if el.isdigit():
            try:
                if int(el) not in dicti:
                    raise NotInList
                ids.append(dicti[int(el)])
                continue
            except NotInList:
                await update.message.reply_text("Одного из номеров не было в списке!")
                return False, ids
        if len(el.split('-')) != 2:
            await update.message.reply_text("Неправильный формат!")
            return False, ids
        a, b = [int(i) for i in el.split('-')]
        try:
            ids += get_ids(list(range(a, b + 1)), dicti)
        except NotInList:
            await update.message.reply_text("Одного из номеров не было в списке!")
            return False, ids
    return True, ids


def get_ids(arr, dicti):
    res = []
    for el in arr:
        if el not in dicti:
            raise NotInList
        res.append(dicti[el])
    return res
