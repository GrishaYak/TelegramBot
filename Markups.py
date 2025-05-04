from telegram import ReplyKeyboardMarkup
from constants import MT_DISCRIPTION, ALL_TIME
from usefull_functions import sep_by_three


def get_markup(preset=1):
    keyboard = [[]]
    match preset:
        case 1:
            keyboard = [['/delete_me', '/income'], ['/checkout', '/consumption'], ['/help']]
        case 2:
            keyboard = [[MT_DISCRIPTION]]
        case 3:
            keyboard = [['/start', '/help']]
        case 4:
            keyboard = [['/escape']]
        case 5:
            keyboard = [[ALL_TIME], ['/escape']]
        case 6:
            keyboard = [['/delete', ALL_TIME], ['/escape']]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)


