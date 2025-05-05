from telegram import ReplyKeyboardMarkup
from constants import EMPTY_DESCRIPTION, ALL_DATES
from helpful_functions import sep_by_three

# Этот файл используется лишь для упрощения создания подсказок пользователю.


def get_markup(preset=1):
    """Эта функция возвращает markup, созданный по введённому пресету."""
    keyboard = [[]]
    match preset:
        case 1:
            keyboard = [['/delete_me', '/add_income'],
                        ['/checkout_alterations', '/add_consumption'],
                        ['/checkout_categories', '/help']]
        case 2:
            keyboard = [[EMPTY_DESCRIPTION]]
        case 3:
            keyboard = [['/start']]
        case 4:
            keyboard = [['/escape']]
        case 5:
            keyboard = [[ALL_DATES],
                        ['/escape']]
        case 6:
            keyboard = [['/delete', ALL_DATES],
                        ['/escape']]
        case 7:
            keyboard = [['/delete_categories'],
                        ['/escape']]
        case 8:
            keyboard = [['/delete_me', '/add_income'],
                        ['/checkout_alterations', '/add_consumption'],
                        ['/checkout_categories']]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)


