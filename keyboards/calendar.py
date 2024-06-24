import calendar
from datetime import date

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


week_days = ('Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс')
months = ('Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь')

def get_years_keyboard(this_date: None | date = None, back_date: None | str = None) -> InlineKeyboardMarkup:
    if this_date is None:
        this_date: date = date.today()
    
    if back_date is None:
        back_date: date = date.today()
    
    floor_year = this_date.year // 10 * 10
    current_year = lambda year: f"[{year}]" if year == date.today().year else f"{year}"

    keyboard = InlineKeyboardBuilder()
    for i in range(5):
        date1 = date(floor_year + i*2, this_date.month, this_date.day)
        date2 = date(floor_year + i*2 + 1, this_date.month, this_date.day)

        keyboard.add(
            InlineKeyboardButton(text=current_year(floor_year+i*2), callback_data=f"year|{date1}|selected"),
            InlineKeyboardButton(text=current_year(floor_year+i*2+1), callback_data=f"year|{date2}|selected"),
        )
    
    prev_date = date(this_date.year-10, this_date.month, this_date.day)
    next_date = date(this_date.year+10, this_date.month, this_date.day)
    
    keyboard.add(
        InlineKeyboardButton(text="<<", callback_data=f"year|{prev_date}|{back_date}|change"),
        InlineKeyboardButton(text="Назад", callback_data=f"year|{back_date}|back"),
        InlineKeyboardButton(text=">>", callback_data=f"year|{next_date}|{back_date}|change"),
    )

    keyboard.adjust(*(2, 2, 2, 2, 2, 3, 1))
    return keyboard.as_markup()

def get_months_keyboard(this_date: None | date = None, back_date: None | date = None) -> InlineKeyboardMarkup:
    if this_date is None:
        this_date: date = date.today()
    
    if back_date is None:
        back_date: date = date.today()

    now_month = date.today().month
    current_month = lambda month: f"[{months[month-1]}]" if month == now_month else f"{months[month-1]}"

    keyboard = InlineKeyboardBuilder()
    for i in range(1, 7):
        date1 = date(this_date.year, i*2-1, this_date.day)
        date2 = date(this_date.year, i*2, this_date.day)
        
        keyboard.add(
            InlineKeyboardButton(text=current_month(i * 2 - 1), callback_data=f"month|{date1}|selected"),
            InlineKeyboardButton(text=current_month(i * 2), callback_data=f"month|{date2}|selected"),
        )
    keyboard.add(
        InlineKeyboardButton(text="Назад", callback_data=f"month|{back_date}|back")
    )

    keyboard.adjust(*(2, 2, 2, 2, 2, 2, 2, 1))
    return keyboard.as_markup()

def get_days_keyboard(this_date: None | date = None, lessons: None | list = None):
    if this_date is None:
        this_date: date = date.today()
    
    if lessons is None:
        lessons = list()
    
    now_year = date.today().year
    now_month = date.today().month
    now_day = date.today().day
    my_clndr = calendar.Calendar()
    current_year = lambda year: f"[{year}]" if year == now_year else f"{year}"
    current_month = lambda month: f"[{months[month-1]}]" if month == now_month and this_date.year == now_year else f"{months[month-1]}"
    current_day = lambda day: f"[{day}]" if day == now_day and this_date.month == now_month and this_date.year == now_year else f"{day}"
    day_has_lesson = lambda day, string: "#" + string if day in list(map(lambda lesson: lesson.date, lessons)) else string

    
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=current_month(this_date.month), callback_data=f"day|{this_date}|month_edit"))
    keyboard.add(InlineKeyboardButton(text=current_year(this_date.year), callback_data=f"day|{this_date}|year_edit"))
    for day in week_days:
        keyboard.add(InlineKeyboardButton(text=f"{day}", callback_data="None"))
    
    all_days = list(my_clndr.itermonthdates(this_date.year, this_date.month))
    for day in all_days:
        date1 = date(day.year, day.month, day.day)
        keyboard.add(InlineKeyboardButton(text=day_has_lesson(day, current_day(day.day)), callback_data=f"day|{date1}|selected"))
    
    if this_date.month == 1:
        prev_date = date(this_date.year-1, 12, 1)
    else:
        prev_date = date(this_date.year, this_date.month-1, 1)
    
    if this_date.month == 12:
        next_date = date(this_date.year+1, 1, 1)
    else:
        next_date = date(this_date.year, this_date.month+1, 1)

    keyboard.add(
        InlineKeyboardButton(text="<<", callback_data=f"day|{prev_date}|change"),
        InlineKeyboardButton(text="Отмена", callback_data=f"day|cancel"),
        InlineKeyboardButton(text=">>", callback_data=f"day|{next_date}|change"),
    )

    keyboard.adjust(2, 7, *[7 for _ in range(len(all_days)//7)], 3)
    return keyboard.as_markup()

def get_years_ml_keyboard(this_date: None | date = None, back_date: None | date | str = None) -> InlineKeyboardMarkup:
    if this_date is None:
        this_date: date = date.today()
    
    if back_date is None:
        back_date: date = date.today()
    
    floor_year = this_date.year // 10 * 10
    current_year = lambda year: f"[{year}]" if year == date.today().year else f"{year}"

    keyboard = InlineKeyboardBuilder()
    for i in range(5):
        date1 = date(floor_year + i*2, this_date.month, this_date.day)
        date2 = date(floor_year + i*2 + 1, this_date.month, this_date.day)

        keyboard.add(
            InlineKeyboardButton(text=current_year(floor_year+i*2), callback_data=f"year|{date1}|selected_ml"),
            InlineKeyboardButton(text=current_year(floor_year+i*2+1), callback_data=f"year|{date2}|selected_ml"),
        )
    
    prev_date = date(this_date.year-10, this_date.month, this_date.day)
    next_date = date(this_date.year+10, this_date.month, this_date.day)
    
    keyboard.add(
        InlineKeyboardButton(text="<<", callback_data=f"year|{prev_date}|{back_date}|change_ml"),
        InlineKeyboardButton(text="Назад", callback_data=f"year|{back_date}|back_ml"),
        InlineKeyboardButton(text=">>", callback_data=f"year|{next_date}|{back_date}|change_ml"),
    )

    keyboard.adjust(*(2, 2, 2, 2, 2, 3, 1))
    return keyboard.as_markup()

def get_months_ml_keyboard(this_date: None | date = None) -> InlineKeyboardMarkup:
    if this_date is None:
        this_date: date = date.today()
    
    now_month = date.today().month
    now_year = date.today().year
    current_month = lambda month: f"[{months[month-1]}]" if month == now_month and this_date.year == now_year else f"{months[month-1]}"
    current_year = lambda year: f"[{year}]" if year == date.today().year else f"{year}"

    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=current_year(this_date.year), callback_data=f"month|{this_date}|year_edit_ml"))
    for i in range(1, 7):
        date1 = date(this_date.year, i*2-1, this_date.day)
        date2 = date(this_date.year, i*2, this_date.day)
        
        keyboard.add(
            InlineKeyboardButton(text=current_month(i * 2 - 1), callback_data=f"month|{date1}|selected_ml"),
            InlineKeyboardButton(text=current_month(i * 2), callback_data=f"month|{date2}|selected_ml"),
        )
    keyboard.add(
        InlineKeyboardButton(text="Отмена", callback_data=f"month|cancel_ml")
    )

    keyboard.adjust(*(1, 2, 2, 2, 2, 2, 2, 2, 1))
    return keyboard.as_markup()