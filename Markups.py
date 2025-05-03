from telegram import ReplyKeyboardMarkup
from constants import MT_DISCRIPTION


def get_markup(preset=1):
    keyboard = [[]]
    match preset:
        case 1:
            keyboard = [['/consumption', '/income'], ['/checkout', '/delete_me']]
        case 2:
            keyboard = [[MT_DISCRIPTION]]
        case 3:
            keyboard = [['/start', '/help']]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)


