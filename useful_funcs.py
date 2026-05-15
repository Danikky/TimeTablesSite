import datetime
import parser

#Добавил модуль чисто для различных нужных функций, чтобы не засорять другие модули




#Вроде работает, но надо потестить нормально, с незаконченной рабочей неделей
def get_week_hours():
    """Возвращаем словарь с парами группа + количество часов за эту рабочую неделю(прошедшую, если сегодня выходной)
    \n Часов, не пар (пар меньше в 2 раза)"""
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    week_dates = []
    for i in range(6):  # 0=пн, 5=сб
        d = monday + datetime.timedelta(days=i)
        week_dates.append(f"{d.day}.{str(d.month).zfill(2)}")
    

    
    all_sheets = parser.read_sheets()
    week_sheets = []
    for s in all_sheets:
        if s['date'] in week_dates:
            week_sheets.append(s)

    
    group_lessons = {}
    for sheet in week_sheets:
        key = sheet['date'] + ' ' + sheet['day']
        for lesson in sheet[key]:
            name = lesson['name']
            count = 0
            for i in range(1, 7):
                slot = lesson[str(i)]
                if slot and slot.get('para'):
                    count += 1
            group_lessons[name] = group_lessons.get(name, 0) + count

    result = {}
    for name, lessons in group_lessons.items():
        result[name] = lessons * 2
    return result

