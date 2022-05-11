# from main import registration
import sqlite3

conn = sqlite3.connect('db/cepuDB.db', check_same_thread=False)
cursor = conn.cursor()

user_name = ""
user_second_name = ""
user_third_name = ""
user_group = ""
user_department = ""

student_name = ""
student_second_name = ""
student_third_name = ""
student_group = ""
student_department = ""

reply_to_user = "Студент не найден, дополните недостающую/исправьте настояющую персональную информацию. \n"\
                "Регистрация не окончена"
check_param = False


# sql запрос для первичной регистрации пользователя
def create_pre_user(user_id: int):
    cursor.execute('INSERT INTO user_list (user_id) VALUES (?)',
                   (user_id,))
    conn.commit()


# sql запрос для получения ФИО конкретного пользователя
def get_existing_user(user_id: int):
    global user_name
    global user_second_name
    global user_third_name
    global user_group
    global user_department
    info_name = cursor.execute('SELECT name, second_name, third_name, "group", department FROM user_list '
                               'WHERE user_id=?', (user_id,))
    pre = info_name.fetchone()
    user_name = pre[0]
    user_second_name = pre[1]
    user_third_name = pre[2]
    user_group = pre[3]
    user_department = pre[4]
    print(pre)


# sql запрос для получения ФИО конкретного студента
def get_existing_student(name: str, second_name: str, third_name: str, group: str, department: str):
    global student_name
    global student_second_name
    global student_third_name
    global student_group
    global student_department
    global reply_to_user
    global check_param
    info_name = cursor.execute('SELECT * FROM student_list WHERE name=?1 and second_name=?2 and third_name=?3 '
                               'or name=?1 and second_name=?2 and "group"=?4 '
                               'or name=?1 and second_name=?2 and "group"=?4 and department=?5 '
                               'or name=?1 and second_name=?2 and third_name=?3 and "group"=?4 and department=?5',
                               (name, second_name, third_name, group, department))
    pre = info_name.fetchall()
    if len(pre) == 1:

        reply_to_user = "Студент найден, регистрация окончена"

        pre = pre[0]
        check_param = True

        student_name = pre[1]
        student_second_name = pre[2]
        student_third_name = pre[3]
        student_group = pre[4]
        student_department = pre[5]
        print(student_third_name)

    elif len(pre) != 1:
        reply_to_user = "Студент не найден, дополните недостающую/исправьте настояющую персональную информацию. \n" \
                        "Регистрация не окончена"
        check_param = False


# sql запрос для получения группы конкретного пользователя
def get_existing_user_group(user_id: int):
    global user_group
    info_group = cursor.execute('SELECT "group" FROM user_list WHERE user_id=?', (user_id,))
    pre = info_group.fetchone()
    user_group = pre[0]


# sql запрос для получения факультета конкретного пользователя
def get_existing_user_department(user_id: int):
    global user_department
    info_department = cursor.execute('SELECT department FROM user_list WHERE user_id=?', (user_id,))
    pre = info_department.fetchone()
    user_department = pre[0]


# sql запрос для редактирования имени пользователя
def update_user_name(name: str, user_id: int):
    cursor.execute('UPDATE user_list SET name = ? where user_id = ?', (name, user_id))
    conn.commit()


# sql запрос для редактирования фамилии пользователя
def update_user_second_name(second_name: str, user_id: int):
    cursor.execute('UPDATE user_list SET second_name = ? where user_id = ?', (second_name, user_id))
    conn.commit()


# sql запрос для редактирования отчества пользователя
def update_user_third_name(third_name: str, user_id: int):
    cursor.execute('UPDATE user_list SET third_name = ? where user_id = ?', (third_name, user_id))
    conn.commit()


# sql запрос для редактирования группы пользователя
def update_user_group(group: str, user_id: int):
    cursor.execute('UPDATE user_list SET "group" = ? where user_id = ?', (group, user_id))
    conn.commit()


# sql запрос для редактирования факультета пользователя
def update_user_department(department: str, user_id: int):
    cursor.execute('UPDATE user_list SET department = ? where user_id = ?', (department, user_id))
    conn.commit()
