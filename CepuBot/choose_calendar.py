from db import get_existing_user_group
import db

calendar_IDs = {'И-1-18': 'n29cccq1b6ddm24p92uuphv3f4@group.calendar.google.com',
                'И-2-18': 'eo7t3oqllbr2n38k7o649ghst4@group.calendar.google.com'}
calendarID = ''


def get_calendar_id(message):
    global calendarID
    us_id = message.from_user.id
    get_existing_user_group(user_id=us_id)

    for key in calendar_IDs:
        if key == db.user_group:
            calendarID = calendar_IDs.get(key)
            print(calendarID)
