from telegram import ReplyKeyboardMarkup


def get_markup(preset=1):
    match preset:
        case 1:
            keyboard = [['/set', '/help', '/unset']]
            return ReplyKeyboardMarkup(keyboard)
