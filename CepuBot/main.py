from telebot import types


import connect_google_api
import news

from bot_connect import bot
from all_infos import vacancies_info, jobs_info, internship_info, \
    courses_info, library_info, association_info, site_info

from db import get_existing_user_department, get_existing_user_group, \
    create_pre_user, update_user_department, update_user_group, update_user_name, get_existing_user, \
    update_user_second_name, update_user_third_name, get_existing_student
import db

check_valid = False


@bot.message_handler(commands=['start', 'help'])
def hello_screen(message):

    try:
        connect_google_api.connect(message)
        print(db.user_group)
    except:
        pass

    us_id = message.from_user.id

    try:
        get_existing_user(user_id=us_id)
        print('user joined', us_id, db.user_name)
    except:
        # create_pre_user(user_id=us_id, fio=fio)
        create_pre_user(user_id=us_id)
        print('user created', us_id)

    try:
        get_existing_user_group(user_id=us_id)
    except:
        pass

    try:
        get_existing_user_department(user_id=us_id)
    except:
        pass

    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item_signUp = types.KeyboardButton("Регистрация")
    item_get_all_news = types.KeyboardButton("Последние новости университета")

    item_schedule = types.KeyboardButton("Расписание")
    item_vacancies = types.KeyboardButton("Вакантные места")
    item_jobs = types.KeyboardButton("Трудоустройство")
    item_internship = types.KeyboardButton("Профстажировки 2.0")
    item_courses = types.KeyboardButton("Кружковая работа")
    item_library = types.KeyboardButton("Библиотека")
    item_association = types.KeyboardButton("СНО")
    item_site = types.KeyboardButton("Дистанционное обучение")

    keyboard.add(item_schedule)
    keyboard.add(item_get_all_news)
    keyboard.add(item_jobs, item_vacancies, item_internship)
    keyboard.add(item_courses, item_library, item_association, item_site, item_signUp)

    if db.user_name is not None:
        bot.send_message(message.chat.id, f"Здравствуйте {db.user_name}! \n"
                                          "Вас приветствует информационный чат-бот КИПУ им. Февзи Якубова, "
                                          "который поможет вам узнать различную информаию, "
                                          "будет держать в курсе последних новостей университета, "
                                          "а также предоставит персональное расписание занятий.",
                         reply_markup=keyboard)
        db.user_name = ''
    else:
        bot.send_message(message.chat.id, "Здравствуйте! \n"
                                          "Вас приветствует информационный чат-бот КИПУ им. Февзи Якубова, "
                                          "который поможет вам узнать различную информаию, "
                                          "будет держать в курсе последних новостей университета, "
                                          "а также предоставит персональное расписание занятий.",
                         reply_markup=keyboard)


# раздел регистрации пользователя
def registration(message):
    reg_keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    item_name = types.KeyboardButton("Ввести ФИО")
    item_group = types.KeyboardButton("Ввести группу")
    item_faculty = types.KeyboardButton("Ввести кафедру")
    item_go_back = types.KeyboardButton("Закончить регистрацию")

    reg_keyboard.add(item_name, item_group, item_faculty, item_go_back)
    bot.send_message(message.chat.id, "Пожалуйста, введите информацию о себе\n"
                                      "(прим. Регистрация только для студентов ВУЗа)", reply_markup=reg_keyboard)


# запись имени пользователя в БД
def get_student_name(message):
    if message.text == "Продолжить заполнение ФИО":
        enter_fio(message)
    else:
        name = message.text
        us_id = message.from_user.id

        update_user_name(name=name, user_id=us_id)

        bot.send_message(message.chat.id, f"Ваше имя будет {message.text}")
        get_existing_user(user_id=us_id)
        enter_fio(message)


# запись фамилии пользователя в БД
def get_student_second_name(message):
    if message.text == "Продолжить заполнение ФИО":
        enter_fio(message)
    else:
        second_name = message.text
        us_id = message.from_user.id

        update_user_second_name(second_name=second_name, user_id=us_id)

        bot.send_message(message.chat.id, f"Ваша фамилия будет {message.text}")
        get_existing_user(user_id=us_id)
        enter_fio(message)


# запись отчества пользователя в БД
def get_student_third_name(message):
    if message.text == "Продолжить заполнение ФИО":
        enter_fio(message)
    else:
        third_name = message.text
        us_id = message.from_user.id

        update_user_third_name(third_name=third_name, user_id=us_id)

        bot.send_message(message.chat.id, f"Ваше отчество будет {message.text}")
        get_existing_user(user_id=us_id)
        enter_fio(message)


# запись группы пользователя в БД
def get_student_group(message):
    if message.text == "Продолжить заполнение персональных данных":
        registration(message)
    else:
        group = message.text
        us_id = message.from_user.id

        update_user_group(group=group, user_id=us_id)

        bot.send_message(message.chat.id, f"Вы выбрали группу {message.text}")
        registration(message)


# запись факультета пользователя в БД
def get_student_department(message):
    if message.text == "Продолжить заполнение персональных данных":
        registration(message)
    else:
        department = message.text
        us_id = message.from_user.id

        update_user_department(department=department, user_id=us_id)

        bot.send_message(message.chat.id, f"Вы выбрали кафедру {message.text}")
        registration(message)


# реализовать рассылку расписания с помощью яндекс.календарь API
def schedule_select(message):
    schedule_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item_today = types.KeyboardButton("Расписание на сегодня")
    item_tomorrow = types.KeyboardButton("Расписание на завтра")
    item_next = types.KeyboardButton("Следующая пара")
    item_go_back = types.KeyboardButton("На главную")

    schedule_kb.add(item_next)
    schedule_kb.add(item_today, item_tomorrow)
    schedule_kb.add(item_go_back)
    bot.send_message(message.chat.id, "Какое расписание вас интересует?", reply_markup=schedule_kb)


def enter_fio(message):
    name_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item_set_name = types.KeyboardButton("Ввести имя")
    item_set_second_name = types.KeyboardButton("Ввести фамилию")
    item_set_third_name = types.KeyboardButton("Ввести отчество")
    item_go_back = types.KeyboardButton("Продолжить заполнение персональных данных")

    name_kb.add(item_set_second_name, item_set_name, item_set_third_name)
    name_kb.add(item_go_back)

    # bot.register_next_step_handler(message, get_student_fio)

    bot.send_message(message.chat.id, 'С чего начнем?', reply_markup=name_kb)


# проверка существования студента
def check_user(message):
    global check_valid
    id_us = message.from_user.id
    get_existing_user(user_id=id_us)
    get_existing_student(name=db.user_name, second_name=db.user_second_name, third_name=db.user_third_name,
                         group=db.user_group, department=db.user_department)

    bot.send_message(message.chat.id, f"{db.reply_to_user}")
    if db.check_param:
        update_user_name(db.student_name, id_us)
        update_user_second_name(db.student_second_name, id_us)
        update_user_third_name(db.student_third_name, id_us)
        update_user_group(db.student_group, id_us)
        update_user_department(db.student_department, id_us)
        check_valid = True
    else:
        check_valid = False


@bot.message_handler(content_types=['text'])
def reg_handle(message):
    if message.text == "Регистрация":
        registration(message)

    elif message.text == "Расписание":
        schedule_select(message)

    elif message.text == "Вакантные места":
        vacancies_info(message)

    elif message.text == "Трудоустройство":
        jobs_info(message)

    elif message.text == "Профстажировки 2.0":
        internship_info(message)

    elif message.text == "Кружковая работа":
        courses_info(message)

    elif message.text == "Библиотека":
        library_info(message)

    elif message.text == "СНО":
        association_info(message)

    elif message.text == "Дистанционное обучение":
        site_info(message)

    elif message.text == "Ввести ФИО":
        enter_fio(message)

    elif message.text == "Ввести имя":
        name_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

        item_go_back = types.KeyboardButton("Продолжить заполнение ФИО")

        name_kb.add(item_go_back)
        bot.send_message(message.chat.id, 'Введите имя', reply_markup=name_kb)
        bot.register_next_step_handler(message, get_student_name)

    elif message.text == "Ввести фамилию":
        name_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

        item_go_back = types.KeyboardButton("Продолжить заполнение ФИО")

        name_kb.add(item_go_back)
        bot.send_message(message.chat.id, 'Введите фамилию', reply_markup=name_kb)
        bot.register_next_step_handler(message, get_student_second_name)

    elif message.text == "Ввести отчество":
        name_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

        item_go_back = types.KeyboardButton("Продолжить заполнение ФИО")

        name_kb.add(item_go_back)
        bot.send_message(message.chat.id, 'Введите отчество', reply_markup=name_kb)
        bot.register_next_step_handler(message, get_student_third_name)

    elif message.text == "Ввести группу":
        group_kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        item_go_back = types.KeyboardButton("Продолжить заполнение персональных данных")

        group_kb.add(item_go_back)

        bot.send_message(message.chat.id, "Введите название группы, к которой вы принадлежите\n"
                                          "(формат группы должен соответствовать примеру: И-1-18)",
                         reply_markup=group_kb)
        bot.register_next_step_handler(message, get_student_group)

    elif message.text == "Ввести кафедру":
        department_kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        item_go_back = types.KeyboardButton("Продолжить заполнение персональных данных")

        department_kb.add(item_go_back)
        bot.send_message(message.chat.id, "Введите кафедру, на которой вы обучаетесь", reply_markup=department_kb)

        bot.register_next_step_handler(message, get_student_department)

    elif message.text == "Продолжить заполнение персональных данных":
        registration(message)

    elif message.text == "Продолжить заполнение ФИО":
        enter_fio(message)

    elif message.text == "На главную":
        hello_screen(message)

    elif message.text == "Расписание на сегодня":
        if check_valid:
            if db.user_group is not None:
                connect_google_api.get_valid_date()
                bot.send_message(message.chat.id, f"Расписание на {connect_google_api.today} для группы {db.user_group}")
                try:
                    connect_google_api.get_today_lessons(message)
                except:
                    bot.send_message(message.chat.id, "Отсутствует")
            else:
                bot.send_message(message.chat.id, "Не выбрана группа")
        else:
            bot.send_message(message.chat.id, "Пользователь не зарегистрирован")

    elif message.text == "Расписание на завтра":
        if check_valid:
            if db.user_group is not None:
                connect_google_api.get_valid_date()
                bot.send_message(message.chat.id, f"Расписание на {connect_google_api.tomorrow} "
                                                  f"для группы {db.user_group}")
                try:
                    connect_google_api.get_tomorrow_lessons(message)
                except:
                    bot.send_message(message.chat.id, "Отсутствует")
            else:
                bot.send_message(message.chat.id, "Не выбрана группа")
        else:
            bot.send_message(message.chat.id, "Пользователь не зарегистрирован")

    elif message.text == "Следующая пара":
        if check_valid:
            if db.user_group is not None:
                bot.send_message(message.chat.id, f"Следующая пара для группы {db.user_group}")
                try:
                    connect_google_api.get_closest_lesson(message)
                except:
                    bot.send_message(message.chat.id, "Отсутствует")
            else:
                bot.send_message(message.chat.id, "Не выбрана группа")
        else:
            bot.send_message(message.chat.id, "Пользователь не зарегистрирован")

    elif message.text == 'Последние новости университета':
        news.get_all_news(message)

    elif message.text == 'Закончить регистрацию':
        check_user(message)
        hello_screen(message)


bot.infinity_polling()

