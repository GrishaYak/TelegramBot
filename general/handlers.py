from alterations.delete_alterations import delete_alteration, delete_alteration2
from alterations.checkout_alteration import checkout_alteration_question, checkout_alteration
from delete_user import delete_user_question, delete_user
from categories.checkout_categories import checkout_categories
from categories.delete_categories import delete_categories_which, delete_categories
from telegram.ext import CommandHandler, MessageHandler, filters
from alterations.add_alteration import (add_alteration_sum, add_alteration_category, add_alteration_description,
                                        add_income, add_consumption)
from general_commands import start, help_command, escape

# В этом файле инициализируются все handler'ы. Это самая некрасивая часть моего проекта C:

start_handler = CommandHandler("start", start)
help_handler = CommandHandler("help", help_command)
escape_handler = CommandHandler("escape", escape)

checkout_alteration_handler = CommandHandler("checkout_alterations", checkout_alteration_question)
checkout_alteration_handler2 = MessageHandler(filters.TEXT & ~filters.COMMAND, checkout_alteration)

delete_user_are_you_shure_handler = CommandHandler("delete_me", delete_user_question)
delete_user_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, delete_user)

add_consumption_handler = CommandHandler("add_consumption", add_consumption)
add_income_handler = CommandHandler("add_income", add_income)

add_alteration_sum_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, add_alteration_sum)
add_alteration_category_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, add_alteration_category)
add_alteration_description_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, add_alteration_description)

delete_alterations_which_handler = CommandHandler("delete", delete_alteration)
delete_alterations_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, delete_alteration2)

checkout_categories_handler = CommandHandler('checkout_categories', checkout_categories)

delete_categories_which_handler = CommandHandler('delete_categories', delete_categories_which)
delete_categories_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, delete_categories)