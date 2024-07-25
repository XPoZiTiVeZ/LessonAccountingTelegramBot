from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.utils.deep_linking import create_start_link

from datetime import date
from bot import mime_types

def get_menu_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    
    keyboard.add(
        KeyboardButton(text="Профиль"),
        KeyboardButton(text="Показать занятия"),
        KeyboardButton(text="Посчитать занятия за месяц"),
    )
    
    keyboard.adjust(2, 2)
    return keyboard.as_markup()

def get_menu_inline_keyboard(this_date = None) -> InlineKeyboardBuilder:
    if this_date is None:
        this_date: date = date.today()
    keyboard = InlineKeyboardBuilder()
    
    keyboard.add(
        InlineKeyboardButton(text="Профиль", callback_data="profile"),
        InlineKeyboardButton(text="Показать занятия", callback_data=f"calendar|{this_date}"),
        InlineKeyboardButton(text="Проверить занятия", callback_data=f"calendar_ml|{this_date}"),
    )
    keyboard.adjust(1)
    return keyboard.as_markup()

def get_to_menu_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    
    keyboard.add(
        InlineKeyboardButton(text="Профиль", callback_data="profile"),
    )

    return keyboard.as_markup()

def get_profile_keyboard(text, association_id):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text=text, callback_data="profile|change"))
    if association_id is not None:
        keyboard.add(InlineKeyboardButton(text=f"Удалить связь (1/3)", callback_data=f"profile|{association_id}|delete|1"))
        keyboard.add(InlineKeyboardButton(text=f"Даты занятий в этом месяце", callback_data=f"calendar_ml|{date.today()}|export_profile"))
    keyboard.add(InlineKeyboardButton(text="назад", callback_data="menu"))
    
    keyboard.adjust(1)
    return keyboard.as_markup()

def get_delete_association_keyboard(association_id, n: int):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text=f"Удалить связь ({n}/3)", callback_data=f"profile|{association_id}|delete|{n}"))
    keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="profile"))
    
    keyboard.adjust(1)
    return keyboard.as_markup()

def get_person_keyboard(persons):
    keyboard = InlineKeyboardBuilder()
    
    for text, value in persons:
        keyboard.add(InlineKeyboardButton(text=text, callback_data=f"profile|change|{value}"))
    
    keyboard.add(InlineKeyboardButton(text="назад", callback_data="profile"))
    
    keyboard.adjust(1)
    return keyboard.as_markup()

def get_lesson_keyboard(date: str, association_id: str, description: bool, chat_id: int, message_id: int):
    keyboard = InlineKeyboardBuilder()
    
    keyboard.add(InlineKeyboardButton(text="Изменить статус", callback_data=f"change_status|{date}|{association_id}"))
    keyboard.add(InlineKeyboardButton(text=f"{'Изменить описание' if description else 'Добавить описание'}", callback_data=f"change_description|{date}|{association_id}"))
    keyboard.add(InlineKeyboardButton(text="Файлы", callback_data=f"files|{date}|{association_id}"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data=f"calendar|{date}"))

    keyboard.adjust(1)
    return keyboard.as_markup()

def change_description_keyboard(date: str):
    keyboard = InlineKeyboardBuilder()
    
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data=f"day|{date}|selected"))
    
    keyboard.adjust(1)
    return keyboard.as_markup()

def get_back_to_lesson_from_description_keyboard(date: str, association_id: str, deleteDescription=False):
    keyboard = InlineKeyboardBuilder()
    
    if deleteDescription:
        keyboard.add(InlineKeyboardButton(text="Удалить описание", callback_data=f"delete_description|{date}|{association_id}"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data=f"day|{date}|selected"))
    
    keyboard.adjust(1)
    return keyboard.as_markup()

def get_lesson_files_keyboard(date: str, association_id: str, files: list):
    keyboard = InlineKeyboardBuilder()
    
    keyboard.add(InlineKeyboardButton(text="Добавить файлы", callback_data=f"add_files|{date}|{association_id}"))
    for file in files:
        parts = file.file_name.split(".")
        has_ext = parts[-1] in mime_types.values()
        ext = parts[-1] if has_ext else ""
        name = ".".join(parts[:-1] if has_ext else parts)
        
        keyboard.add(InlineKeyboardButton(text=f"Удалить файл {name[:16] + "." + ext}", callback_data=f"delete_file|{date}|{association_id}|{file.id}"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data=f"day|{date}|selected"))
    
    keyboard.adjust(1)
    return keyboard.as_markup()

def get_add_lesson_files_keyboard(date: str, association_id: str):
    keyboard = InlineKeyboardBuilder()
    
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data=f"files|{date}|{association_id}"))
    
    keyboard.adjust(1)
    return keyboard.as_markup()

def get_month_lessons_keyboard(date: date):
    keyboard = InlineKeyboardBuilder()
    
    keyboard.add(InlineKeyboardButton(text="Печать всех дат", callback_data=f"calendar_ml|{date}|export"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data=f"calendar_ml|{date}"))
    
    keyboard.adjust(1)
    return keyboard.as_markup()

def get_export_month_lessons_keyboard(date: date):
    keyboard = InlineKeyboardBuilder()
    
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data=f"month|{date}|selected_ml"))
    
    keyboard.adjust(1)
    return keyboard.as_markup()