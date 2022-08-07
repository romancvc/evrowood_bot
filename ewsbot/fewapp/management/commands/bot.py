from django.core.management.base import BaseCommand
from django.conf import settings
from telegram.utils.request import Request
from django.db.models import Max
from telegram.ext import *
from telegram import *
import random
import datetime
import re

from fewapp.models import *


ENTER_KEY, AUTHORIZATION, NEW_OUTLET, NAME_OUTLET, METRO, ADDRESS_OUTLET, NUMBER_POINT, STAND, PHOTO_STAND, ACTIVE_LED, STAND_COL, HANDOUT, MARK, COMPETITORS, ADD_COMPETITORS, CONTACTS_NAME, CONTACTS_PHONE, CONTACTS_EMAIL = range(18)


authen = 'Начать авторизацию'
new_point = 'Добавить новую точку'
dont_market = 'Это магазин, а не рынок'
yes = 'Да'
no = 'Нет'
thereis_stand = 'Есть стенд'
thereisno_stand = 'Нет стенда'
add_competitor = 'Добавить конкурента'
no_competitor = 'Продают только нас'
exit_competitor = 'Больше конкурентов нет'
dont_email = 'Нет эл. почты'

point_name = str()

CALLBACK_BUTTON1_YES = "callbak_button1_yes"
CALLBACK_BUTTON1_NO = "callbak_button1_no"

TITLE = {
    CALLBACK_BUTTON1_YES: "Да",
    CALLBACK_BUTTON1_NO: "Нет"
}

reply_yes_no = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=yes),
            KeyboardButton(text=no),
        ],
    ],
    resize_keyboard=True,
)

reply_stand = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=thereis_stand),
            KeyboardButton(text=thereisno_stand),
        ],
    ],
    resize_keyboard=True,
)

reply_dont_market = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=dont_market),
        ],
    ],
    resize_keyboard=True,
)

reply_dont_email = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=dont_email),
        ],
    ],
    resize_keyboard=True,
)

reply_marks = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='1'),
            KeyboardButton(text='2'),
            KeyboardButton(text='3'),
            KeyboardButton(text='4'),
            KeyboardButton(text='5'),
        ],
        [
            KeyboardButton(text='6'),
            KeyboardButton(text='7'),
            KeyboardButton(text='8'),
            KeyboardButton(text='9'),
            KeyboardButton(text='10'),
        ],
    ],
    resize_keyboard=True,
)

reply_competitor_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=no_competitor),
        ],
    ],
    resize_keyboard=True,
)

reply_competitor_in = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=add_competitor),
            KeyboardButton(text=exit_competitor),
        ],
    ],
    resize_keyboard=True,
)

compretitors_list = []


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            print(error_message)
            raise e

    return inner




@log_errors
def start_handler(update: Update, context: CallbackContext):
    """ Начало взаимодействия """
    text = update.message.text
    chat_id = update.message.chat_id
    now_user = str(User.objects.values_list('user_id', flat=True))

    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'nickname': update.message.from_user.username
        }
    )

    if str(chat_id) in now_user:

        reply_markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=new_point)
                ],
            ],
            resize_keyboard=True,
        )

        reply_text = f'С возвращением! Чем сегодня займемся?'
        update.message.reply_text(
            text=reply_text,
            reply_markup=reply_markup,
        )
        return NEW_OUTLET

    else:
        reply_markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=authen)
                ],
            ],
            resize_keyboard=True,
        )

        reply_text = f'Привет! Нажми кнопку ниже, чтобы авторизироваться'
        update.message.reply_text(
            text=reply_text,
            reply_markup=reply_markup,
        )
        return ENTER_KEY


@log_errors
def enter_key(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat_id
    #User.objects.update(user_id=chat_id)

    if text == authen:
        reply_text = 'Введите полученный ключ авторизции'
        update.message.reply_text(
            text=reply_text,
            reply_markup=ReplyKeyboardRemove(),
        )
    return AUTHORIZATION


@log_errors
def authorization(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat_id
    result = User.objects.values_list("key_auto", flat=True).filter(user_id=0)

    if text in result:
        p = User.objects.filter(key_auto=text).update(
                        profile_id=Profile.objects.values_list('external_id', flat=True).get(external_id=chat_id),
                        user_id=chat_id
                 )

        reply_murkup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=new_point)
                ],
            ],
            resize_keyboard=True,
        )

        reply_text = 'Авторизация прошла успешно. Нажмите кнопку ниже, чтобы добавить новую торговую точку'
        update.message.reply_text(
            text=reply_text,
            reply_markup=reply_murkup,
        )
        return NEW_OUTLET

    elif text != result:
        reply_text = 'Вы ввели неверный ключ или такого менеджера не существует!'
        update.message.reply_text(
            text=reply_text,
            reply_markup=ReplyKeyboardRemove(),
        )
        return AUTHORIZATION


@log_errors
def new_outlet(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat_id

    reply_text = f'Введите название контрагента:'
    update.message.reply_text(
        text=reply_text,
        reply_markup=ReplyKeyboardRemove(),
    )
    return NAME_OUTLET



@log_errors
def name_outlet(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat_id

    global point_name
    point_name = text

    PointSales.objects.create(point_name=text)

    reply_text = f'Введите ближайшую к торговой точке станцию метро:'
    update.message.reply_text(
        text=reply_text,
    )
    return METRO


@log_errors
def metro(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat_id

    PointSales.objects.filter(point_name=point_name).update(metro=text)

    reply_text = f'Введите полный адрес торговой точки:\n Например: 874653, Москва, ул. Остоженко, 60'
    update.message.reply_text(
        text=reply_text,
    )
    return ADDRESS_OUTLET


@log_errors
def address_outlet(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat_id

    PointSales.objects.filter(point_name=point_name).update(point_address=text)

    reply_text = f'Введите номер точки на рынке:'
    update.message.reply_text(
        text=reply_text,
        reply_markup=reply_dont_market,
    )
    return NUMBER_POINT


@log_errors
def number_point(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat_id

    if text == dont_market:
        reply_text = f'Есть ли стенд EVROWOOD на торговой точке?'
        update.message.reply_text(
            text=reply_text,
            reply_markup=reply_stand,
        )
        return STAND
    else:
        PointSales.objects.filter(point_name=point_name).update(point_number=text)

        reply_text = f'Есть ли стенд EVROWOOD на торговой точке?'
        update.message.reply_text(
            text=reply_text,
            reply_markup=reply_stand,
        )
        return STAND


@log_errors
def stand(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat_id

    if text == thereis_stand:
        reply_text = f'Пришлите фотографию стенда EVROWOOD:'
        update.message.reply_text(
            text=reply_text,
            reply_markup=ReplyKeyboardRemove(),
        )
        return PHOTO_STAND
    elif text == thereisno_stand:
        reply_text = f'Оцените точку от 1 до 10:'
        update.message.reply_text(
            text=reply_text,
            reply_markup=reply_marks,
        )
        return MARK


@log_errors
def photo_stand(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat_id

    img_id = context.bot.get_file(update.message.photo[-1].file_id)
    img_id.download(f'images/{img_id["file_unique_id"]}.jpg')
    PointSales.objects.filter(point_name=point_name).update(point_photo=img_id["file_unique_id"])

    reply_text = f'Горит ли LED плинтус на стенде EVROWOOD?'
    update.message.reply_text(
        text=reply_text,
        reply_markup=reply_yes_no
    )
    return ACTIVE_LED


@log_errors
def active_led(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat_id

    PointSales.objects.filter(point_name=point_name).update(active_led=text)

    reply_text = f'Есть ли возможность установки стенда-колонны?'
    update.message.reply_text(
        text=reply_text,
        reply_markup=reply_yes_no,
    )
    return STAND_COL


@log_errors
def ctand_col(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat_id

    PointSales.objects.filter(point_name=point_name).update(stand_column=text)

    reply_text = f'Есть ли раздаточный материал на торговой точке?'
    update.message.reply_text(
        text=reply_text,
        reply_markup=reply_yes_no,
    )
    return HANDOUT


@log_errors
def handout(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat_id

    PointSales.objects.filter(point_name=point_name).update(handout=text)

    reply_text = f'Оцените точку от 1 до 10:'
    update.message.reply_text(
        text=reply_text,
        reply_markup=reply_marks,
    )
    return MARK


@log_errors
def mark(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat_id

    PointSales.objects.filter(point_name=point_name).update(mark_point=text)

    reply_text = f'Укажите конкурента, который продаёт на точке МДФ плинтус'
    update.message.reply_text(
        text=reply_text,
        reply_markup=reply_competitor_start,
    )
    return ADD_COMPETITORS


@log_errors
def add_competitors(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat_id

    if text == no_competitor:
        reply_text = f'Оставьте контакты владельца или менеджера торговой точки. Напишите ФИО:'
        update.message.reply_text(
            text=reply_text,
            reply_markup=ReplyKeyboardRemove(),
        )
        return CONTACTS_NAME
    else:
        compretitors_list.append(text)

        reply_text = f'Нажмите "Добавить" если есть еще конкурент:'
        update.message.reply_text(
            text=reply_text,
            reply_markup=reply_competitor_in,
        )

        return COMPETITORS


@log_errors
def competitors(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat_id

    if text == add_competitor:
        reply_text = f'Укажите конкурента, который продаёт на точке МДФ плинтус'
        update.message.reply_text(
            text=reply_text,
        )
        return ADD_COMPETITORS
    else:
        PointSales.objects.filter(point_name=point_name).update(competitor=str(compretitors_list))

        reply_text = f'Оставьте контакты владельца или менеджера торговой точки. Напишите ФИО:'
        update.message.reply_text(
            text=reply_text,
            reply_markup=ReplyKeyboardRemove(),
        )
        return CONTACTS_NAME


@log_errors
def contacts_name(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat_id

    PointSales.objects.filter(point_name=point_name).update(contacts_point_name=text)

    reply_text = f'Напишите номер телефона:'
    update.message.reply_text(
        text=reply_text,
    )
    return CONTACTS_PHONE


@log_errors
def contacts_phone(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat_id

    PointSales.objects.filter(point_name=point_name).update(contacts_point_phone=text)

    reply_text = f'Укажите элекстронную почту. Если ее нет - нажмите кнопку:'
    update.message.reply_text(
        text=reply_text,
        reply_markup=reply_dont_email
    )
    return CONTACTS_EMAIL


@log_errors
def contacts_email(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat_id

    if text == dont_email:
        reply_text = f'Спасибо!\nПлюсик в твою копилочку😉'
        update.message.reply_animation(
            r'https://avatars.mds.yandex.net/get-zen_doc/941737/pub_5e9da02fa0e2262e8eeafc26_5e9da0eadd625f3a39c00a47/orig'
        )
        update.message.reply_text(
            text=reply_text,
        )
        return ConversationHandler.END
    else:
        PointSales.objects.filter(point_name=point_name).update(contacts_point_email=text)
        reply_text = f'Спасибо!\nПлюсик в твою копилочку😉'
        update.message.reply_animation(
            r'https://avatars.mds.yandex.net/get-zen_doc/941737/pub_5e9da02fa0e2262e8eeafc26_5e9da0eadd625f3a39c00a47/orig'
        )
        update.message.reply_text(
            text=reply_text,
        )
        return ConversationHandler.END



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
                    MessageHandler(Filters.all, photo_stand, pass_user_data=True)
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
                ADD_COMPETITORS: [
                    MessageHandler(Filters.all, add_competitors, pass_user_data=True)
                ],
                COMPETITORS: [
                    MessageHandler(Filters.all, competitors, pass_user_data=True)
                ],
                CONTACTS_NAME: [
                    MessageHandler(Filters.all, contacts_name, pass_user_data=True)
                ],
                CONTACTS_PHONE: [
                    MessageHandler(Filters.all, contacts_phone, pass_user_data=True)
                ],
                CONTACTS_EMAIL: [
                    MessageHandler(Filters.all, contacts_email, pass_user_data=True)
                ],
            },
            fallbacks=[],
        )
        updater.dispatcher.add_handler(conv_handler)

        updater.start_polling()
        updater.idle()

    if __name__ == '__main__':
        handle()