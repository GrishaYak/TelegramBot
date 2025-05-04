from telegram import ReplyKeyboardMarkup
from constants import EMPTY_DESCRIPTION, ALL_DATES
from usefull_functions import sep_by_three


def get_markup(preset=1):
    keyboard = [[]]
    match preset:
        case 1:
            keyboard = [['/delete_me', '/income'],
                        ['/checkout_alterations', '/consumption'],
                        ['/checkout_categories', '/help']]
        case 2:
            keyboard = [[EMPTY_DESCRIPTION]]
        case 3:
            keyboard = [['/start', '/help']]
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
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)


