import datetime
from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import CallbackQuery, Message, LabeledPrice, PreCheckoutQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import logging
from sqlalchemy.orm import sessionmaker
from aiogram.utils.deep_linking import create_start_link, decode_payload
import openai

from bot.tools.gpt import ask_gpt
from bot.tools.plugins.config import config
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

async def create_answers(business_info, company_info, audience_info):
    marketing_strategy_plan_prompt = f"Ты маркетолог в телеграм, твои формулировки точны, просты, понятны любым клиентам :: Составь концепцию для маркетинга, который поможет грамотно вести телеграм канал со следующим описанием проекта - {business_info}. Учти также описание его аудитории - {audience_info}. И воспользуйся информацией о продуктах - {company_info}. :: Результат должен включать в себя развернутые 4 пункта :: 1 - описание каждого Продукта из списка предоставленной информацией о продуктах. Включать, что мы продаем, для кого мы это делаем и как мы это делаем. 2 - описание конкурентных преимуществ. Почему именно мы, чем мы лучше других, почему стоит выбрать именно нас. 3 - детальное описание целевой аудитории на базе предоствленных данных о целевой аудитории. Должно содержать - Кто наш клиент, чего он хочет, какие у него есть потребности и желания. 4 - Позиционирование. Кто мы, что мы делаем и для кого :: Выведи ответ без вводных фраз с подробным описанием на все пункты. Пиши на русском языке"
    mark_answer = await ask_gpt(marketing_strategy_plan_prompt)
    lead_magnet_prompt = f"Придумай 3 идеи лид-магнитов для телеграм канала и бизнеса в целом. Распиши подробно каждый лид-магнит в 10 тезисов. Учти описание проекта - {business_info}. Учти также описание его аудитории - {audience_info}. И воспользуйся информацией о продуктах - {company_info}. Также вопсользуйся следующей информацией про маркетинг проекта - {mark_answer}. Пиши на русском языке. Не давай каких-либо комментариев."
    lead_answer = await ask_gpt(lead_magnet_prompt)
    content_plan_prompt = content_plan_prompt = f'Создай контент план для телеграм канала на 7 дней, по 2 поста в день. Посты должны быть разные: продающие, вовлекающие, информационные, познавательные, опросы, отзывы, рассказ о продуктах эксперта. В посте указывать, какой это пост, как в примере ""Вечерний пост (Познавательный)"" :: Учти описание проекта - {business_info}. Учти также описание его аудитории - {audience_info}. И воспользуйся информацией о продуктах - {company_info}. Также воспользуйся следующей информацией про маркетинг проекта - {mark_answer}:: также учти наличие следующих лиц-магнитов - {lead_answer}. Пиши на русском языке'
    content_plan = await ask_gpt(content_plan_prompt)
    pinned_post_prompt = f"Учитывая информацию о проекте {business_info}, продуктах {company_info} и контент-план {content_plan}, напиши пост, который автор закрепит в телеграм. Пост должен вызвать интерес у людей, побудить записаться на консультацию, также укажи информацию о канале и авторе, о продуктах. Пост должен быть от 1500 до 2000 символов. Пиши на русском языке"
    post_answer = await ask_gpt(pinned_post_prompt)
    return mark_answer, post_answer, content_plan, lead_answer



@router.message(Command("start"))
async def start_handler(message: Message, command: CommandObject):
    current_time = datetime.datetime.now()
    user_id = message.from_user.id
    logging.info("Команда /start вызвана")
    if NewUsersFuncs.user_in_database(user_id) and not (SubscriptionsFuncs.user_in_database(user_id)):
        logging.info("Пользователь уже в БД")
        joined_time, joined_date = NewUsersFuncs.get_user_join_time(user_id)[1].split('.')[0].split(':'), \
        NewUsersFuncs.get_user_join_time(user_id)[0].split('-')
        joined_time_and_date = datetime.datetime(year=int(joined_date[0]), month=int(joined_date[1]), \
                                                 day=int(joined_date[2]), hour=int(joined_time[0]), \
                                                 minute=int(joined_time[1]), second=int(joined_time[2]))
        dif_time = (current_time - joined_time_and_date).total_seconds()
        if dif_time > 86400:
            await message.answer(
                text="Пробное время закончилось. Вы можете приобрести подписку, чтобы продолжить пользование ботом.")
            return donation_menu(CallbackQuery)
    elif (SubscriptionsFuncs.user_in_database(user_id)):
        log_day, log_time = SubscriptionsFuncs.get_date(user_id)[0].split('-'), \
        SubscriptionsFuncs.get_date(user_id)[1].split('.')[0].split[":"]
        subscribed_time_and_day = datetime.datetime(year=log_time[0], month=log_day[1], day=log_day[2],
                                                    hour=log_time[0], minute=log_time[1], second=log_time[2])
        dif_time = (current_time - subscribed_time_and_day).total_seconds()
        subscribed_day = SubscriptionsFuncs.get_days(user_id)
        if dif_time > (subscribed_day * 86400):
            await message.answer(text="Подписка истекла")
            return donation_menu(CallbackQuery)
    else:
        query = NewUsersModel(
            user_id=message.from_user.id,
            access_time=str(datetime.datetime.now().time()).split('.')[0],
            access_date=str(str(datetime.datetime.now().date()))
        )
        NewUsersFuncs.add_new_user(query)
        logging.info("Пользователь зарегистрирован")
    logging.error("before start")
    try:
        args = command.get_args()
        reference = decode_payload(args)
        await message.answer(text=texts.hello_message + f"\n Ваш реферал {reference}",
                             reply_markup=keyboards.to_main_menu_keyboard)
    except:
        await message.answer(text=texts.hello_message,
                             reply_markup=keyboards.to_main_menu_keyboard)


@router.callback_query(F.data == "to_mmenu")
async def main_menu_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text=texts.main_menu_text, reply_markup=keyboards.main_menu_keyboard)


@router.callback_query(F.data == "main_menu_secound")
async def main_menu_secound_handler(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=keyboards.main_menu_secound_keyboard)


@router.callback_query(F.data=="referal_and_donation")
async def referal_and_donation(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(text="referal_and_donation", reply_markup=keyboards.refer_donat_kb)



@router.callback_query(F.data == "referal_system")
async def referal(bot: Bot, callback: CallbackQuery):
    await callback.answer()
    referal_url = await create_start_link(bot=bot, payload=str(callback.from_user.username))
    await message.answer(text=f"Ваша реферальная ссылка: {referal_url}", reply_markup=keyboards.to_main_menu_keyboard)


@router.callback_query(F.data == "donation")
async def donation_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    if SubscriptionsFuncs.user_in_database(user_id):
        time_left = SubscriptionsFuncs.get_time(user_id)
        text = f"{time_left.split()[0]} дней, {time_left.split()[2].split(':')[0]} часов и {time_left.split()[2].split(':')[2]} минут"
        await callback.message.edit_text(text=f"Осталось: {text}", reply_markup=keyboards.subscribtion_buy_keyboard)
    else:
        await callback.message.edit_text(text=f"У вас нет подписки", reply_markup=keyboards.subscribtion_buy_keyboard)


@router.callback_query(F.data == "common_buy")
async def sub_bay(callback: CallbackQuery, bot: Bot):
    prices = [
        LabeledPrice(label='Полный функционал', amount=10000)  # 1000 копеек = 10.00 рублей
    ]
    await bot.send_invoice(chat_id=callback.message.chat.id,
                           title="Подписка на бота",
                           description="Активация подписки на бота на 1 месяц",
                           provider_token="381764678:TEST:89879",
                           currency="rub",
                           prices=prices,
                           start_parameter="start",
                           payload="test-invoice-payload")


@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message, bot: Bot):
    logging.info("SUCCESSFUL PAYMENT")
    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")
    if SubscriptionsFuncs.user_in_database(message.from_user.id):
        SubscriptionsFuncs.add_days(message.from_user.id, 30, False)
    else:
        query = SubscriptionsModel(
            user_id=message.from_user.id,
            subscription_date=str(datetime.datetime.now().date),
            subscription_time=str(datetime.datetime.now().time()),
            subscription_days=30,
            access_to_chats=False
        )
        SubscriptionsFuncs.add_new_user(query)


@router.callback_query(F.data == "exclusive_buy")
async def sub_bay(callback: CallbackQuery, bot: Bot):
    prices = [
        LabeledPrice(label='Полный функционал+Доступ к чатам', amount=10000)  # 1000 копеек = 10.00 рублей
    ]
    await bot.send_invoice(chat_id=callback.message.chat.id,
                           title="Подписка на бота",
                           description="Активация подписки на бота на 1 месяц",
                           provider_token="381764678:TEST:89879",
                           currency="rub",
                           prices=prices,
                           start_parameter="start",
                           payload="test-invoice-payload")


@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message, bot: Bot):
    logging.info("SUCCESSFUL PAYMENT")
    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")
    if SubscriptionsFuncs.user_in_database(message.from_user.id):
        SubscriptionsFuncs.add_days(message.from_user.id, 30, True)
    else:
        query = SubscriptionsModel(
            user_id=message.from_user.id,
            subscription_date=str(datetime.datetime.now().date),
            subscription_time=str(datetime.datetime.now().time()),
            subscription_days=30,
            access_to_chats=True
        )
        SubscriptionsFuncs.add_new_user(query)


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
        await callback.message.delete()
        await callback.message.answer(text="Вы уже отвечали на вопросы, желаете пропустить их?",
                                      reply_markup=keyboards.marketer_question_keyboards)
    else:
        await callback.message.delete()
        await callback.message.answer(text=texts.message1_1)
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
        marketing_strategy_plan="",
        lead_magnet="",
        pinned_post="",
        content_plan="",
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
    await callback.message.edit_text(text="Одну минутку...", reply_markup=None)
    business_info, company_info, audience_info = HistoryFuncs.get_history(user_id)
    marketing_strategy_plan_response, pinned_post_response, content_plan_response, lead_magnet_response = await create_answers(business_info, company_info, audience_info)
    HistoryFuncs.edit_history(user_id, business_info, company_info, audience_info, \
                              marketing_strategy_plan_response, lead_magnet_response, pinned_post_response, \
                              content_plan_response)
    return await funcion_menu(callback)


@router.callback_query(F.data == "next_keyboard1")
async def first_answer(callback: CallbackQuery):
    user_id = callback.from_user.id
    answer = HistoryFuncs.get_gpt_history(user_id)[0]
    text = texts.names(answer)
    await callback.message.edit_text(text=text, reply_markup=keyboards.to_function_menu)


@router.callback_query(F.data == "funcs_menu")
async def funcion_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        text="Добро пожаловать в главное меню! Я помогу тебе с созданием контента для телеграм канала и его ведением 📱. \nВот задачи, с которыми я могу помочь 👇",
        reply_markup=keyboards.your_marketer_keyboard)


@router.callback_query(F.data == "think_about_marketing")
async def marketing(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    if None in HistoryFuncs.get_gpt_history(user_id):
        await callback.message.edit_text(text="К сожалению, у нас не сохранились ваши ответы. Придется пройти заного")
        return restart_mark(callback, state)
    await callback.message.edit_text(
        text="Напомню, что уже немного знаю о твоем проекте, если ты хочешь получить решение по готовой информации - выбери нужную кнопку. Если хочешь “все … давай по новой” - выбери другую кнопку 😁",
        reply_markup=keyboards.restart_keyboard_mark)


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
        marketing_strategy_plan="",
        lead_magnet="",
        pinned_post="",
        content_plan="",
    )
    if HistoryFuncs.user_in_database(user_id):
        HistoryFuncs.edit_history(id=user_id, new_business=business, new_company=company, new_audience=audience)
    else:
        HistoryFuncs.add_new_user(query)
    logging.info(f"История пользователя '{user_id}' сохранена.")
    await message.edit_text(
        text="Итак, я поразмышляла над идеей. Скорее жми на кнопку, чтобы я могла поделиться ею с тобой",
        reply_markup=keyboards.continue_mark)


@router.callback_query(F.data == "mark_results")
async def mark_results(callback: CallbackQuery):
    await callback.answer()
    business_info, company_info, audience_info = HistoryFuncs.get_history(user_id)
    marketing_strategy_plan_prompt = f"Ты маркетолог в телеграм, твои формулировки точны, просты, понятны любым клиентам :: Составь концепцию для маркетинга, который поможет грамотно вести телеграм канал со следующим описанием проекта - {business_info}. Учти также описание его аудитории - {audience_info}. И воспользуйся информацией о продуктах - {company_info}. :: Результат должен включать в себя развернутые 4 пункта :: 1 - описание каждого Продукта из списка предоставленной информацией о продуктах. Включать, что мы продаем, для кого мы это делаем и как мы это делаем. 2 - описание конкурентных преимуществ. Почему именно мы, чем мы лучше других, почему стоит выбрать именно нас. 3 - детальное описание целевой аудитории на базе предоствленных данных о целевой аудитории. Должно содержать - Кто наш клиент, чего он хочет, какие у него есть потребности и желания. 4 - Позиционирование. Кто мы, что мы делаем и для кого :: Выведи ответ без вводных фраз с подробным описанием на все пункты. Пиши на русском языке"
    marketing_strategy_plan_response = await ask_gpt(
        marketing_strategy_plan_prompt)
    HistoryFuncs.change_marketing(user_id, marketing_strategy_plan_response)
    await message.edit_text(text=f"Итак, вот идея маркетинга:\n {marketing_strategy_plan_response}",
                            reply_markup=keyboards.to_fmenu_from_choices_kb)


@router.callback_query(F.data == 'continue_questions_mark')
async def mark_skip(callback: CallbackQuery):
    user_id = callback.from_user.id
    mark_results = HistoryFuncs.get_gpt_history(user_id)[1]
    await callback.message.edit_text(text=f"Вот маркетинг:\n {mark_results}",
                                     reply_markup=keyboards.to_fmenu_from_choices_kb)


@router.callback_query(F.data == "create_content_plan")
async def create_content_plan(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    if None in HistoryFuncs.get_gpt_history(user_id):
        await callback.message.edit_text(text="К сожалению, у нас не сохранились ваши ответы. Придется пройти заного")
        return restart_content(callback, state)
    await callback.message.edit_text(
        text="Напомню, что уже немного знаю о твоем проекте, если ты хочешь получить решение по готовой информации - выбери нужную кнопку. Если хочешь “все … давай по новой” - выбери другую кнопку 😁",
        reply_markup=keyboards.restart_keyboard_content)


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
        marketing_strategy_plan="",
        lead_magnet="",
        pinned_post="",
        content_plan="",
    )
    if HistoryFuncs.user_in_database(user_id):
        HistoryFuncs.edit_history(id=user_id, new_business=business, new_company=company, new_audience=audience)
    else:
        HistoryFuncs.add_new_user(query)
    logging.info(f"История пользователя '{user_id}' сохранена.")
    await message.answer(
        text="Итак, я поразмышляла над идеей. Теперь определись, какой длительностью будет наш контент-план",
        reply_markup=keyboards.content_days)


@router.callback_query(F.data == "continue_questions_content")
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
    content_plan = await ask_gpt(content_plan_prompt)
    HistoryFuncs.change_content(user_id, content_plan)
    await callback.message.edit_text(
        text=f"Отлично, вот такие посты нам точно стоит сделать в ближайший день\n {content_plan} \nХочешь, чтобы я написала каждый пост сама? 😍",
        reply_markup=keyboards.to_fmenu_from_choices_kb)


@router.callback_query(F.data == "three_content_day")
async def three_content_day(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    business_info, company_info, audience_info = HistoryFuncs.get_history(user_id)
    content_plan_prompt = f'Создай контент план для телеграм канала на 3 дня, по 2 поста в день. Посты должны быть разные: продающие, вовлекающие, информационные, познавательные, опросы, отзывы, рассказ о продуктах эксперта. В посте указывать, какой это пост, как в примере ""Вечерний пост (Познавательный)"" :: Учти описание проекта - {business_info}. Учти также описание его аудитории - {audience_info}. И воспользуйся информацией о продуктах - {company_info}. Также воспользуйся следующей информацией про маркетинг проекта - {marketing_strategy_plan_response}:: также учти наличие следующих лиц-магнитов - {lead_magnet_response}. Пиши на русском языке. Не давай каких-либо комментариев.'
    content_plan = await ask_gpt(content_plan_prompt)
    HistoryFuncs.change_content(user_id, content_plan)
    await callback.message.edit_text(
        text=f"Отлично, вот такие посты нам точно стоит сделать в ближайшие 3 дня\n {content_plan} \nХочешь, чтобы я написала каждый пост сама? 😍",
        reply_markup=keyboards.to_fmenu_from_choices_kb)


@router.callback_query(F.data == "seven_content_day")
async def one_content_day(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    business_info, company_info, audience_info = HistoryFuncs.get_history(user_id)
    content_plan_prompt = f'Создай контент план для телеграм канала на 7 дней, по 2 поста в день. Посты должны быть разные: продающие, вовлекающие, информационные, познавательные, опросы, отзывы, рассказ о продуктах эксперта. В посте указывать, какой это пост, как в примере ""Вечерний пост (Познавательный)"" :: Учти описание проекта - {business_info}. Учти также описание его аудитории - {audience_info}. И воспользуйся информацией о продуктах - {company_info}. Также воспользуйся следующей информацией про маркетинг проекта - {marketing_strategy_plan_response}:: также учти наличие следующих лиц-магнитов - {lead_magnet_response}. Пиши на русском языке. Не давай каких-либо комментариев.'
    content_plan = await ask_gpt(content_plan_prompt)
    HistoryFuncs.change_content(user_id, content_plan)
    await callback.message.edit_text(
        text=f"Отлично, вот такие посты нам точно стоит сделать в ближайшую неделю\n {content_plan} \nХочешь, чтобы я написала каждый пост сама? 😍",
        reply_markup=keyboards.to_fmenu_from_choices_kb)


class Shorts(StatesGroup):
    First = State()


@router.callback_query(F.data == "create_shorts")
async def create_shorts(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(
        text="Итак, прежде чем мы начнем, сообщите, о чем будет наш youtube-shorts? Ответ начинайте с 'О...', например: 'О животных'. Помните, чем больше вы напишите, тем лучше")
    await state.set_state(Shorts.First)


@router.message(Shorts.First)
async def shorts_about(message: Message):
    msg = message.text
    await message.answer(text="Такс, дай мне секунду подумать...")
    shorts_query = f"Распиши 3 сценариев коротких видео по теме {msg} :: указав место съемки, раскадровку с числом секунд :: Полный текст, описание ролика с призывом к действию. Ответ должен быть на Русском языке. При создания сценария можно использовать один из методов по списку ниже: 1. Метод «скользкой горки» 2. Техника «шевеления занавеса» 3. Техника «Ложных следов» 4. Метод «Внутренний конфликт» 5. Техника «Крючок»"
    shorts_response = await ask_gpt(shorts_query)
    await message.edit_text(text=f'Вот идеи для youtube-shorts на заданную вами тему:\n\n{shorts_response}',
                            reply_markup=keyboards.to_fmenu_from_choices_kb)


@router.callback_query(F.data == "create_post")
async def create_post(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        text="Отлично - люблю писать посты. Можем воспользоваться заготовленными материалами, либо ввести новые данные о твоем канале - а еще ты можешь полностью сам сформулировать нужный запрос, и я адаптирую пост под формат телеграмма 😁",
        reply_markup=keyboards.restart_keyboard_post)


@router.callback_query(F.data == "continue_questions_post")
async def skip_questions_post(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        text='Хорошо, будем использовать старые ответы. Теперь необходимо определиться, от чьего лица будут писаться посты?',
        reply_markup=keyboards.face_keyboard)


@router.callback_query(F.data == "restart_questions_post")
async def restart_post(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        text="Хорошо. Желаете ли вы сами написать о чем будет пост, или предпочтете ответить по формам?",
        reply_markup=keyboards.post_choose)


class RestartQuestionsPost(StatesGroup):
    First = State()
    Second = State()
    Third = State()


@router.callback_query(F.data == "post_by_bot")
async def post_by_bot(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text=texts.message1_1)
    await state.set_state(RestartQuestionsPost.First)


@router.message(RestartQuestionsPost.First)
async def first_restarted_answer(message: Message, state: FSMContext):
    await state.update_data({"business": message.text})
    await message.answer(text=texts.message2)
    await state.set_state(RestartQuestionsPost.Second)


@router.message(RestartQuestionsContent.Second)
async def second_restarted_answer(message: Message, state: FSMContext):
    await state.update_data({"company": message.text})
    await message.answer(text=texts.message3)
    await state.set_state(RestartQuestionsPost.Third)


@router.message(RestartQuestionsContent.Third)
async def third_restarted_question(message: Message, state: FSMContext):
    await state.update_data({"audio": message.text})
    user_id = message.from_user.id
    data = await state.get_data()
    await state.set_state()
    business, company, audience = data["business"], data["company"], data["audio"]
    query = HistoryModel(
        user_id=user_id,
        about_business=business,
        about_company=company,
        about_audience=audience,
        marketing_strategy_plan="",
        lead_magnet="",
        pinned_post="",
        content_plan="",
    )
    if HistoryFuncs.user_in_database(user_id):
        HistoryFuncs.edit_history(id=user_id, new_business=business, new_company=company, new_audience=audience)
    else:
        HistoryFuncs.add_new_user(query)
    logging.info(f"История пользователя '{user_id}' сохранена.")
    await message.answer(
        text="Хорошо. Теперь необходимо определиться, от чьего лица будут писаться посты",
        reply_markup=keyboards.face_keyboard)


@router.callback_query(F.data == "from_me")
async def from_me(callback: CallbackQuery):
    await callback.answer()
    await state.update_data({"face": "Я"})
    await callback.message.edit_text(
        text="Теперь необходимо определиться с тоном, как мы будем обращаться к читателям?",
        reply_markup=keyboards.tone_keyboard)


@router.callback_query(F.data == "from_us")
async def from_us(callback: CallbackQuery):
    await callback.answer()
    await state.update_data({"face": "Мы"})
    await callback.message.edit_text(
        text="Теперь необходимо определиться с тоном, как мы будем обращаться к читателям?",
        reply_markup=keyboards.tone_keyboard)


@router.callback_query(F.data == "friendly_tone")
async def friendly_tone(callback: CallbackQuery):
    await callback.answer()
    await state.update_data({"tone": "Дружелюбный"})
    await callback.message.edit_text(text="Каким будет характер поста?", reply_markup=keyboards.chara_keyboard)


@router.callback_query(F.data == "classic_tone")
async def classic_tone(callback: CallbackQuery):
    await callback.answer()
    await state.update_data({"tone": "Классический"})
    await callback.message.edit_text(text="Каким будет характер поста?", reply_markup=keyboards.chara_keyboard)


@router.callback_query(F.data == "serious_tone")
async def serious_tone(callback: CallbackQuery):
    await callback.answer()
    await state.update_data({"tone": "Строгий"})
    await callback.message.edit_text(text="Какого характера у нас будет пост? Для каких целей мы его пишем?",
                                     reply_markup=keyboards.chara_keyboard)


@router.callback_query(F.data == "advert")
async def advert_chara(callback: CallbackQuery):
    await callback.answer()
    await state.update_data({"chara": "Рекламный"})
    await callback.message.edit_text(text="Так-с, все данные получены, дай мне секунду на подумать...",
                                     reply_markup=None)
    data = await state.get_data()
    await state.clear()
    face, tone, chara = data["face"], data["tone"], date["chara"]
    user_id = callback.from_user.id
    business_info, company_info, audio_info = HistoryFuncs.get_history(user_id)
    post_prompt = f"Создай 3 поста для телеграм бота для бизнеса с описанием {business_info}, основной продукт которого {company_info}. Также учитывай и целевую аудиторию бота, {audio_info}. Все посты пиши от '{face}', с {tone} тоном. Помимо этого, все посты должны иметь {chara} характер."
    post = await ask_gpt(post_prompt)
    await callback.message.edit_text(
        text=f"Держи посты! Можешь добавить их в отложенный постинг и прикрепить фотографии - подписчикам будет еще интереснее:\n{post}",
        reply_markup=keyboards.to_fmenu_from_choices_kb)


class InfoUser(StatesGroup):
    First = State()


@router.callback_query(F.data == "post_by_user")
async def post_by_user(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(
        text="Тогда напиши - о чем нужен пост, в каком стиле его написать, каким тоном говорить и в целом - буду рада, если сможешь мне излить душу в этом посте и выложить максимум вводных данных.",
        reply_markup=None)
    await state.set_state(InfoUser.First)


@router.message(InfoUser.First)
async def post_written(message: Message, state: FSMContext):
    await state.clear()
    msg = message.text
    usiness_info, company_info, audio_info = HistoryFuncs.get_history(user_id)
    post_prompt = f"Создай 3 поста для телеграм бота для бизнеса с описанием {business_info}, основной продукт которого {company_info}. Также учитывай и целевую аудиторию бота, {audio_info}. Учитывай пожелания пользователя: {msg}"
    post = await ask_gpt(post_prompt)
    await message.answer(
        text=f"Держи посты! Можешь добавить их в отложенный постинг и прикрепить фотографии - подписчикам будет еще интереснее:\n{post}")


@router.callback_query(F.data == "create_video")
async def create_video(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        text="Напиши, о чем хочешь сделать видео. Если планируешь видео больше чем на 30 минут, укажи примерное время")
    await state.set_state(Video.First)


class Video(StatesGroup):
    First = State()
    Second = State()


@router.message(Video.First)
async def about_video(message: Message, state: FSMContext):
    await state.update_data({'about': message.text})
    await message.edit_text(text="Теперь выбери среднюю длительность для видео", reply_markup=keyboards.video_length)


@router.callback_query(F.data == "short_video")
async def short_video(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data({'length': 'Короткое (5-10 минут)'})
    await state.set_state(None)
    await callback.message.edit_text(text="Все данные получены", reply_markup=keyboards.forward_video)


@router.callback_query(F.data == "average_video")
async def average_video(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data({'length': 'Среднее (15-20 минут)'})
    await state.set_state(None)
    await callback.message.edit_text(text="Все данные получены", reply_markup=keyboards.forward_video)


@router.callback_query(F.data == "long_video")
async def short_video(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data({'length': 'Длинное (25-30 минут)'})
    await state.set_state(None)
    await callback.message.edit_text(text="Все данные получены", reply_markup=keyboards.forward_video)


@router.callback_query(F.data == "forward_video")
async def forward_video(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    await state.clear()
    about, length = date['about'], date['length']
    video_prompt = f'Создай сценарий для видео длительностью {length}. Учитывай, что оно будет {about}. Везде указывай примерное время видео, чтобы пользователю было проще ориентироваться'
    video = await ask_gpt(video_prompt)
    await callback.message.edit_text(text=f"Вот, что у меня получилось:\n{video}",
                                     reply_markup=keyboards.to_fmenu_from_choices_kb)

@router.callback_query(F.data == "sales_assistance")
async def sales_assistance(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.answer(text="Сообщение 10", reply_markup=keyboard.sales_assistance)

class GPT_dialogue(StatesGroup):
    First = State()


@router.callback_query(F.data == "clear_data")
async def clear_data(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    if user_id in user_histories:
        del user_histories[user_id]
        await callback.message.answer(text="Контекст очищен!", reply_markup=keyboards.to_sales_menu)
    else:
        await callback.message.answer(text="История пуста!", reply_markup=keyboards.to_sales_menu)

@router.callback_query(F.data == "start_helper")
async def start_helper(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(text="Отправляйте сообщение. Если пожелаете закончить, напишите 'Закончить'")
    await state.set_state(GPT_dialogue.First)

user_histories = {}
SYSTEM_MESSAGE = {
    "role": "system",
    "content": """Ты - ассистент по продажам, тебя интегрируют в бота, который будет выполнять следующую функцию 
                            Я буду отправлять тебе сообщения своего клиента, а твоя задача - на них отвечать, чтобы выполнить какую-либо цель от диалога с клиентом. Мне пишут люди в мессенджер и мне нужно им ответить, тебе нужно представить, что ты продавец и придумывать за меня ответы и полностью вести диалог.
                            Тебе важно учесть следующие требования
                            1. Необходимо создавать ощущение, что диалог идет с человеком 
                            2. Ответы должны быть краткие, точные и меткие 
                            3. Не должно быть лишних слов 
                            4. Не надо сразу продавать лоб 
                            5. Нужно закрывать возражения и вести человека к покупке 
                            Тебе важно использовать знания из литературы и книг по маркетингу в том числе 
                            Сейчас я отправлю тебе информацию для создания контекста о своем бизнесе, чтобы получить максимум информации, задай мне уточняющие вопросы, когда вопросы будут окончены, напиши «отлично, теперь можешь прислать мне сообщение клиента"
                            """
}

@router.message(GPT_dialogue.First)
async def dialogue_with_GPT(message: Message):
    user_id = message.from_user.id
    msg = message.text
    if msg.lower() == "закончить":
        await message.answer(text="Прекращаем диалог", reply_markup=keyboards.to_sales_menu)
    if user_id not in user_histories:
        user_histories[user_id] = [SYSTEM_MESSAGE]

    user_histories[user_id].append({"role": "user", "content": user_input})

    response = await openai.ChatCompletion.acreate(
        model=config['model'],
        messages=user_histories[user_id]
    )

    bot_response = response.choices[0].message['content']
    user_histories[user_id].append({"role": "assistant", "content": bot_response})
    await message.answer(text=bot_response)



@router.callback_query(F.data == "create_lead_magnet")
async def create_lead_magnet(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(text="Желаете использовать старые ответы, или введете новые?", reply_markup=keyboards.restart_keyboard_magnet)

class RestartQuestionsMagnet(StatesGroup):
    First = State()
    Second = State()
    Third = State()


@router.callback_query(F.data == "restart_questions_magnet")
async def restart_questions_magnet(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text=texts.message1_1)
    await state.set_state(RestartQuestionsMagnet.First)


@router.message(RestartQuestionsMagnet.First)
async def first_restarted_answer(message: Message, state: FSMContext):
    await state.update_data({"business": message.text})
    await message.answer(text=texts.message2)
    await state.set_state(RestartQuestionsMagnet.Second)


@router.message(RestartQuestionsMagnet.Second)
async def second_restarted_answer(message: Message, state: FSMContext):
    await state.update_data({"company": message.text})
    await message.answer(text=texts.message3)
    await state.set_state(RestartQuestionsMagnet.Third)


@router.message(RestartQuestionsMagnet.Third)
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
        marketing_strategy_plan="",
        lead_magnet="",
        pinned_post="",
        content_plan="",
    )
    if HistoryFuncs.user_in_database(user_id):
        HistoryFuncs.edit_history(id=user_id, new_business=business, new_company=company, new_audience=audience)
    else:
        HistoryFuncs.add_new_user(query)
    logging.info(f"История пользователя '{user_id}' сохранена.")
    await message.answer(
        text="Мне надо некоторое время на подумать, подождите пожалуйста пару минут",
        reply_markup=keyboards.continue_magnet)

@router.callback_query(F.data == "magnet_results")
async def magnet_results(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    business_info, company_info, audience_info = HistoryFuncs.get_history(user_id)
    marketing_strategy_plan_response = HistoryFuncs.get_gpt_history(user_id)[1]
    lead_magnet_prompt = f"Придумай 5 идей лид-магнитов для телеграм канала и бизнеса в целом. Распиши подробно каждый лид-магнит в 15 тезисов. Учти описание проекта - {business_info}. Учти также описание его аудитории - {audience_info}. И воспользуйся информацией о продуктах - {company_info}. Также вопсользуйся следующей информацией про маркетинг проекта - {marketing_strategy_plan_response}. Пиши на русском языке. Не давай каких-либо комментариев."
    lead_magnet = await ask_gpt(lead_magnet_prompt)
    HistoryFuncs.change_magnet(user_id, lead_magnet)
    await callback.message.answer(text=f"{lead_magnet}\n\nОтлично! Вот мои идеи - рекомендую сделать кнопку с возможность открыть твой материал в закрепленном посте (его я отправлю тебе следом) или же поставить кнопку на твой аккаунт, чтобы люди могли написать тебе напрямую 📱⚙", reply_markup=keyboards.to_fmenu_from_choices_kb)

@router.callback_query(F.data == "continue_questions_magnet")
async def continue_questions_magnet(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    lead_magnet = HistoryFuncs.get_gpt_history(user_id)[2]
    await callback.message.answer(text=f"{lead_magnet}\n\nОтлично! Вот мои идеи - рекомендую сделать кнопку с возможность открыть твой материал в закрепленном посте (его я отправлю тебе следом) или же поставить кнопку на твой аккаунт, чтобы люди могли написать тебе напрямую 📱⚙", reply_markup=keyboards.to_fmenu_from_choices_kb)


