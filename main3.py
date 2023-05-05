# Импортируем необходимые классы.
import aiohttp
import main
import logging
import datetime
from telegram.ext import Application, MessageHandler, ConversationHandler, filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from random import randint
from data.geocode import get_ll_span
from main import start_

# Запускаем логгирование

name = ""
spis_facult = ["1", "2", "3"]
spis_vyz = main.get_all_university()
spis_need_olymp = ["Всерос"]
spis_olymp = main.get_all_olymp()

error_DB = "ERROR. Database not available. Please, write about this Exception to the number 89151771271"
# ссылка на группу с нами под названием developers
reply_keyboard_MAIN = [['/USER', '/add', '/lists'],
                       ['/help', '/start', '/all']]
markup_MAIN = ReplyKeyboardMarkup(reply_keyboard_MAIN, one_time_keyboard=False)

reply_keyboard_SPIC = [['/spic_VYZ', '/spic_OLYMP'],
                       ['/help_SPIC', '/main']]
markup_SPIC = ReplyKeyboardMarkup(reply_keyboard_SPIC, one_time_keyboard=False)

reply_keyboard_USER = [['/change_DELTA', '/change_NAME'],
                       ['/help_USER', '/main']]
markup_USER = ReplyKeyboardMarkup(reply_keyboard_USER, one_time_keyboard=False)

reply_keyboard_ADD = [['/spic_VYZ', '/spic_OLYMP'],
                      ['/add_VYZ', '/find_VYZ', "/add_OLYMP", "/del_OLYMP"],
                      ['/help_ADD', '/main']]
markup_ADD = ReplyKeyboardMarkup(reply_keyboard_ADD, one_time_keyboard=False)

reply_keyboard_ALL = [['/help_all'],
                      ['/USER', '/add', '/lists'],
                      ['/help', '/start', '/all'],
                      ['/spic_VYZ', '/spic_OLYMP', '/help_SPIC'],
                      ['/change_DELTA', '/stop', '/help_USER'],
                      ['/add_VYZ', '/add_olymp', '/help_ADD'],
                      ['/main']]
markup_ALL = ReplyKeyboardMarkup(reply_keyboard_ALL, one_time_keyboard=False)


async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет, {user.mention_html()}!",
        reply_markup=markup_MAIN
    )
    start_(user)


def get_spic_olymp(key):
    '''ЗДЕСЬ НЕОБХОДИМО В ЗАВИСИМОСТИ ОТ key ВЫДАТЬ СПИСОК ВСЕХ НАЗВАНИЙ ОЛИМПИАД'''
    if key == "all":
        # return list(something)
        # ["Олимпиада 1", "...."]
        pass
    elif key == "test":
        return error_DB
    else:
        '''иначе мы 100% должны получить в качестве параметра название вуза и уже по нему выдать олимпиады (от этого)/(нужные этому) вуза/у'''
        # return list(something)
        pass


def get_spic_VYZ(key):
    pass


async def _help_(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"""Привет, {user.mention_html()}! Я бот, который сможет помочь тебе поступить в ВУЗ в Москве. Используя команды на панели вы сможете: 
        1) Узнать больше о ВУЗах Москвы
        2) Выбрать один из них и стремиться к тому, чтобы 
            поступить в него
        3) Следить за личными достижениями и расписанием олимпиад""")


async def help_ADD(update, context):
    await update.message.reply_html(
        rf"""📚 Здесь вы можете изменить выбранный вуз: /set_VYZ

        Помните - изменить свой выбор можно всегда!

        Также мы собрали список всех ВУЗов Москвы,
         который Вы можете посмотреть по команде /spic_VYZ! 🎓""")


async def help_SPIC(update, context):
    await update.message.reply_html(
        rf"""🏫 По команде /spic_VYZ Вы сможете увидеть список всех ВУЗов Москвы, в будущем это может пригодиться для выбора одного из них.
👨‍🎓 А использовав /spic_OLYMP можно получить аналогичный список олимпиад""")


async def help_USER(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf'''🚩 {user.mention_html()}, это Ваше личное Лобби, где можно узнать о личных достижениях, выбранном вузе, изменить свой ник и изменить время между "напоминалками"''')


async def help_SET(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf'''⌛ Команды /set_OLYMP и /change_DELTA
Помогают соответсвенно выбрать внеурочную олимпиаду и поставить на нее напоминание, а также изменить время между "напоминалками"''')


async def help_all(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf'''🤔 {user.mention_html()}, если ты забыл/а о значении какой либо кнопке, либо же ты тут в первый раз, то раздел ALL создан для тебя!
В нашем боте существует 4 основных раздела и один дополнительный:
    ~ /MAIN - основной, главный раздел
    ~ /USER - отвечает за всю информацию о тебе и твоих установленных олимпиадах, вузах и напоминалках
    ~ /add - отвечает за добавление новых ВУЗов и олимпиад в раздел целей
    ~ /lists - отвечает за показ всех доступных в боте ВУЗов и олимпиад
    дополнительный раздел - 
    ~ /all - раздел со всеми кнопками

❗ПОДРОБНЕЕ О РАЗДЕЛАХ МОЖНО УЗНАТЬ, ПЕРЕЙДЯ В НИХ И ВЫБРАВ КОМАНДУ ТИПА /help_(название раздела)❗
Команды:
    ~ /help - выводит информацию о боте (находится в MAIN)
    ~ /start - запускает бота
    ~ /spic_VYZ - выводит список всех ВУЗов, существующих в БД
    ~ /spic_OLYMP - выводит список всех олимпиад, существующих в БД
    ~ /change_DELTA - изменение времени, за которое нужно предупредить о предстоящей олимпиаде
    ~ /add_VYZ - добавляет ВУЗ в раздел целей
    ~ /add_OLYMP - добавляет олимпиаду в раздел целей
''')


async def stop(update, context):
    await update.message.reply_html("Stop")


async def _main_(update, context):
    await update.message.reply_html(
        rf"Загрузка ...",
        reply_markup=markup_MAIN
    )


# --------------------------------------------------------------------------------------------------
async def find_VYZ(update, context):
    await update.message.reply_html("Напиши адрес вуза и увидишь его местоположение")
    return 1


async def geocoder(update, context):
    try:
        geocoder_uri = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode="
        response = await get_response(geocoder_uri + update.message.text + "&format=json")

        toponym = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        print(toponym)
        ll, spn = get_ll_span(toponym)
        # Можно воспользоваться готовой функцией,
        # которую предлагалось сделать на уроках, посвящённых HTTP-геокодеру.

        static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=map"
        await context.bot.send_photo(
            update.message.chat_id,  # Идентификатор чата. Куда посылать картинку.
            # Ссылка на static API, по сути, ссылка на картинку.
            # Телеграму можно передать прямо её, не скачивая предварительно карту.
            static_api_request,
            caption="Нашёл:"
        )
    except Exception:
        pass
    return ConversationHandler.END


async def get_response(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()


async def add_OLYMP(update, context):
    await update.message.reply_text("Напиши олимпиаду, в которой хочешь участвовать")
    return 1


async def add_OLYMP_2(update, context):
    olymp = update.message.text
    if olymp in spis_olymp:
        main.add_olymp(olymp, 1, 1, 1, "")
        if olymp not in spis_need_olymp:
            await update.message.reply_text(
                "Добавлена олимпиада, не влияющая на поступление в нужный вуз. Чтобы удалить её, нажми /del_OLYMP, чтобы поставить напоминание, нажми /change_DELTA")
        else:
            await update.message.reply_text(
                "Добавлена нужная тебе олимпиада. Чтобы удалить её, нажми /del_OLYMP, чтобы поставить напоминание, нажми /change_DELTA")
        return ConversationHandler.END
    else:
        await update.message.reply_text(
            "К сожалению, бот не знает о такой олимпиаде. Посмотри список олимпиад, нажав /spis_OLYMP")
        return ConversationHandler.END


# ------------------------------------------------------------------------------

async def del_OLYMP(update, context):
    await update.message.reply_text("Напиши олимпиаду, которую ХОЧЕШЬ УДАЛИТЬ")
    return 1


async def del_OLYMP_2(update, context):
    olymp = update.message.text
    if olymp in spis_olymp:
        main.user_olymp_delete(olymp, cur_user=update.effective_user)
        if olymp not in spis_need_olymp:
            await update.message.reply_text(
                "Удалена олимпиада, не влияющая на поступление в нужный вуз. Чтобы добавить её, нажми /add_OLYMP")
        else:
            await update.message.reply_text(
                "Удалена нужная тебе олимпиада. Чтобы добавить её, нажми /add_OLYMP, чтобы поставить напоминание, нажми /change_DELTA")
        return ConversationHandler.END
    else:
        await update.message.reply_text(
            "К сожалению, бот не знает о такой олимпиаде. Посмотри список олимпиад, нажав /spis_OLYMP")
        return ConversationHandler.END


async def del_VYZ(update, context):
    await update.message.reply_text("Напиши вуз, который хочешь удалить")
    return 1


async def del_VYZ_2(update, context):
    global vyz
    vyz = update.message.text
    if vyz in spis_vyz:
        main.user_university_delete(vyz, cur_user=update.effective_user)
        await update.message.reply_text(
            "Отлично! Ты можешь написать факультет, который хочешь удалить, или нажать /stop")
        return 2

    else:
        await update.message.reply_text(
            "К сожалению, бот не знает о таком вузе. Посмотри список вузов, нажав на /spic_VYZ. ")
        return ConversationHandler.END


# ------------------------------------------------------------------------------

async def add_VYZ(update, context):
    await update.message.reply_text("Напиши вуз, в который хочешь поступить и в скобках факультет")
    return 1


async def add_VYZ_2(update, context):
    global vyz
    vyz = update.message.text
    if vyz.split("(")[0] in spis_vyz:
        main.user_university_add(vyz, cur_user=update.effective_user)
        await update.message.reply_text(
            "Отлично! Теперь факультет вуза добавлен")
        return ConversationHandler.END

    else:
        await update.message.reply_text(
            "К сожалению, бот не знает о таком вузе. Посмотри список вузов, нажав на /spic_VYZ. ")
        return ConversationHandler.END


async def add_VYZ_3(update, context):
    await update.message.reply_text(
        "Теперь ты можешь посмотреть олимпиады для выбранных тобой факультетов, нажав /spis_need_olymp")
    return ConversationHandler.END


# ------------------------------------------------------------------------------

async def change_DELTA(update, context):
    await update.message.reply_text(
        "Напиши название олимпиады, восклицательный знак и время, в которое нужно о ней напомнить")
    return 0


async def change_DELTA_2(update, context):
    # В разработке
    await update.message.reply_text("В разработке!")
    return ConversationHandler.END


# ------------------------------------------------------------------------------


async def spic_VYZ(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"{user.mention_html()}, ожидайте. Сейчас я выведу список всех ВУЗов ниже:",
    )
    await update.message.reply_html(rf'{main.get_all_university()}')


async def spic_OLYMP(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"{user.mention_html()}, ожидайте. Сейчас я выведу список всех будущих олимпиад ниже:",
    )
    await update.message.reply_html(rf'{main.get_all_olymp()}')


async def add(update, context):
    await update.message.reply_html(
        rf"Загрузка ...",
        reply_markup=markup_ADD
    )


async def lists(update, context):
    await update.message.reply_html(
        rf"Загрузка ...",
        reply_markup=markup_SPIC
    )


async def _all_(update, context):
    await update.message.reply_html(
        rf"Загрузка ...",
        reply_markup=markup_ALL
    )
    await update.message.reply_html(
        rf"📚 Здесь находятся все доступные команды, узнать о значении которых ты можешь по команде /help_all"
    )


async def USER(update, context):
    await update.message.reply_html(
        rf"Загрузка ...",
        reply_markup=markup_USER
    )


def main1():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token("6015537560:AAGF7yrC-4QnR4DtbFh78GplDpMD1YDqSt4").build()

    application.add_handler(CommandHandler("help", _help_))
    application.add_handler(CommandHandler("help_ADD", help_ADD))
    application.add_handler(CommandHandler("help_SPIC", help_SPIC))
    application.add_handler(CommandHandler("help_USER", help_USER))
    application.add_handler(CommandHandler("help_SET", help_SET))
    application.add_handler(CommandHandler("help_all", help_all))

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("main", _main_))
    application.add_handler(CommandHandler("lists", lists))
    application.add_handler(CommandHandler("all", _all_))

    # application.add_handler(CommandHandler("add_OLYMP", add_OLYMP))
    # application.add_handler(CommandHandler("add_VYZ", add_VYZ))

    # application.add_handler(CommandHandler("add_VYZ", change_VYZ))
    # application.add_handler(CommandHandler("change_DELTA", change_DELTA))
    # application.add_handler(CommandHandler("change_NAME", change_NAME))

    application.add_handler(CommandHandler("spic_VYZ", spic_VYZ))
    application.add_handler(CommandHandler("spic_OLYMP", spic_OLYMP))

    application.add_handler(CommandHandler("USER", USER))

    conv1 = ConversationHandler(
        entry_points=[CommandHandler('change_DELTA', change_DELTA)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, change_DELTA_2)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv1)

    conv2 = ConversationHandler(
        entry_points=[CommandHandler('add_VYZ', add_VYZ)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_VYZ_2)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv2)

    conv3 = ConversationHandler(
        entry_points=[CommandHandler('del_OLYMP', del_OLYMP)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, del_OLYMP_2)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv3)

    conv4 = ConversationHandler(
        entry_points=[CommandHandler('add_OLYMP', add_OLYMP)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_OLYMP_2)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv4)

    conv5 = ConversationHandler(
        entry_points=[CommandHandler('find_VYZ', find_VYZ)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, geocoder)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv5)

    # Запускаем приложение.
    application.run_polling()
