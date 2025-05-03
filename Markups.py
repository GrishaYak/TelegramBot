from telegram import ReplyKeyboardMarkup


def get_markup(preset=1):
    match preset:
        case 1:
            keyboard = [['/consumption', '/income'], ['/checkout', '/delete_me']]
            return ReplyKeyboardMarkup(keyboard)
