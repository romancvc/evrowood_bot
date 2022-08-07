from django.core.management.base import BaseCommand
from django.conf import settings
from telegram.utils.request import Request
from django.db.models import Max
from telegram.ext import *
from telegram import *
import random
import datetime
import bot

authentification = 'Начать аутентификацию'

ENTER_KEY, AUTHORIZATION, NEW_OUTLET, NAME_OUTLET, METRO, ADDRESS_OUTLET, NUMBER_POINT, STAND, PHOTO_STAND, ACTIVE_LED, STAND_COL, HANDOUT, MARK, COMPETITORS, CONTACTS = range(16)

class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN
        )

        updater = Updater(
            bot=bot,
            use_context=True,
        )

        conv_handler = ConversationHandler(
            entry_points=[
                CommandHandler("start", start_handler)
            ],
            states={
                ENTER_KEY: [
                    MessageHandler(Filters.all, enter_key, pass_user_data=True)
                ],
                AUTHORIZATION: [
                    MessageHandler(Filters.all, authorization, pass_user_data=True)
                ],
                NEW_OUTLET: [
                    MessageHandler(Filters.all, new_outlet, pass_user_data=True)
                ],
                NAME_OUTLET: [
                    MessageHandler(Filters.all, name_outlet, pass_user_data=True)
                ],
                METRO: [
                    MessageHandler(Filters.all, metro, pass_user_data=True)
                ],
                ADDRESS_OUTLET: [
                    MessageHandler(Filters.all, address_outlet, pass_user_data=True)
                ],
                NUMBER_POINT: [
                    MessageHandler(Filters.all, number_point, pass_user_data=True)
                ],
                STAND: [
                    MessageHandler(Filters.all, stand, pass_user_data=True)
                ],
                PHOTO_STAND: [
                    MessageHandler(Filters.photo, photo_stand, pass_user_data=True)
                ],
                ACTIVE_LED: [
                    MessageHandler(Filters.all, active_led, pass_user_data=True)
                ],
                STAND_COL: [
                    MessageHandler(Filters.all, ctand_col, pass_user_data=True)
                ],
                HANDOUT: [
                    MessageHandler(Filters.all, handout, pass_user_data=True)
                ],
                MARK: [
                    MessageHandler(Filters.all, mark, pass_user_data=True)
                ],
                COMPETITORS: [
                    MessageHandler(Filters.all, competitors, pass_user_data=True)
                ],
                CONTACTS: [
                    MessageHandler(Filters.all, contacts, pass_user_data=True)
                ]
            },
            fallbacks=[],
        )
        updater.dispatcher.add_handler(conv_handler)

        updater.start_polling()
        updater.idle()
