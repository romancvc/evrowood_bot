from django.core.management.base import BaseCommand
from django.conf import settings
from telegram.utils.request import Request
from django.db.models import Max
from telegram.ext import *
from telegram import *
import random
import datetime
import re
from .statics import *

from fewapp.models import *

ENTER_KEY, AUTHORIZATION, NEW_OUTLET, NAME_OUTLET, METRO, ADDRESS_OUTLET, NUMBER_POINT, STAND, POSS_STAND, PHOTO_STAND, ACTIVE_LED, STAND_COL, HANDOUT, MARK, COMPETITORS, ADD_COMPETITORS, CONTACTS_NAME, CONTACTS_PHONE, CONTACTS_EMAIL = range(19)

point_name = str()

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
        reply_text = f'Нажмите кнопку ниже, чтобы добавить новую торговую точку:'
        update.message.reply_text(
            text=reply_text,
            reply_markup=reply_new_point,
        )
        return NEW_OUTLET

    else:
        reply_text = f'Привет! Нажми кнопку ниже, чтобы авторизироваться'
        update.message.reply_text(
            text=reply_text,
            reply_markup=reply_authen,
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
    result = User.objects.values_list("key_auto", flat=True)

    if text in result:
        p = User.objects.filter(key_auto=text).update(
                        profile_id=Profile.objects.values_list('external_id', flat=True).get(external_id=chat_id),
                        user_id=chat_id
                 )

        reply_text = 'Авторизация прошла успешно. Нажмите кнопку ниже, чтобы добавить новую торговую точку'
        update.message.reply_text(
            text=reply_text,
            reply_markup=reply_new_point,
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
def exit_bot(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat_id

    reply_text = f'Вы вышли из диалога. Введите /start чтобы перезапустить бота.'
    update.message.reply_text(
        text=reply_text,
        reply_markup=reply_new_point,
    )
    return ConversationHandler.END


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

    reply_text = f'Введите полный адрес торговой точки:\n Например: Москва, ул. Остоженко, 60'
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
        reply_text = f'Есть ли возможность установки стенда для EVROWOOD на торговой точке?'
        update.message.reply_text(
            text=reply_text,
            reply_markup=reply_yes_no,
        )
        return POSS_STAND


def poss_stand(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat_id

    PointSales.objects.filter(point_name=point_name).update(poss_stand=text)

    if text == yes:
        reply_text = f'Есть ли возможность установки стенда-колонны?'
        update.message.reply_text(
            text=reply_text,
            reply_markup=reply_yes_no,
        )
        return STAND_COL

    elif text == no:
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

    reply_text = f'Есть ли возможность установки стенда-колонны?'
    update.message.reply_text(
        text=reply_text,
        reply_markup=reply_yes_no,
    )
    return STAND_COL


@log_errors
def stand_col(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat_id

    PointSales.objects.filter(point_name=point_name).update(stand_column=text)

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

    if not re.match(r"(^[+0-9]{1,3})*([0-9]{10,11}$)", text):
        reply_text = f'Неправильно набран номер. Попробуйте еще раз:'
        update.message.reply_text(
            text=reply_text,
        )
        return CONTACTS_PHONE
    else:
        PointSales.objects.filter(point_name=point_name).update(contacts_point_phone=text)

        reply_text = f'Укажите электронную почту. Если ее нет - нажмите кнопку:'
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
            reply_markup=ReplyKeyboardRemove(),
        )
        reply_text2 = f'Введите /start чтобы вернуться в начало'
        update.message.reply_text(
            text=reply_text2,
        )
        return ConversationHandler.END
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", text):
        reply_text = f'Вы точно ввели электронный адрес? Попробуйте еще раз'
        update.message.reply_text(
            text=reply_text,
        )
        return CONTACTS_EMAIL
    else:
        PointSales.objects.filter(point_name=point_name).update(contacts_point_email=text)
        reply_text = f'Спасибо!\nПлюсик в твою копилочку😉'
        update.message.reply_animation(
            r'https://avatars.mds.yandex.net/get-zen_doc/941737/pub_5e9da02fa0e2262e8eeafc26_5e9da0eadd625f3a39c00a47/orig'
        )
        update.message.reply_text(
            text=reply_text,
            reply_markup=ReplyKeyboardRemove(),
        )
        reply_text2 = f'Введите /start чтобы вернуться в начало'
        update.message.reply_text(
            text=reply_text2,
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
                    MessageHandler(Filters.all & (~ Filters.command), enter_key, pass_user_data=True)
                ],
                AUTHORIZATION: [
                    MessageHandler(Filters.all & (~ Filters.command), authorization, pass_user_data=True)
                ],
                NEW_OUTLET: [
                    MessageHandler(Filters.all & (~ Filters.command), new_outlet, pass_user_data=True)
                ],
                NAME_OUTLET: [
                    MessageHandler(Filters.all & (~ Filters.command), name_outlet, pass_user_data=True)
                ],
                METRO: [
                    MessageHandler(Filters.all & (~ Filters.command), metro, pass_user_data=True)
                ],
                ADDRESS_OUTLET: [
                    MessageHandler(Filters.all & (~ Filters.command), address_outlet, pass_user_data=True)
                ],
                NUMBER_POINT: [
                    MessageHandler(Filters.all & (~ Filters.command), number_point, pass_user_data=True)
                ],
                STAND: [
                    MessageHandler(Filters.all & (~ Filters.command), stand, pass_user_data=True)
                ],
                POSS_STAND: [
                        MessageHandler(Filters.all & (~ Filters.command), poss_stand, pass_user_data=True)
                ],
                PHOTO_STAND: [
                    MessageHandler(Filters.all & (~ Filters.command), photo_stand, pass_user_data=True)
                ],
                ACTIVE_LED: [
                    MessageHandler(Filters.all & (~ Filters.command), active_led, pass_user_data=True)
                ],
                STAND_COL: [
                    MessageHandler(Filters.all & (~ Filters.command), stand_col, pass_user_data=True)
                ],
                HANDOUT: [
                    MessageHandler(Filters.all & (~ Filters.command), handout, pass_user_data=True)
                ],
                MARK: [
                    MessageHandler(Filters.all & (~ Filters.command), mark, pass_user_data=True)
                ],
                ADD_COMPETITORS: [
                    MessageHandler(Filters.all & (~ Filters.command), add_competitors, pass_user_data=True)
                ],
                COMPETITORS: [
                    MessageHandler(Filters.all & (~ Filters.command), competitors, pass_user_data=True)
                ],
                CONTACTS_NAME: [
                    MessageHandler(Filters.all & (~ Filters.command), contacts_name, pass_user_data=True)
                ],
                CONTACTS_PHONE: [
                    MessageHandler(Filters.all & (~ Filters.command), contacts_phone, pass_user_data=True)
                ],
                CONTACTS_EMAIL: [
                    MessageHandler(Filters.all & (~ Filters.command), contacts_email, pass_user_data=True)
                ],
            },
            fallbacks=[
                CommandHandler("exit", exit_bot)
            ],
        )
        updater.dispatcher.add_handler(conv_handler)
        updater.dispatcher.add_handler(CommandHandler('exit', exit_bot))

        updater.start_polling()
        updater.idle()

    if __name__ == '__main__':
        handle()