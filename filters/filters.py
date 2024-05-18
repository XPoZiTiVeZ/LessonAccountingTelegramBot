from aiogram.types import CallbackQuery, Message

def show_menu_filter(call: CallbackQuery) -> bool:
    match call.data:
        case "menu":
            return True
    return False

def show_link_filter(call: CallbackQuery) -> bool:
    match call.data:
        case "show_link":
            return True
    return False

def add_student_filter(message: Message) -> bool:
    match message.text.split("?="):
        case "/add", _:
            return True
    return False

def show_profile_filter(call: CallbackQuery) -> bool:
    match call.data:
        case "profile":
            return True
    return False

def delete_association_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "profile", _, "delete", _:
            return True
    return False

def profile_change_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "profile", "change":
            return True
    return False

def profile_change_person_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "profile", "change", _:
            return True
    return False

def change_lesson_status_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "change_status", _, _:
            return True
    return False

def change_lesson_description_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "change_description", _, _:
            return True
    return False

def delete_lesson_description_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "delete_description", _, _:
            return True
    return False

def back_calendar_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "calendar", _:
            return True
    return False

def export_calendar_ml_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "calendar_ml", _, "export":
            return True
    return False

def back_calendar_ml_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "calendar_ml", _:
            return True
    return False