import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build

import choose_calendar
from bot_connect import bot
from choose_calendar import get_calendar_id
import locale
locale.setlocale(locale.LC_ALL, "")

scopes = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']
credentials = None
service = None
events = []
timeMin = None
timeMax = None

event_summary = ''
summary = ''
description = ''
start_lesson_time: str = ''
end_lesson_time: str = ''
today = None
tomorrow = None


def connect(message):
    global credentials
    global service

    get_calendar_id(message)
    credentials = service_account.Credentials.from_service_account_file('cepu-bot.json')


def get_closest_lesson(message):
    global service
    global events
    global timeMin
    global timeMax
    global event_summary
    global summary
    global description
    global start_lesson_time
    global end_lesson_time

    service = build("calendar", "v3", credentials=credentials)
    timeMin = datetime.datetime.utcnow().isoformat() + 'Z'
    timeMax = timeMin[0:10] + "T17:00:00.000000Z"

    events = service.events().list(calendarId=choose_calendar.calendarID,
                                   timeMin=timeMin, timeMax=timeMax, singleEvents=True, orderBy='startTime').execute()

    event_summary = events['summary']
    summary = events['items'][0]['summary']
    description = events['items'][0]['description']
    pre_start_time = events['items'][0]['start']['dateTime']
    pre_end_time = events['items'][0]['end']['dateTime']
    start_lesson_time = pre_start_time[11:16]
    end_lesson_time = pre_end_time[11:16]

    print('calendar for:', event_summary, '\n',
          'summary:', summary, "\n",
          'description:', description, '\n',
          'start:', start_lesson_time, '\n',
          'end: ', end_lesson_time)

    bot.send_message(message.chat.id, f'{summary} \n '
                                      f'{description} \n '
                                      f'Начало: {start_lesson_time} \n '
                                      f'Конец: {end_lesson_time}')


def get_today_lessons(message):
    global service
    global events
    global timeMin
    global timeMax
    global event_summary
    global summary
    global description
    global start_lesson_time
    global end_lesson_time

    service = build("calendar", "v3", credentials=credentials)
    timeMin = datetime.date.today().isoformat() + "T06:20:00.000000Z"
    timeMax = timeMin[0:10] + "T17:00:00.000000Z"
    events = service.events().list(calendarId=choose_calendar.calendarID,
                                   timeMin=timeMin, timeMax=timeMax).execute()

    for i in range(len(events['items']) - 1):
        if events['items'][i]['start']['dateTime'] > events['items'][i + 1]['start']['dateTime']:
            events['items'][i], events['items'][i + 1] = events['items'][i + 1], events['items'][i]

    if len(events['items']) != 0:
        print('today')
        for i in range(len(events['items'])):
            event_summary = events['summary']
            summary = events['items'][i]['summary']
            description = events['items'][i]['description']
            pre_start_time = events['items'][i]['start']['dateTime']
            pre_end_time = events['items'][i]['end']['dateTime']
            start_lesson_time = pre_start_time[11:16]
            end_lesson_time = pre_end_time[11:16]

            print('calendar for:', event_summary, '\n',
                  'summary:', summary, "\n",
                  'description:', description, '\n',
                  'start:', start_lesson_time, '\n',
                  'end: ', end_lesson_time)

            bot.send_message(message.chat.id, f'{summary} \n '
                                              f'{description} \n '
                                              f'Начало: {start_lesson_time} \n '
                                              f'Конец: {end_lesson_time}')
    elif len(events['items']) == 0:
        bot.send_message(message.chat.id, "Отсутствует")


def get_tomorrow_lessons(message):
    global service
    global events
    global timeMin
    global timeMax
    global event_summary
    global summary
    global description
    global start_lesson_time
    global end_lesson_time

    service = build("calendar", "v3", credentials=credentials)
    next_day = datetime.date.today() + datetime.timedelta(days=1)

    timeMin = next_day.isoformat() + "T06:20:00.000000Z"
    timeMax = timeMin[0:10] + "T17:00:00.000000Z"
    events = service.events().list(calendarId=choose_calendar.calendarID,
                                   timeMin=timeMin, timeMax=timeMax).execute()

    for i in range(len(events['items']) - 1):
        if events['items'][i]['start']['dateTime'] > events['items'][i + 1]['start']['dateTime']:
            events['items'][i], events['items'][i + 1] = events['items'][i + 1], events['items'][i]

    if len(events['items']) != 0:
        print('tomorrow')
        for i in range(len(events['items'])):
            event_summary = events['summary']
            summary = events['items'][i]['summary']
            description = events['items'][i]['description']
            pre_start_time = events['items'][i]['start']['dateTime']
            pre_end_time = events['items'][i]['end']['dateTime']
            start_lesson_time = pre_start_time[11:16]
            end_lesson_time = pre_end_time[11:16]

            print('calendar for:', event_summary, '\n',
                  'summary:', summary, "\n",
                  'description:', description, '\n',
                  'start:', start_lesson_time, '\n',
                  'end: ', end_lesson_time)

            bot.send_message(message.chat.id, f'{summary} \n '
                                              f'{description} \n '
                                              f'Начало: {start_lesson_time} \n '
                                              f'Конец: {end_lesson_time}')
    else:
        bot.send_message(message.chat.id, "Отсутствует")


def get_valid_date():
    global today
    global tomorrow

    today = datetime.date.today().strftime("%d %b")

    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    tomorrow = tomorrow.strftime("%d %b")
