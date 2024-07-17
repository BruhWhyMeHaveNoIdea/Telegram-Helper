from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice


to_main_menu_buttons = [
    [
        InlineKeyboardButton(text="В меню!", callback_data="to_mmenu")
    ]
]
to_main_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=to_main_menu_buttons)

marketer_question_buttons = [
    [
        InlineKeyboardButton(text="Да", callback_data="follow"),
        InlineKeyboardButton(text="Нет", callback_data="complete_questions")
    ]]

marketer_question_keyboards = InlineKeyboardMarkup(inline_keyboard=marketer_question_buttons)

main_menu_buttons = [
    [
        InlineKeyboardButton(text="Бизнес помощник", callback_data="business_assistant"),
        InlineKeyboardButton(text="Канал с уроками", callback_data="channel_with_lessons")
    ],
    [
        InlineKeyboardButton(text="Чат нетворкинга", callback_data="networking_chat"),
        InlineKeyboardButton(text="Настройки", callback_data="settings")
    ],
    [
        InlineKeyboardButton(text="Помощь и инструкции", callback_data="help_and_instructions"),
        InlineKeyboardButton(text="Техническая поддержка", callback_data="technical_support")
    ],
    [
        InlineKeyboardButton(text="Сообщение", callback_data="first"),
        InlineKeyboardButton(text="➡️ Следующая страница ➡️", callback_data="main_menu_secound")
    ]
]

main_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=main_menu_buttons)

main_menu_secound_buttons = [
    [
        InlineKeyboardButton(text="Сообщение 2", callback_data="first"),
        InlineKeyboardButton(text="Сообщение 3", callback_data="first")
    ],
    [
        InlineKeyboardButton(text="Сообщение 4", callback_data="referal_and_donation"),
        InlineKeyboardButton(text="Сообщение 6", callback_data="first"),
    ],
    [
        InlineKeyboardButton(text="⬅️ Предыдущая страница ⬅️", callback_data="to_mmenu"),
        InlineKeyboardButton(text="Сообщение 7", callback_data="first")
    ]
]

main_menu_secound_keyboard = InlineKeyboardMarkup(inline_keyboard=main_menu_secound_buttons)

refer_donat_buttons = [
    [
        InlineKeyboardButton(text="Подписка", callback_data="donation"),
        InlineKeyboardButton(text="Реферальная программа", callback_data="referal_system")
    ]
]

refer_donat_kb = InlineKeyboardMarkup(inline_keyboard=refer_donat_buttons)

business_buttons = [
    [
        InlineKeyboardButton(text="Твой маркетолог", callback_data="your_marketer"),
    ],
    [
        InlineKeyboardButton(text="Помощь с продажами", callback_data="sales_assistance"),
    ],
    [
        InlineKeyboardButton(text="Найти клиентов / сотрудников", callback_data="found_people"),
    ],
    [
        InlineKeyboardButton(text="Назад", callback_data="to_mmenu")
    ]
]

business_keyboard = InlineKeyboardMarkup(inline_keyboard=business_buttons)

your_marketer_buttons = [
    [
        InlineKeyboardButton(text="Продумать маркетинг", callback_data="think_about_marketing")
    ],
    [
        InlineKeyboardButton(text="Создать пост", callback_data="create_post")
    ],
    [
        InlineKeyboardButton(text="Создать контент-план (сторис и посты)", callback_data="create_content_plan")
    ],
    [
        InlineKeyboardButton(text="Создать shorts", callback_data="create_shorts")
    ],
    [
        InlineKeyboardButton(text="Создать видео", callback_data="create_video")
    ],
    [
        InlineKeyboardButton(text="Создать лид-магнит", callback_data="create_lead_magnet")
    ],
    [
        InlineKeyboardButton(text="Создать воронку", callback_data="create_lead_magnet")
    ],
    [
        InlineKeyboardButton(text="Назад", callback_data="to_mmenu")
    ]
]

your_marketer_keyboard = InlineKeyboardMarkup(inline_keyboard=your_marketer_buttons)

continue_buttons = [
    [
        InlineKeyboardButton(text="Продолжить", callback_data="follow"),
        InlineKeyboardButton(text="Заного", callback_data="your_marketer")
        ]
    ]
continue_keyboard = InlineKeyboardMarkup(inline_keyboard=continue_buttons)

to_function_buttons = [
    [
    InlineKeyboardButton(text="Вперёд!", callback_data="funcs_menu")
]
]

to_function_menu = InlineKeyboardMarkup(inline_keyboard=to_function_buttons)

first = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Составить оффер', callback_data='offer')],
        [InlineKeyboardButton(text='Ответить клиенту', callback_data='send_to_client')],
        [InlineKeyboardButton(text='Сообщение 19', callback_data='sms19')],
        [InlineKeyboardButton(text='Сообщение 20', callback_data='sms20')]
                     ]
)

sms_19 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Сообщение 19', callback_data='sms19')]
    ]
)

sms_20 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Сообщение 20', callback_data='sms20')]
    ]
)


restart_buttons_mark = [
    [
        InlineKeyboardButton(text="Начать заного", callback_data="restart_questions_mark"),
        InlineKeyboardButton(text="Оставить прежние", callback_data="continue_questions_mark")
    ]
]

restart_keyboard_mark = InlineKeyboardMarkup(inline_keyboard=restart_buttons_mark)

restart_buttons_post = [
    [
        InlineKeyboardButton(text="Начать заного", callback_data="restart_questions_post"),
        InlineKeyboardButton(text="Оставить прежние", callback_data="continue_questions_post")
    ]
]

restart_keyboard_post = InlineKeyboardMarkup(inline_keyboard=restart_buttons_post)

restart_buttons_content = [
    [
        InlineKeyboardButton(text="Начать заного", callback_data="restart_questions_content"),
        InlineKeyboardButton(text="Оставить прежние", callback_data="continue_questions_content")
    ]
]

restart_keyboard_content = InlineKeyboardMarkup(inline_keyboard=restart_buttons_content)

restart_buttons_magnet = [
    [
        InlineKeyboardButton(text="Начать заного", callback_data="restart_questions_magnet"),
        InlineKeyboardButton(text="Оставить прежние", callback_data="continue_questions_magnet")
    ]
]

restart_keyboard_magnet = InlineKeyboardMarkup(inline_keyboard=restart_buttons_magnet)

to_fmenu_from_choices = [
    [
        InlineKeyboardButton(text="Назад", callback_data="funcs_menu")
    ]
]

to_fmenu_from_choices_kb = InlineKeyboardMarkup(inline_keyboard=to_fmenu_from_choices)


continue_mark = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Вперед!", callback_data="mark_results")]])
continue_post = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Вперед!", callback_data="post_results")]])
continue_content = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Вперед!", callback_data="content_results")]])
continue_shorts = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Вперед!", callback_data="shorts_results")]])
continue_video = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Вперед!", callback_data="video_results")]])
continue_magnet = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Вперед!", callback_data="magnet_results")]])

content_days_button = [
    [
        InlineKeyboardButton(text="1 день", callback_data="one_content_day")
    ],
    [
        InlineKeyboardButton(text="3 дня", callback_data="three_content_day")
    ],
    [
        InlineKeyboardButton(text="7 дней", callback_data="seven_content_day")
    ]
]

content_days = InlineKeyboardMarkup(inline_keyboard=content_days_button)

self_post_buttons = [
    [
        InlineKeyboardButton(text="Да, сделай все сама", callback_data="gpt_work"),
        InlineKeyboardButton(text="Нет, я напишу сам")
    ]
]


subscribtion_buy_buttons = [
    [
        InlineKeyboardButton(text='Подписка "Весь функционал" за 3.490₽', callback_data="common_buy")
    ],
    [
        InlineKeyboardButton(text='Подписка "Весь функционал + Доступ к ...', callback_data="exclusive_buy")
    ]
]

subscribtion_buy_keyboard =InlineKeyboardMarkup(inline_keyboard=subscribtion_buy_buttons)


post_buttons = [
    [
        InlineKeyboardButton(text='Сам', callback_data="post_by_user"),
        InlineKeyboardButton(text='По формам', callback_data="post_by_bot")
    ]
]
post_choose=InlineKeyboardMarkup(inline_keyboard=post_buttons)


face_buttons = [
    [
        InlineKeyboardButton(text="От 'Я'", callback_data="from_me"),
        InlineKeyboardButton(text="От 'Мы'", callback_data="from us")
    ]
]

face_keyboard = InlineKeyboardMarkup(inline_keyboard=face_buttons)

tone_buttons = [
    [InlineKeyboardButton(text="Дружелюбный", callback_data="friendly_tone")],
    [InlineKeyboardButton(text="Классический",callback_data="classic_tone")],
    [InlineKeyboardButton(text="Строгий",callback_data="serious_tone")]
]
tone_keyboard = InlineKeyboardMarkup(inline_keyboard=tone_buttons)

chara_buttons = [
    [
        InlineKeyboardButton(text="Рекламный", callback_data="advert"),
        InlineKeyboardButton(text="Информационный", callback_data="information")
    ],
    [
        InlineKeyboardButton(text="Продающий",callback_data="selling"),
        InlineKeyboardButton(text="Развлекательный",callback_data="fun")
    ]
]
chara_keyboard = InlineKeyboardMarkup(inline_keyboard=chara_buttons)


video_len_button = [[
    InlineKeyboardButton(text="Короткое (5-10 минут)", callback_data="short_video")
],
    [
        InlineKeyboardButton(text="Среднее (15-20 минут)", callback_data="average_video")
    ],
    [
        InlineKeyboardButton(text="Длинное (25-30 минут)", callback_data="long_video")
    ]
]

forward_buttons = [[InlineKeyboardButton(text="Вперёд", callback_data="forward_video")]]
forward_video = InlineKeyboardMarkup(inline_keyboard=forward_buttons)


sales_assistance_b = [[InlineKeyboardButton(text="Запустить помощника", callback_data="start_helper")],
                      [InlineKeyboardButton(text="Очистить контекст", callback_data="clear_data")],
                      [InlineKeyboardButton(text="Назад", callback_data="business_assistant")]]

sales_assistance= InlineKeyboardMarkup(inline_keyboard=sales_assistance_b)

to_sales_buttons = [[InlineKeyboardButton(text="Назад", callback_data="sales_assistance")]]
to_sales_menu = InlineKeyboardMarkup(inline_keyboard=to_sales_button)
