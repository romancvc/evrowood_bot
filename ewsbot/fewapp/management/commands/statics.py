from telegram import ReplyKeyboardMarkup, KeyboardButton

authen = 'Начать авторизацию'
new_point = 'Добавить новую точку'
dont_market = 'Это магазин, а не рынок'
yes = 'Да'
no = 'Нет'
thereis_stand = 'Есть стенд'
thereisno_stand = 'Нет стенда'
add_competitor = 'Добавить конкурента'
no_competitor = 'Нет конкурентов'
exit_competitor = 'Больше конкурентов нет'
dont_email = 'Нет эл. почты'


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

reply_new_point = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=new_point)
                ],
            ],
            resize_keyboard=True,
        )

reply_authen = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=authen)
                ],
            ],
            resize_keyboard=True,
        )