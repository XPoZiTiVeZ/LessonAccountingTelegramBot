from aiogram.types import Message, CallbackQuery
from aiogram.utils.deep_linking import create_start_link, decode_payload
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext

from bot import bot, mime_types
from db.db import *
from keyboards.keyboards import *
from keyboards.calendar import *
from handlers.callback import show_lesson
from utils.states import Files

import locale

locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))

async def check_user(from_user, state: FSMContext, clear: bool = True) -> User:
    if clear:
        await state.clear()

    user: User | None = User.get(from_user.id)
    if user is None:
        return User.add(from_user.id, from_user.username, from_user.first_name, from_user.last_name)
    
    User.update(user, from_user.username, from_user.first_name, from_user.last_name)
    return user

async def startmsg(message: Message,  state: FSMContext):
    await check_user(message.from_user, state)
    await message.answer(
        "Здраствуйте, я бот, который ведёт учёт ваших занятий, а также информацию о них.",
        reply_markup=get_menu_keyboard()
    )

async def add_student(message: Message, command: CommandObject, state: FSMContext):
    user = await check_user(message.from_user, state)
    teacher: User | None = User.get(int(command.args))
    
    if teacher is None:
        return await message.answer(f"Учителя с таким id не существует")
    
    try:
        teacher.add_student(user)
        return await message.answer(f"Вы успешно прикреплены к учителю @{teacher.username}")
    except SameUserException:
        return await message.answer("Вы не можете прикрепить себя")
    except EntryAlreadyExists:
        return await message.answer(f"Вы уже были прикреплены к учителю @{teacher.username}")

async def show_calendar(message: Message, state: FSMContext):
    user = await check_user(message.from_user, state)
    await message.answer("Выберите день занятия.", reply_markup=get_days_keyboard(lessons=user.lessons()))

async def show_calendar_ml(message: Message):
    await message.answer("Выберите месяц.", reply_markup=get_months_ml_keyboard())

async def show_profile(message: Message, state: FSMContext):
    user = await check_user(message.from_user, state)
    association = Association.get(user.association_id)

    text = "Выберите связь"
    if association is not None:
        if association.teacher_id == user.user_id:
            another_user: User | None = User.get(association.student_id)
            if another_user is not None:
                text = "Ученик {}".format(another_user.username)
        else:
            another_user: User | None = User.get(association.teacher_id)
            if another_user is not None:
                text = "Учитель {}".format(another_user.username)
    
    await message.answer(
        "Профиль\nСсылка для прикрепления ученика:\n{}\nЗанятий в этом месяце: {}\n{}\n".format(
            await create_start_link(bot, payload=str(user.user_id)),
            len(user.lessons()),
            "Выберите связь" if user.association_id is None or association is None else "Вы ученик" if association.student_id == user.user_id else "Вы учитель"
        ),
        reply_markup=get_profile_keyboard(text, association.association_id if association is not None else None)
    )

async def change_lesson_description_message(message: Message, state: FSMContext):
    data = await state.get_data()
    user = await check_user(message.from_user, state)
    
    this_date = data.get("date")
    association = Association.get(data.get("association_id"))
    lesson = Lesson.get(this_date, association.association_id)
    
    if association is None:
        await message.answer(
            "Ошибка, повторите выбор учителя или ученика в профиле и выберите день снова.",
            reply_markup=get_to_menu_keyboard()
        )
        return
    
    if association.association_id != user.association_id:
        await message.answer(
            "Ошибка, ваш учитель/ученик не совпадает с выбранным в профиле.",
            reply_markup=get_to_menu_keyboard()
        )
        return
    
    if len(message.text) > 4000:
        if lesson is None:
            return await message.answer(
                "Ошибка, сообщение больше 4000 символов.",
                reply_markup=change_description_keyboard(this_date)
            )
        
        return await message.answer(
            "Ошибка, сообщение больше 4000 символов.",
            reply_markup=get_back_to_lesson_from_description_keyboard(this_date, association.association_id, False)
        )

    if lesson is None:
        lesson = Lesson.add(date=this_date, description=None, status=statuses[0], association_id=association.association_id)
    Lesson.change_description(lesson, message.text)

    call = CallbackQuery(from_user=message.from_user, message=message, data=f"day|{this_date}|selected")
    await show_lesson(call, state)


async def add_lesson_files_message(message: Message, state: FSMContext):
    data = await state.get_data()
    user = await check_user(message.from_user, state, False)

    this_date = data.get("date")
    association_id = data.get("association_id")
    association = Association.get(association_id)
    lesson = Lesson.get(this_date, association.association_id)
    
    if association is None:
        await message.answer(
            "Ошибка, повторите выбор учителя или ученика в профиле и выберите день снова.",
            reply_markup=get_to_menu_keyboard()
        )
        return
    
    if association.association_id != user.association_id:
        await message.answer(
            "Ошибка, ваш учитель/ученик не совпадает с выбранным в профиле.",
            reply_markup=get_to_menu_keyboard()
        )
        return
    
    files = [] if lesson is None else lesson.files()
    
    input_file = None
    if document := message.document:
        input_file = document
    
    elif photo := message.photo[-1]:
        input_file = photo
    
    if len(files) >= 8:
        if lesson is None:
            return await message.answer(
                "Ошибка, файлов больше 8.",
                reply_markup=change_description_keyboard(this_date)
            )
        return await message.answer(
            "Ошибка, файлов больше 8.",
            reply_markup=get_add_lesson_files_keyboard(this_date, association.association_id)
        )
    
    if lesson is None:
        lesson = Lesson.add(date=this_date, description=None, status=statuses[0], association_id=association.association_id)
    
    lesson.add_file(input_file.file_id, input_file.file_name)
    
    await message.answer(
        "Файл успешно добавлен",
        reply_markup=get_add_lesson_files_keyboard(this_date, association.association_id)
    )