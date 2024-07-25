from aiogram.types import CallbackQuery

def show_calendar_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "calendar", _:
            return True
    return False

def show_calendar_ml_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "calendar_ml", _:
            return True
    return False

def year_select_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "year", _, "selected":
            return True
    return False

def year_change_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "year", _, _, "change":
            return True
    return False

def year_back_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "year", _, "back":
            return True
    return False

def month_select_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "month", _, "selected":
            return True
    return False

def month_back_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "month", _, "back":
            return True
    return False

def day_change_year_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "day", _, "year_edit":
            return True
    return False

def day_change_month_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "day", _, "month_edit":
            return True
    return False

def day_select_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "day", _, "selected":
            return True
    return False

def new_day_select_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "day", _, "selected", _, _:
            return True
    return False

def day_change_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "day", _, "change":
            return True
    return False

def day_cancel_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "day", "cancel":
            return True
    return False

###################################################################

def year_change_ml_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "year", _, _, "selected_ml":
            return True
    return False

def year_select_ml_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "year", _, "selected_ml":
            return True
    return False

def year_back_ml_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "year", _, "back_ml":
            return True
    return False

def month_change_year_ml_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "month", _, "year_edit_ml":
            return True
    return False

def month_select_ml_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "month", _, "selected_ml":
            return True
    return False

def month_cancel_ml_filter(call: CallbackQuery) -> bool:
    match call.data.split("|"):
        case "month", "cancel_ml":
            return True
    return False