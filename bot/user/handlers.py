import datetime
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, LabeledPrice
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import logging
from sqlalchemy.orm import sessionmaker




from bot.tools.another_way import ask_question
from bot.tools.plugins.gpt_config import gpt_config
from bot.tools.plugin_manager import PluginManager
from bot.database.database import engine
import bot.user.texts as texts
import bot.user.keyboards as keyboards
import bot.database.crud.Subscriptions as SubscriptionsFuncs
import bot.database.crud.NewUsers as NewUsersFuncs
import bot.database.crud.History as HistoryFuncs
from bot.database.models.History import History as HistoryModel
from bot.database.models.NewUsers import NewUsers as NewUsersModel
from bot.database.models.Subscriptions import Subscriptions as SubscriptionsModel

router = Router()

logging.basicConfig(level=logging.INFO)



@router.message(Command("start"))
async def start_handler(message: Message):
    start_time = datetime.datetime.now()
    user_id=message.from_user.id
    logging.info("Команда /start вызвана")
    if NewUsersFuncs.user_in_database(user_id) and not(SubscriptionsFuncs.user_in_database(user_id)):
        logging.info("Пользователь уже в БД")
        current_time = datetime.datetime.now()
        joined_time, joined_date = NewUsersFuncs.get_user_join_time(user_id)[1].split('.')[0].split(':'), NewUsersFuncs.get_user_join_time(user_id)[0].split('-')
        print('ffff', joined_time, joined_date)
        joined_time_and_date = datetime.datetime(year=int(joined_date[0]), month=int(joined_date[1]),\
                                                 day=int(joined_date[2]), hour=int(joined_time[0]),\
                                                 minute=int(joined_time[1]), second=int(joined_time[2]))
        dif_time = (current_time-joined_time_and_date).total_seconds()
        print(dif_time)
        if dif_time > 86400:
            await message.answer(text="Пробное время закончилось. Вы можете приобрести подписку, чтобы продолжить пользование ботом.")
            return
    else:
        query = NewUsersModel(
        user_id=message.from_user.id,
        access_time=str(datetime.datetime.now().time()).split('.')[0],
        access_date=str(str(datetime.datetime.now().date()))
        )
        NewUsersFuncs.add_new_user(query)
        logging.info("Пользователь зарегистрирован")
    logging.error("before start")
    await message.answer(text=texts.hello_message, reply_markup=keyboards.to_main_menu_keyboard)
    end_time = datetime.datetime.now()
    duration = (end_time - start_time).total_seconds()
    logging.info(f"Команда /start выполнена за {duration} секунд")

@router.callback_query(F.data == "to_mmenu")
async def main_menu_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text=texts.main_menu_text, reply_markup=keyboards.main_menu_keyboard)

@router.callback_query(F.data == "main_menu_secound")
async def main_menu_secound_handler(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=keyboards.main_menu_secound_keyboard)

@router.callback_query(F.data == "donation")
async def donation_menu(bot: Bot, callback: CallbackQuery):
    user_id=callback.from_user.id
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title="Покупка ТГ",
        description="Покупка через ТГ",
        payload="Payment TG",
        provider_token="381764678:TEST:89879",
        currency='rub',
        prices=[
            LabeledPrice(
                label="Доступ",
                amount=99000
            ),
            LabeledPrice(
                label="НДС",
                amount=20000
            ),
            LabeledPrice(
                label="Скидка",
                amount=-20000
            ),
            LabeledPrice(
                label="Бонус",
                amount=-40000
            )
        ],
        max_tip_amount=500,
        suggested_tip_amounts=[1000, 2000],
        start_parameter='hiii',
        provider_data=None
    )
    '''
    if SubscriptionsFuncs.is_subscribed(user_id):
        time_left= SubscriptionsFuncs.get_time(user_id)
        text = f"{time_left.split()[0]} дней, {time_left.split()[2].split(':')[0]} часов и {time_left.split()[2].split(':')[2]} минут"
        await callback.message.edit_text(text=f"Осталось: {text}")
    else:
        await callback.message.edit_text(text=f"У вас нет подписки")
    '''

@router.callback_query(F.data == 'sms10')
async def process_sms10(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=keyboard.first)
    pass

@router.callback_query(F.data == 'sms11')
async def process_sms11(callback: CallbackQuery):
    await callback.message.edit_text('TXT', reply_markup=keyboard.second)
    pass

@router.callback_query(F.data == 'offer')
async def process_sms19(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=keyboard.sms_19)
    pass

@router.callback_query(F.data == 'send_to_client')
async def process_sms20(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=keyboard.sms_20)
    pass

@router.callback_query(F.data == 'find_clients')
async def process_sms21(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=keyboard.sms_21)
    pass

@router.callback_query(F.data == 'find_staff')
async def process_sms22(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=keyboard.sms_22)
    pass

@router.callback_query(F.data == 'sms21')
async def process_category_keywords_21(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=keyboard.category_keywords_21)
    pass

@router.callback_query(F.data == 'sms22')
async def process_category_keywords_22(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=keyboard.category_keywords_22)
    pass

@router.callback_query(F.data == "business_assistant")
async def business_handler(callback: CallbackQuery):
    await callback.message.edit_text(text=texts.business_text, reply_markup=keyboards.business_keyboard)

@router.callback_query(F.data == "channel_with_lessons")
async def lessons_channel(callback: CallbackQuery):
    pass

@router.callback_query(F.data == "networking_chat")
async def network_chat(callback: CallbackQuery):
    pass

@router.callback_query(F.data == "settings")
async def settings(callback: CallbackQuery):
    pass

@router.callback_query(F.data == "help_and_instructions")
async def help_and_instructions(callback: CallbackQuery):
    pass

@router.callback_query(F.data == "technical_support")
async def technical_support(callback: CallbackQuery):
    pass

class Questioning(StatesGroup):
    First_question = State()
    Second_question = State()
    Third_questiong = State()

@router.callback_query(F.data == "your_marketer")
async def your_marketer_handler(callback: CallbackQuery, state: FSMContext):
    if HistoryFuncs.user_in_database(callback.from_user.id):
        await callback.message.edit_text(text="Вы уже отвечали на вопросы, желаете пропустить их?", reply_markup=keyboards.marketer_question_keyboards)
    else:
        await callback.message.edit_text(text=texts.message1_1)
        await state.set_state(Questioning.First_question)

@router.callback_query(F.data == "complete_questions")
async def first_question(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text=texts.message1_1)
    await state.set_state(Questioning.First_question)

@router.message(Questioning.First_question)
async def first_question(message: Message, state: FSMContext):
    await state.update_data({"business": message.text})
    await message.answer(text=texts.message2)
    await state.set_state(Questioning.Second_question)

@router.message(Questioning.Second_question)
async def secound_question(message: Message, state: FSMContext):
    await state.update_data({"company": message.text})
    await message.answer(text=texts.message3)
    await state.set_state(Questioning.Third_questiong)

@router.message(Questioning.Third_questiong)
async def third_question(message: Message, state: FSMContext):
    await state.update_data({"audio": message.text})
    user_id = message.from_user.id
    data = await state.get_data()
    business, company, audience = data["business"], data["company"], data["audio"]
    query = HistoryModel(
        user_id=user_id,
        about_business=business,
        about_company=company,
        about_audience=audience,
        names_and_descriptions="",
        marketing_strategy_plan="",
        lead_magnet="",
        pinned_post="",
        content_plan="",
        stories_content="",
    )
    if HistoryFuncs.user_in_database(user_id):
        HistoryFuncs.edit_history(id=user_id, new_business=business, new_company=company, new_audience=audience)
    else:
        HistoryFuncs.add_new_user(query)
    logging.info(f"История пользователя '{user_id}' сохранена.")
    await message.answer(text=texts.message4, reply_markup=keyboards.continue_keyboard)
    await state.clear()


@router.callback_query(F.data == "follow")
async def third_block(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    user_id = callback.from_user.id
    business_info, company_info, audience_info = HistoryFuncs.get_history(user_id)
    names_and_descriptions_prompt = f"Придумай название и описание для телеграм канала проекта со следующим описанием проекта - {business_info}. Учти также описание его аудитории - {audience_info}. И воспользуйся информацией о продуктах - {company_info}. Описание должно быть не более 255 символов, а название должно содержать от 2 до 4 слов. Предложи 10 идей названий, каждое название пиши на новой строке. Не давай каких-либо комментариев. Пиши на русском языке"
    marketing_strategy_plan_prompt = f"Ты маркетолог в телеграм, твои формулировки точны, просты, понятны любым клиентам :: Составь концепцию для маркетинга, который поможет грамотно вести телеграм канал со следующим описанием проекта - {business_info}. Учти также описание его аудитории - {audience_info}. И воспользуйся информацией о продуктах - {company_info}. :: Результат должен включать в себя развернутые 4 пункта :: 1 - описание каждого Продукта из списка предоставленной информацией о продуктах. Включать, что мы продаем, для кого мы это делаем и как мы это делаем. 2 - описание конкурентных преимуществ. Почему именно мы, чем мы лучше других, почему стоит выбрать именно нас. 3 - детальное описание целевой аудитории на базе предоствленных данных о целевой аудитории. Должно содержать - Кто наш клиент, чего он хочет, какие у него есть потребности и желания. 4 - Позиционирование. Кто мы, что мы делаем и для кого :: Выведи ответ без вводных фраз с подробным описанием на все пункты. Пиши на русском языке"
    marketing_strategy_plan_response, marketing_strategy_plan_tokens = await ask_question(marketing_strategy_plan_prompt)
    # done лид магнит должен включать генерацию marketing_strategy_plan_prompt
    lead_magnet_prompt = f"Придумай 5 идей лид-магнитов для телеграм канала и бизнеса в целом. Распиши подробно каждый лид-магнит в 15 тезисов. Учти описание проекта - {business_info}. Учти также описание его аудитории - {audience_info}. И воспользуйся информацией о продуктах - {company_info}. Также вопсользуйся следующей информацией про маркетинг проекта - {marketing_strategy_plan_response}. Пиши на русском языке. Не давай каких-либо комментариев."
    lead_magnet_response, lead_magnet_tokens = await ask_question(lead_magnet_prompt)
    # done контент план должен содержать генерации marketing_strategy_plan_prompt и lead_magnet_prompt
    content_plan_prompt = f'Создай контент план для телеграм канала на 7 дней, по 2 поста в день. Посты должны быть разные: продающие, вовлекающие, информационные, познавательные, опросы, отзывы, рассказ о продуктах эксперта. В посте указывать, какой это пост, как в примере ""Вечерний пост (Познавательный)"" :: Учти описание проекта - {business_info}. Учти также описание его аудитории - {audience_info}. И воспользуйся информацией о продуктах - {company_info}. Также воспользуйся следующей информацией про маркетинг проекта - {marketing_strategy_plan_response}:: также учти наличие следующих лиц-магнитов - {lead_magnet_response}. Пиши на русском языке. Не давай каких-либо комментариев.'
    # done контент план для сторис должен содержать генерации marketing_strategy_plan_prompt и lead_magnet_prompt
    stories_content_prompt = f"Создай контент план сторис для телеграм канала на 7 дней, который должен включать 21 сторис. Сторис должны быть разные: продающие, вовлекающие, информационные, познавательные, опросы, отзывы, рассказ о продуктах эксперта. :: Учти описание проекта - {business_info}. Учти также описание его аудитории - {audience_info}. И воспользуйся информацией о продуктах - {company_info}. Также воспользуйся следующей информацией про маркетинг проекта - {marketing_strategy_plan_response} :: также учти наличие следующих лиц-магнитов - {lead_magnet_response}. Пиши на русском языке. Не давай каких-либо комментариев."
    # ради интереса, проверить сохраняет ли гпт контекст | в любом случае выполнять генерацию промпта последним
    pinned_post_prompt = f"Учитывая информацию о проекте, продуктах и контент план, напиши пост, который автор закрепит в телеграм. Пост должен вызвать интерес у людей, побудить записаться на консультацию, также укажи информацию о канале и авторе, о продуктах. Пост должен быть от 1500 до 2000 символов. Пиши на русском языке"
    names_and_descriptions_response, names_and_descriptions_total_tokens = await ask_question(names_and_descriptions_prompt)
    pinned_post_response, pinned_post_tokens = await ask_question(pinned_post_prompt)
    content_plan_response, content_plan_tokens = await ask_question(content_plan_prompt)
    stories_content_response, stories_content_tokens = await ask_question(stories_content_prompt)


    query = HistoryModel(
        user_id = user_id,
        about_business = business_info,
        about_company = company_info,
        about_audience = audience_info,
        names_and_descriptions = names_and_descriptions,
        marketing_strategy_plan = marketing_strategy_plan,
        lead_magnet = lead_magnet,
        pinned_post = pinned_post,
        content_plan = content_plan,
        stories_content = stories_content,
    )
    HistoryFuncs.edit_history(user_id, business_info, company_info, audience_info, names_and_descriptions, marketing_strategy_plan, lead_magnet, pinned_post, content_plan, stories_content)
    await callback.message.edit_reply_markup(reply_markup=keyboards.to_function_menu)

@router.callback_query(F.data == "next_keyboard1")
async def first_answer(callback: CallbackQuery):
    user_id = callback.from_user.id
    answer = HistoryFuncs.get_gpt_history(user_id)[0]
    text = texts.names(answer)
    await callback.message.edit_text(text=text, reply_markup=keyboards.to_function_menu)

@router.callback_query(F.data == "funcs_menu")
async def funcion_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text= "Добро пожаловать в главное меню! Я помогу тебе с созданием контента для телеграм канала и его ведением 📱. \nВот задачи, с которыми я могу помочь 👇", reply_markup=keyboards.your_marketer_keyboard)


@router.callback_query(F.data == "think_about_marketing")
async def marketing(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    if None in HistoryFuncs.get_gpt_history(user_id):
        await callback.message.edit_text(text="К сожалению, у нас не сохранились ваши ответы. Придется пройти заного")
        return restart_mark(callback, state)
    await callback.message.edit_text(text="Напомню, что уже немного знаю о твоем проекте, если ты хочешь получить решение по готовой информации - выбери нужную кнопку. Если хочешь “все … давай по новой” - выбери другую кнопку 😁", reply_markup=keyboards.restart_keyboard_mark)

class RestartQuestionsMark(StatesGroup):
    First = State()
    Second = State()
    Third = State()

@router.callback_query(F.data == "restart_questions_mark")
async def restart_mark(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(text=texts.message1_1)
    await state.set_state(RestartQuestionsMark.First)

@router.message(RestartQuestionsMark.First)
async def first_restarted_answer(message: Message, state: FSMContext):
    await state.update_data({"business": message.text})
    await message.edit_text(text=texts.message2)
    await state.set_state(RestartQuestionsMark.Second)

@router.message(RestartQuestionsMark.Second)
async def second_restarted_answer(message: Message, state: FSMContext):
    await state.update_data({"company": message.text})
    await message.edit_text(text=texts.message3)
    await state.set_state(RestartQuestionsMark.Third)

@router.message(RestartQuestionsMark.Third)
async def third_restarted_question(message: Message, state: FSMContext):
    await state.update_data({"audio": message.text})
    user_id = message.from_user.id
    data = await state.get_data()
    await state.clear()
    business, company, audience = data["business"], data["company"], data["audio"]
    query = HistoryModel(
        user_id=user_id,
        about_business=business,
        about_company=company,
        about_audience=audience,
        names_and_descriptions="",
        marketing_strategy_plan="",
        lead_magnet="",
        pinned_post="",
        content_plan="",
        stories_content="",
    )
    if HistoryFuncs.user_in_database(user_id):
        HistoryFuncs.edit_history(id=user_id, new_business=business, new_company=company, new_audience=audience)
    else:
        HistoryFuncs.add_new_user(query)
    logging.info(f"История пользователя '{user_id}' сохранена.")
    await message.edit_text(text="Итак, я поразмышляла над идеей. Скорее жми на кнопку, чтобы я могла поделиться ею с тобой", reply_markup=keyboards.continue_mark)


@router.callback_query(F.data=="mark_results")
async def mark_results(callback: CallbackQuery):
    await callback.answer()
    business_info, company_info, audience_info = HistoryFuncs.get_history(user_id)
    marketing_strategy_plan_prompt = f"Ты маркетолог в телеграм, твои формулировки точны, просты, понятны любым клиентам :: Составь концепцию для маркетинга, который поможет грамотно вести телеграм канал со следующим описанием проекта - {business_info}. Учти также описание его аудитории - {audience_info}. И воспользуйся информацией о продуктах - {company_info}. :: Результат должен включать в себя развернутые 4 пункта :: 1 - описание каждого Продукта из списка предоставленной информацией о продуктах. Включать, что мы продаем, для кого мы это делаем и как мы это делаем. 2 - описание конкурентных преимуществ. Почему именно мы, чем мы лучше других, почему стоит выбрать именно нас. 3 - детальное описание целевой аудитории на базе предоствленных данных о целевой аудитории. Должно содержать - Кто наш клиент, чего он хочет, какие у него есть потребности и желания. 4 - Позиционирование. Кто мы, что мы делаем и для кого :: Выведи ответ без вводных фраз с подробным описанием на все пункты. Пиши на русском языке"
    marketing_strategy_plan_response, marketing_strategy_plan_tokens = await ask_question(
        marketing_strategy_plan_prompt)
    HistoryFuncs.change_marketing(user_id, marketing_strategy_plan_response)
    await message.edit_text(text=f"Итак, вот идея маркетинга:\n {marketing_strategy_plan_response}", reply_markup=keyboards.to_fmenu_from_choices_kb)

@router.callback_query(F.data=='continue_questions_mark')
async def mark_skip(callback: CallbackQuery):
    user_id = callback.from_user.id
    mark_results = HistoryFuncs.get_gpt_history(user_id)[1]
    await callback.message.edit_text(text= f"Вот маркетинг:\n {mark_results}", reply_markup=keyboards.to_fmenu_from_choices_kb)



@router.callback_query(F.data == "create_post")
async def create_post(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    if None in HistoryFuncs.get_gpt_history(user_id):
        await callback.message.edit_text(text="К сожалению, у нас не сохранились ваши ответы. Придется пройти заного")
        return restart_post(callback, state)
    await callback.message.answer(
        text="Напомню, что уже немного знаю о твоем проекте, если ты хочешь получить решение по готовой информации - выбери нужную кнопку. Если хочешь “все … давай по новой” - выбери другую кнопку 😁",
        reply_markup=keyboards.restart_keyboard_post
)

class RestartQuestionsPost(StatesGroup):
    First = State()
    Second = State()
    Third = State()

@router.callback_query(F.data == "restart_questions_post")
async def restart_post(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text=texts.message1_1)
    await state.set_state(RestartQuestionsPost.First)

@router.message(RestartQuestionsPost.First)
async def first_restarted_answer(message: Message, state: FSMContext):
    await state.update_data({"business": message.text})
    await message.answer(text=texts.message2)
    await state.set_state(RestartQuestionsMark.Second)

@router.message(RestartQuestionsPost.Second)
async def second_restarted_answer(message: Message, state: FSMContext):
    await state.update_data({"company": message.text})
    await message.answer(text=texts.message3)
    await state.set_state(RestartQuestionsPost.Third)

@router.message(RestartQuestionsPost.Third)
async def third_restarted_question(message: Message, state: FSMContext):
    await state.update_data({"audio": message.text})
    user_id = message.from_user.id
    data = await state.get_data()
    await state.clear()
    business, company, audience = data["business"], data["company"], data["audio"]
    query = HistoryModel(
        user_id=user_id,
        about_business=business,
        about_company=company,
        about_audience=audience,
        names_and_descriptions="",
        marketing_strategy_plan="",
        lead_magnet="",
        pinned_post="",
        content_plan="",
        stories_content="",
    )
    if HistoryFuncs.user_in_database(user_id):
        HistoryFuncs.edit_history(id=user_id, new_business=business, new_company=company, new_audience=audience)
    else:
        HistoryFuncs.add_new_user(query)
    logging.info(f"История пользователя '{user_id}' сохранена.")
    await message.answer(text="Итак, я поразмышляла над идеей. Скорее жми на кнопку, чтобы я могла поделиться ею с тобой", reply_markup=keyboards.continue_post)


@router.callback_query(F.data=="post_results")
async def post_results(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    business_info, company_info, audience_info = HistoryFuncs.get_history(user_id)
    pinned_post_prompt = f"Учитывая информацию о проекте, продуктах и контент план, напиши пост, который автор закрепит в телеграм. Пост должен вызвать интерес у людей, побудить записаться на консультацию, также укажи информацию о канале и авторе, о продуктах. Пост должен быть от 1500 до 2000 символов. Пиши на русском языке"
    pinned_post, pinned_post_tokens = await ask_question(
        pinned_post_prompt)
    HistoryFuncs.change_ppost(user_id, pinned_post)
    await message.edit_text(text=f"{pinned_post}\nЧтобы человек остался в канале, важно сразу дать ему понять, что ценного он здесь получит, поэтому я подготовил для тебя пост-закреп - оцени его и жми на кнопку ниже ", reply_markup=keyboards.to_fmenu_from_choices_kb)

@router.callback_query(F.data=='continue_questions_post')
async def post_skip(callback: CallbackQuery):
    user_id = callback.from_user.id
    post_result = HistoryFuncs.get_gpt_history(user_id)[3]
    await callback.message.edit_text(text= f"{post_result}\nЧтобы человек остался в канале, важно сразу дать ему понять, что ценного он здесь получит, поэтому я подготовил для тебя пост-закреп - оцени его ниже и жми на кнопку ниже ", reply_markup=keyboards.to_fmenu_from_choices_kb)

@router.callback_query(F.data == "create_content_plan")
async def create_content_plan(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    if None in HistoryFuncs.get_gpt_history(user_id):
        await callback.message.edit_text(text="К сожалению, у нас не сохранились ваши ответы. Придется пройти заного")
        return restart_content(callback, state)
    await callback.message.edit_text(text="Напомню, что уже немного знаю о твоем проекте, если ты хочешь получить решение по готовой информации - выбери нужную кнопку. Если хочешь “все … давай по новой” - выбери другую кнопку 😁", reply_markup=keyboards.restart_keyboard_content)


class RestartQuestionsContent(StatesGroup):
    First = State()
    Second = State()
    Third = State()

@router.callback_query(F.data == "restart_questions_content")
async def restart_content(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text=texts.message1_1)
    await state.set_state(RestartQuestionsContent.First)

@router.message(RestartQuestionsContent.First)
async def first_restarted_answer(message: Message, state: FSMContext):
    await state.update_data({"business": message.text})
    await message.answer(text=texts.message2)
    await state.set_state(RestartQuestionsContent.Second)

@router.message(RestartQuestionsContent.Second)
async def second_restarted_answer(message: Message, state: FSMContext):
    await state.update_data({"company": message.text})
    await message.answer(text=texts.message3)
    await state.set_state(RestartQuestionsContent.Third)

@router.message(RestartQuestionsContent.Third)
async def third_restarted_question(message: Message, state: FSMContext):
    await state.update_data({"audio": message.text})
    user_id = message.from_user.id
    data = await state.get_data()
    await state.clear()
    business, company, audience = data["business"], data["company"], data["audio"]
    query = HistoryModel(
        user_id=user_id,
        about_business=business,
        about_company=company,
        about_audience=audience,
        names_and_descriptions="",
        marketing_strategy_plan="",
        lead_magnet="",
        pinned_post="",
        content_plan="",
        stories_content="",
    )
    if HistoryFuncs.user_in_database(user_id):
        HistoryFuncs.edit_history(id=user_id, new_business=business, new_company=company, new_audience=audience)
    else:
        HistoryFuncs.add_new_user(query)
    logging.info(f"История пользователя '{user_id}' сохранена.")
    await message.answer(text="Итак, я поразмышляла над идеей. Теперь определись, какой длительностью будет наш контент-план", reply_markup=keyboards.content_days)

@router.callback_query(F.data=="continue_questions_content")
async def skip_content(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Итак, я поразмышляла над идеей. Теперь определись, какой длительностью будет наш контент-план",
        reply_markup=keyboards.content_days)

@router.callback_query(F.data == "one_content_day")
async def one_content_day(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    business_info, company_info, audience_info = HistoryFuncs.get_history(user_id)
    content_plan_prompt = f'Создай контент план для телеграм канала на 1 день, по 2 поста. Посты должны быть разные: продающие, вовлекающие, информационные, познавательные, опросы, отзывы, рассказ о продуктах эксперта. В посте указывать, какой это пост, как в примере ""Вечерний пост (Познавательный)"" :: Учти описание проекта - {business_info}. Учти также описание его аудитории - {audience_info}. И воспользуйся информацией о продуктах - {company_info}. Также воспользуйся следующей информацией про маркетинг проекта - {marketing_strategy_plan_response}:: также учти наличие следующих лиц-магнитов - {lead_magnet_response}. Пиши на русском языке. Не давай каких-либо комментариев.'
    HistoryFuncs.change_content(user_id, content_plan)
    await callback.message.edit_text(text=f"Отлично, вот такие посты нам точно стоит сделать в ближайший день\n {content_plan} \nХочешь, чтобы я написала каждый пост сама? 😍",
                            reply_markup=keyboards.to_fmenu_from_choices_kb)


@router.callback_query(F.data == "three_content_day")
async def three_content_day(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    business_info, company_info, audience_info = HistoryFuncs.get_history(user_id)
    content_plan_prompt = f'Создай контент план для телеграм канала на 3 дня, по 2 поста в день. Посты должны быть разные: продающие, вовлекающие, информационные, познавательные, опросы, отзывы, рассказ о продуктах эксперта. В посте указывать, какой это пост, как в примере ""Вечерний пост (Познавательный)"" :: Учти описание проекта - {business_info}. Учти также описание его аудитории - {audience_info}. И воспользуйся информацией о продуктах - {company_info}. Также воспользуйся следующей информацией про маркетинг проекта - {marketing_strategy_plan_response}:: также учти наличие следующих лиц-магнитов - {lead_magnet_response}. Пиши на русском языке. Не давай каких-либо комментариев.'

    HistoryFuncs.change_content(user_id, content_plan)
    await callback.message.edit_text(text=f"Отлично, вот такие посты нам точно стоит сделать в ближайшие 3 дня\n {content_plan} \nХочешь, чтобы я написала каждый пост сама? 😍",
                            reply_markup=keyboards.to_fmenu_from_choices_kb)

@router.callback_query(F.data == "seven_content_day")
async def one_content_day(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    business_info, company_info, audience_info = HistoryFuncs.get_history(user_id)
    content_plan_prompt = f'Создай контент план для телеграм канала на 7 дней, по 2 поста в день. Посты должны быть разные: продающие, вовлекающие, информационные, познавательные, опросы, отзывы, рассказ о продуктах эксперта. В посте указывать, какой это пост, как в примере ""Вечерний пост (Познавательный)"" :: Учти описание проекта - {business_info}. Учти также описание его аудитории - {audience_info}. И воспользуйся информацией о продуктах - {company_info}. Также воспользуйся следующей информацией про маркетинг проекта - {marketing_strategy_plan_response}:: также учти наличие следующих лиц-магнитов - {lead_magnet_response}. Пиши на русском языке. Не давай каких-либо комментариев.'
    HistoryFuncs.change_content(user_id, content_plan)
    await callback.message.edit_text(text=f"Отлично, вот такие посты нам точно стоит сделать в ближайшую неделю\n {content_plan} \nХочешь, чтобы я написала каждый пост сама? 😍",
                            reply_markup=keyboards.to_fmenu_from_choices_kb)


@router.callback_query(F.data == "create_shorts")
async def create_shorts(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    if None in HistoryFuncs.get_gpt_history(user_id):
        await callback.message.edit_text(text="К сожалению, у нас не сохранились ваши ответы. Придется пройти заного")
        return restart_content(callback, state)
    await callback.message.edit_text(
        text="Напомню, что уже немного знаю о твоем проекте, если ты хочешь получить решение по готовой информации - выбери нужную кнопку. Если “все …, давай по новой” - выбери другую кнопку 😁",
        reply_markup=keyboards.restart_keyboard_shorts)


class RestartQuestionsShorts(StatesGroup):
    First = State()
    Second = State()
    Third = State()

@router.callback_query(F.data == "restart_questions_shorts")
async def restart_content(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text=texts.message1_1)
    await state.set_state(RestartQuestionsShorts.First)

@router.message(RestartQuestionsShorts.First)
async def first_restarted_answer(message: Message, state: FSMContext):
    await state.update_data({"business": message.text})
    await message.answer(text=texts.message2)
    await state.set_state(RestartQuestionsShorts.Second)

@router.message(RestartQuestionsShorts.Second)
async def second_restarted_answer(message: Message, state: FSMContext):
    await state.update_data({"company": message.text})
    await message.answer(text=texts.message3)
    await state.set_state(RestartQuestionsShorts.Third)

@router.message(RestartQuestionsShorts.Third)
async def third_restarted_question(message: Message, state: FSMContext):
    await state.update_data({"audio": message.text})
    user_id = message.from_user.id
    data = await state.get_data()
    await state.clear()
    business, company, audience = data["business"], data["company"], data["audio"]
    query = HistoryModel(
        user_id=user_id,
        about_business=business,
        about_company=company,
        about_audience=audience,
        names_and_descriptions="",
        marketing_strategy_plan="",
        lead_magnet="",
        pinned_post="",
        content_plan="",
        stories_content="",
    )
    if HistoryFuncs.user_in_database(user_id):
        HistoryFuncs.edit_history(id=user_id, new_business=business, new_company=company, new_audience=audience)
    else:
        HistoryFuncs.add_new_user(query)
    logging.info(f"История пользователя '{user_id}' сохранена.")
    await message.answer(text="Итак, я поразмышляла над идеей. Скорее ознакомься с планом ниже по кнопке!", reply_markup=keyboards.continue_shorts)


@router.callback_query(F.data == "shorts_results")
async def shorts_results(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    business_info, company_info, audience_info = HistoryFuncs.get_history(user_id)
    youtube_shorts_prompt = f"Учитывая информацию о проекте, продуктах и контент план, напиши пост, который автор закрепит в телеграм. Пост должен вызвать интерес у людей, побудить записаться на консультацию, также укажи информацию о канале и авторе, о продуктах. Пост должен быть от 1500 до 2000 символов. Пиши на русском языке"
    youtube_shorts, youtube_shorts_tokens = await ask_question(
        youtube_shorts_prompt)
    HistoryFuncs.change_shorts(user_id, youtube_shorts)
    await message.edit_text(
        text=f"{pinned_post}\nЧтобы человек остался в канале, важно сразу дать ему понять, что ценного он здесь получит, поэтому я подготовил для тебя пост-закреп - оцени его и жми на кнопку ниже ",
        reply_markup=keyboards.to_fmenu_from_choices_kb)

@router.callback_query(F.data=="continue_questions_shorts")
async def skip_shorts(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    youtube_shorts = HistoryFuncs.get_gpt_history[5]
    HistoryFuncs.change_shorts(user_id, youtube_shorts)
    await message.edit_text(
        text=f"{pinned_post}\nЧтобы человек остался в канале, важно сразу дать ему понять, что ценного он здесь получит, поэтому я подготовил для тебя пост-закреп - оцени его и жми на кнопку ниже ",
        reply_markup=keyboards.to_fmenu_from_choices_kb)
