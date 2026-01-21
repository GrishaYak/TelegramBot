import logging
from telegram.ext import Application, ConversationHandler
import os
from dotenv import load_dotenv
import asyncio
from handlers import *


def main():
    """Это главная функция, она включает бота и добавляет ему обработчики сообщений, взятые из файла handlers"""
    application = Application.builder().token(os.getenv('BOT_TOKEN')).build()
    # Выше я взял токен бота из окружения, которое загрузил ранее
    start_conv = ConversationHandler(
        entry_points=[start_handler],
        states={
            1: [add_consumption_handler, add_income_handler, checkout_alteration_handler,
                delete_user_are_you_sure_handler, checkout_categories_handler],
            'add_alteration_sum': [add_alteration_sum_handler],
            'add_alteration_category': [add_alteration_category_handler],
            'add_alteration_description': [add_alteration_description_handler],
            'checkout_alteration': [checkout_alteration_handler2],
            'checkout_alteration_done': [checkout_alteration_handler2, delete_alterations_which_handler],
            'delete_alteration': [delete_alterations_handler],
            'delete_user': [delete_user_handler],
            'delete_categories_which': [delete_categories_which_handler],
            'delete_categories': [delete_categories_handler]
        },
        fallbacks=[escape_handler]
    )

    application.add_handler(help_handler)
    application.add_handler(start_conv)
    application.run_polling()


if __name__ == '__main__':
    load_dotenv()  # Загружаем окружение.
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()
