
# Этот файл хранит в себе различные полезные функции, которые можно использовать в нескольких ситуация.


def sep_by_three(arr: list) -> list:
    """Разбивает одномерный массив на группы по три или меньше элементов и делает из них двумерный массив."""
    n = len(arr)
    res = []
    for i in range(0, n, 3):
        res.append(arr[i:i + 3])
    return res


def date_to_str(date):
    """Преобразует объект класса datetime.date в строку формата DD.MM.YYYY"""
    return f"{date.day:02}.{date.month:02}.{date.year:04}"


async def process_numbers(numbers: str, dicti: dict, update):
    """Получает строку numbers в формате '1,2,4-6', преобразует её в массив чисел [1,2,4,5,6] посредством функции
    str_to_numbers, а потом вместо каждого элемента записывает значение, которое получается если использовать элемент
    как ключ словаря dicti.
    Возвращает False и неполный массив в качестве ответа, елси данные были даны в некоректном формате, при этом
    выводит сообщение об ошибке пользователю.
    Иначе она возвращает True и ответ"""
    numbers = numbers.split(',')
    ok, numbers = await str_to_numbers(numbers, update)
    if not ok:
        return False, []
    res = []
    for el in numbers:
        if el not in dicti:
            await update.message.reply_text("Одной из цифр не было в списке.")
            return False, res
        res.append(dicti[el])
    return True, res


async def str_to_numbers(line, update):
    """Преобразует строку формата '1,2,4-7' в массив чисел [1,2,4,5,6,7]
    В качестве ответа возвращает True, если отработала корректно, а вместе с ним правильный ответ.
    Иначе возвращает False и неправильный ответ, при этом выводит сообщение об ошибке пользователю."""
    line = line.split(',')
    numbers = []
    for el in line:
        if el.isdigit():
            numbers.append(int(el))
            continue
        if len(el.split('-')) != 2:
            await update.message.reply_text("Неправильный формат!")
            return False, numbers
        try:
            a, b = [int(i) for i in el.split('-')]
        except TypeError:
            await update.message.reply_text("Неправильный формат!")
            return False, numbers
        numbers += list(range(a, b + 1))
    return True, numbers
