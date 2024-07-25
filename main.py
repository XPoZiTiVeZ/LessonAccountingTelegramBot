from aiogram import Dispatcher, F
from aiogram.filters import CommandStart, Command

from handlers.message import *
from handlers.callback import *
from handlers.calendar import *
from filters.calendar import *
from filters.filters import *
from utils.states import *
from db.db import *
from bot import dp, bot


import logging
import asyncio
import sys

async def on_startup(dp: Dispatcher):
    dp.message.register(add_student,        CommandStart(deep_link=True))
    dp.message.register(startmsg,           CommandStart())
    dp.message.register(add_student,        add_student_filter)
    dp.callback_query.register(show_menu,   show_menu_filter)
    
    dp.message.register(show_profile,                   F.text.lower() == "профиль")
    dp.callback_query.register(show_profile_call,       show_profile_filter)
    dp.callback_query.register(show_profile_change,     profile_change_filter)
    dp.callback_query.register(profile_change_person,   profile_change_person_filter)
    dp.callback_query.register(delete_association,      delete_association_filter)
    
    dp.message.register(show_calendar_ml,           Command("calendar"))
    dp.message.register(show_calendar,              F.text.lower() == "показать занятия")
    dp.callback_query.register(show_calendar_call,  show_calendar_filter)
    dp.message.register(show_calendar_ml,           F.text.lower() == "посчитать занятия за месяц")
    dp.callback_query.register(show_calendar_ml_call,      show_calendar_ml_filter)
    
    dp.callback_query.register(back_calendar,       back_calendar_filter)
    dp.callback_query.register(day_change_year,     day_change_year_filter)
    dp.callback_query.register(day_change_month,    day_change_month_filter)
    dp.callback_query.register(show_lesson,         day_select_filter)
    dp.callback_query.register(day_change,          day_change_filter)
    dp.callback_query.register(day_cancel,          day_cancel_filter)
    
    dp.callback_query.register(month_select,     month_select_filter)
    dp.callback_query.register(month_back,       month_back_filter)
    
    dp.callback_query.register(year_select,      year_select_filter)
    dp.callback_query.register(year_change,      year_change_filter)
    dp.callback_query.register(year_back,        year_back_filter)
    
    
    dp.callback_query.register(back_calendar_ml,        back_calendar_ml_filter)
    dp.callback_query.register(year_change_ml,          year_change_ml_filter)
    dp.callback_query.register(year_select_ml,          year_select_ml_filter)
    dp.callback_query.register(year_back_ml,            year_back_ml_filter)
    dp.callback_query.register(month_change_year_ml,    month_change_year_ml_filter)
    dp.callback_query.register(show_month_lessons,      month_select_ml_filter)
    dp.callback_query.register(export_month_lessons,    export_calendar_ml_filter)
    dp.callback_query.register(export_month_lessons,    export_calendar_ml_profile_filter)
    dp.callback_query.register(month_cancel_ml,         month_cancel_ml_filter)
    
    
    dp.callback_query.register(change_lesson_status,        change_lesson_status_filter)
    dp.callback_query.register(change_lesson_description,   change_lesson_description_filter)
    dp.message.register(change_lesson_description_message,  Description.send)
    dp.callback_query.register(delete_lesson_description,   delete_lesson_description_filter)

    
    dp.callback_query.register(show_lesson_files,   show_lesson_files_filter)
    dp.callback_query.register(add_lesson_files,    add_lesson_files_filter)
    dp.message.register(add_lesson_files_message,   Files.send, F.document != None)
    dp.message.register(add_lesson_files_message,   Files.send, F.photo != None)
    dp.callback_query.register(delete_lesson_file,  delete_lesson_file_filter)
    


async def start():
    create_db()
        
    await on_startup(dp)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start())