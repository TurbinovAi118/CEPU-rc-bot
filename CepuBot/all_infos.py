from bot_connect import bot
from telebot import types


def vacancies_info(message):
    bot.send_message(message.chat.id, 'Список вакантных мест для приема/перевода обучающихся можно найти по [ссылке]'
                                      '(https://kipu-rc.ru/student/vakantnye-mesta-priema-perevoda.html)',
                     parse_mode='Markdown')


def jobs_info(message):
    jobs_inline_kb = types.InlineKeyboardMarkup(row_width=1)

    item_allocation_info = types.InlineKeyboardButton(text="Распределение и трудоустройство выпускников",
                                                      url="https://kipu-rc.ru/student/"
                                                          "trudoustrojstvo/397-svedeniya-o-raspredelenii"
                                                          "-i-trudoustrojstve-vypusknikov.html")

    item_jobs_info = types.InlineKeyboardButton(text="Трудоустройство для обучающихся и выпускников",
                                                url="https://kipu-rc.ru/student/trudoustrojstvo/"
                                                    "291-obuchayushchimsya-i-vypusknikam.html")

    item_documents = types.InlineKeyboardButton(text="Нормативно правовая база по трудоустройству студентов",
                                                url="https://kipu-rc.ru/student/trudoustrojstvo/"
                                                    "289-informatsiya-po-trudoustrojstvu.html")

    item_vacancies = types.InlineKeyboardButton(text="Вакансии рабочих мест",
                                                url="https://kipu-rc.ru/student/trudoustrojstvo/"
                                                    "231-informatsiya-po-trudoustroj.html")

    jobs_inline_kb.add(item_allocation_info, item_jobs_info, item_documents, item_vacancies)
    bot.send_message(message.chat.id, "В данном разделе представлена вся интересующая вас информация, касающаяся "
                                      "трудоустройства студентов и выпускников", reply_markup=jobs_inline_kb)


def internship_info(message):
    bot.send_message(message.chat.id, '«Профстажировки 2.0» – это социальный лифт для студента. '
                                      'Курсовая или диплом становится пропуском на стажировку в '
                                      'компанию мечты и шансом трудоустроиться. '
                                      'Участвуя в проекте, вузы и учреждения СПО могут '
                                      'значительно расширить информационную базу для '
                                      'выполнения курсовых и выпускных квалификационных работ обучающихся, '
                                      'а также установить новые партнерские контакты с крупнейшими работодателями. '
                                      'Более подробная информация представлена по [ссылке]'
                                      '(https://kipu-rc.ru/student/profstazhirovki.html)',
                     parse_mode='Markdown')


def courses_info(message):
    bot.send_message(message.chat.id, 'Вся информация, касающаяся кружковой деятельности представлена по [ссылке]'
                                      '(https://kipu-rc.ru/student/krujkovaya-rabota.html)',
                     parse_mode='Markdown')


def library_info(message):
    bot.send_message(message.chat.id, 'Электронная библиотека находится [тут]'
                                      '(http://www.cepulib.ru/index.php/ru/)',
                     parse_mode='Markdown')


def association_info(message):
    bot.send_message(message.chat.id, 'Cтуденческое научное объединение (СНО) – '
                                      'это внутривузовская общественная организация, '
                                      'созданная по инициативе обучающихся КИПУ имени Февзи Якубова, '
                                      'объединяющая на добровольной основе студентов '
                                      'активно участвующих в научно-исследовательской, '
                                      'инновационной и научно-просветительской работе. '
                                      'Более подробную информацию можно найти по [ссылке]'
                                      '(https://kipu-rc.ru/student/studencheskoe-nauchnoe-ob-edinenie.html)',
                     parse_mode='Markdown')


def site_info(message):
    bot.send_message(message.chat.id, 'Сайт дистанционного обучения находится [тут]'
                                      '(e.kipu-rc.ru/)', parse_mode='Markdown')
