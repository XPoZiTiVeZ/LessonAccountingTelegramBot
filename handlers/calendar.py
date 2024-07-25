from aiogram.types import CallbackQuery
from datetime import date
from aiogram.fsm.context import FSMContext

from keyboards.calendar import *
from db.db import User
from handlers.callback import show_menu

async def check_user(from_user, state: FSMContext) -> User:
    await state.clear()

    user: User | None = User.get(from_user.id)
    if user is None:
        return User.add(from_user.id, from_user.username, from_user.first_name, from_user.last_name)
    
    User.update(user, from_user.username, from_user.first_name, from_user.last_name)
    return user

async def year_select(callback: CallbackQuery, state: FSMContext):
    user = await check_user(callback.from_user, state)
    _, this_date, _ = callback.data.split("|")
    this_date = date.fromisoformat(this_date)
    
    await callback.message.edit_text(
        "Выберите день занятия.",
        reply_markup=get_days_keyboard(this_date, lessons=user.lessons(this_date.month, this_date.year))
    )

async def year_change(callback: CallbackQuery):
    _, this_date, back_date, _ = callback.data.split("|")
    this_date = date.fromisoformat(this_date)
    
    await callback.message.edit_text(
        "Выберите год.",
        reply_markup=get_years_keyboard(this_date, back_date)
    )

async def year_back(callback: CallbackQuery, state: FSMContext):
    user = await check_user(callback.from_user, state)
    _, back_date, _ = callback.data.split("|")
    back_date = date.fromisoformat(back_date)
    
    await callback.message.edit_text(
        "Выберите день занятия.",
        reply_markup=get_days_keyboard(back_date, lessons=user.lessons(back_date.month, back_date.year))
    )

async def month_select(callback: CallbackQuery, state: FSMContext):
    user = await check_user(callback.from_user, state)
    _, this_date, _ = callback.data.split("|")
    this_date = date.fromisoformat(this_date)
    
    await callback.message.edit_text(
        "Выберите месяц.",
        reply_markup=get_days_keyboard(this_date, lessons=user.lessons(this_date.month, this_date.year))
    )

async def month_back(callback: CallbackQuery, state: FSMContext):
    user = await check_user(callback.from_user, state)
    _, back_date, _ = callback.data.split("|")
    back_date = date.fromisoformat(back_date)
    
    await callback.message.edit_text(
        "Выберите день занятия.",
        reply_markup=get_days_keyboard(back_date, lessons=user.lessons(back_date.month, back_date.year))
    )

async def day_change_year(callback: CallbackQuery):
    _, this_date, _ = callback.data.split("|")
    this_date = date.fromisoformat(this_date)
    
    await callback.message.edit_text(
        "Выберите год.",
        reply_markup=get_years_keyboard(this_date, this_date)
    )

async def day_change_month(callback: CallbackQuery):
    _, this_date, _ = callback.data.split("|")
    this_date = date.fromisoformat(this_date)
    
    await callback.message.edit_text(
        "Выберите месяц.",
        reply_markup=get_months_keyboard(this_date, this_date)
    )

async def day_change(callback: CallbackQuery, state: FSMContext):
    user = await check_user(callback.from_user, state)
    _, this_date, _ = callback.data.split("|")
    this_date = date.fromisoformat(this_date)

    await callback.message.edit_text(
        "Выберите день занятия.",
        reply_markup=get_days_keyboard(this_date, lessons=user.lessons(this_date.month, this_date.year))
    )

async def day_cancel(callback: CallbackQuery, state: FSMContext):
    await show_menu(callback, state)

#######################################################

async def year_change_ml(callback: CallbackQuery):
    _, this_date, back_date, _ = callback.data.split("|")
    this_date = date.fromisoformat(this_date)
    
    await callback.message.edit_text(
        "Выберите год.",
        reply_markup=get_years_ml_keyboard(this_date, back_date)
    )

async def year_select_ml(callback: CallbackQuery):
    _, this_date, _ = callback.data.split("|")
    this_date = date.fromisoformat(this_date)
    
    await callback.message.edit_text(
        "Выберите месяц.",
        reply_markup=get_months_ml_keyboard(this_date)
    )

async def year_back_ml(callback: CallbackQuery):
    _, back_date, _ = callback.data.split("|")
    back_date = date.fromisoformat(back_date)
    
    await callback.message.edit_text(
        "Выберите месяц.",
        reply_markup=get_months_ml_keyboard(back_date)
    )

async def month_change_year_ml(callback: CallbackQuery):
    _, this_date, _ = callback.data.split("|")
    this_date = date.fromisoformat(this_date)
    
    await callback.message.edit_text(
        "Выберите год.",
        reply_markup=get_years_ml_keyboard(this_date)
    )

async def month_cancel_ml(callback: CallbackQuery, state: FSMContext):
    await show_menu(callback, state)