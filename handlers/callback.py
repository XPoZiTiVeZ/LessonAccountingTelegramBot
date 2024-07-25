from aiogram.types import Message, CallbackQuery, BufferedInputFile, InputMediaDocument
from aiogram.fsm.context import FSMContext
from datetime import date

from keyboards.keyboards import *
from keyboards.calendar import *
from utils.states import *
from db.db import *
from bot import bot

async def check_user(from_user, state: FSMContext) -> User:
    await state.clear()

    user: User | None = User.get(from_user.id)
    if user is None:
        return User.add(from_user.id, from_user.username, from_user.first_name, from_user.last_name)
    
    User.update(user, from_user.username, from_user.first_name, from_user.last_name)
    return user

async def show_menu(call: CallbackQuery, state: FSMContext):
    await check_user(call.from_user, state)
    
    await call.message.edit_text(
        "Выберите пункт в меню.",
        reply_markup=get_menu_inline_keyboard()
    )

async def show_calendar_call(call: CallbackQuery, state: FSMContext):
    user = await check_user(call.from_user, state)
    _, this_date = call.data.split("|")
    this_date = date.fromisoformat(this_date)
    
    await call.message.edit_text("Выберите день занятия.", reply_markup=get_days_keyboard(this_date, lessons=user.lessons(this_date.month, this_date.year)))

async def show_calendar_ml_call(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Выберите месяц.", reply_markup=get_months_ml_keyboard())

async def show_profile_call(call: CallbackQuery, state: FSMContext):
    user = await check_user(call.from_user, state)
    association = Association.get(user.association_id)

    text = "Выберите"
    if association is not None:
        if association.teacher_id == user.user_id:
            another_user: User | None = User.get(association.student_id)
            if another_user is not None:
                text = "Ученик {}".format(another_user.username)
        else:
            another_user: User | None = User.get(association.teacher_id)
            if another_user is not None:
                text = "Учитель {}".format(another_user.username)
    
    await call.message.edit_text(
        "Профиль\nСсылка для прикрепления ученика:\n{}\nЗанятий в этом месяце: {}\n{}\n".format(
            await create_start_link(bot, payload=str(user.user_id)),
            len(user.lessons()),
            "Выберите связь" if user.association_id is None or association is None else "Вы ученик" if association.student_id == user.user_id else "Вы учитель"
        ),
        reply_markup=get_profile_keyboard(text, user.association_id if association is not None else None)
    )

async def delete_association(call: CallbackQuery, state: FSMContext):
    await check_user(call.from_user, state)
    _, association_id, _, repeat = call.data.split("|")
    association = Association.get(association_id)
    
    if association is None:
        return await call.message.edit_text(
            "Связи не существует",
            reply_markup=get_to_menu_keyboard()
        )
    
    if int(repeat) <= 3:
        return await call.message.edit_text(
            "Подтвердите удаление связи",
            reply_markup=get_delete_association_keyboard(association_id, int(repeat) + 1)
        )
    
    association.delete()
    
    return await call.message.edit_text(
            "Связь успешно удалена",
            reply_markup=get_to_menu_keyboard()
        )
    
async def show_profile_change(call: CallbackQuery, state: FSMContext):
    user = await check_user(call.from_user, state)
    
    associations = Association.get_all(user.user_id)
    persons = list()
    for association in associations:
        if association.teacher_id == user.user_id:
            another_user = User.get(association.student_id)
            persons.append((f"Ученик {another_user.username}",  association.association_id))
        else:
            another_user = User.get(association.teacher_id)
            persons.append((f"Учитель {another_user.username}", association.association_id))
    
    await call.message.edit_text(
        "Выберите ученика или учителя.",
        reply_markup=get_person_keyboard(persons)
    )
    
async def profile_change_person(call: CallbackQuery, state: FSMContext):
    user = await check_user(call.from_user, state)
    _, _, association_id = call.data.split("|")
    
    association = Association.get(association_id)
    if association is None:
        call.answer("Ошибка", show_alert=True)
        await show_profile_call(call, state)
        return

    User.change_association(user, association_id)
        
    await show_profile_call(call, state)

async def back_calendar(call: CallbackQuery, state: FSMContext):
    user = await check_user(call.from_user, state)
    _, this_date = call.data.split("|")
    this_date = date.fromisoformat(this_date)
    
    await call.message.edit_text("Выберите день занятия.", reply_markup=get_days_keyboard(this_date, lessons=user.lessons(this_date.month, this_date.year)))

async def show_lesson(call: CallbackQuery, state: FSMContext):
    user = await check_user(call.from_user, state)
    _, this_date, _ = call.data.split("|")
    this_date = date.fromisoformat(this_date)
    
    association = Association.get(user.association_id)
    lesson = Lesson.get(this_date, user.association_id)
    
    if association is None:
        return await call.message.edit_text(
            "Ошибка, повторите выбор учителя или ученика в профиле и выберите день снова.",
            reply_markup=get_to_menu_keyboard()
        )
    
    association = Association.get(user.association_id)
    teacher, student = User.get(association.teacher_id), User.get(association.student_id)
    if lesson is None:
        message = await call.message.edit_text(
            "Занятие        {}\nСтатус:          {}\nУчитель:       @{}\nУченик:         @{}\nОписание:    {}".format(
                this_date.strftime("%d.%m.%Y"), "Не состоялось",
                teacher.username, student.username,
                "Нет"
            )
        )
        await message.edit_reply_markup(reply_markup=get_lesson_keyboard(this_date, user.association_id, False, message.chat.id, message.message_id))
    
    message = await call.message.edit_text(
        "Занятие        {}\nСтатус:           {}\nУчитель:       @{}\nУченик:         @{}\nОписание:    {}".format(
            lesson.date.strftime("%d.%m.%Y"), lesson.status,
            teacher.username, student.username,
            "Нет" if lesson.description is None or lesson.description == "" else f"\n{lesson.description}"
        ),
        disable_web_page_preview=True
    )
    await message.edit_reply_markup(reply_markup=get_lesson_keyboard(lesson.date, lesson.association_id, lesson.description is not None and lesson.description != "", message.chat.id, message.message_id))

async def show_month_lessons(call: CallbackQuery, state: FSMContext):
    user = await check_user(call.from_user, state)
    _, this_date, _ = call.data.split("|")
    this_date = date.fromisoformat(this_date)
    
    months = ('Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь')
    lessons = len(user.lessons(this_date.month, this_date.year))
    
    await call.message.edit_text(
        "В {} {} года состоялось {} заняти{}".format(
            f"{months[this_date.month - 1][:-1]}е".lower(), this_date.year,
            lessons,
            "й" if lessons % 10 in [0, 5, 6, 7, 8, 9] or lessons in range(11, 20) else "е" if lessons % 10 == 1 else "я"
        ),
        reply_markup=get_month_lessons_keyboard(this_date)
    )

async def export_month_lessons(call: CallbackQuery, state: FSMContext):
    user = await check_user(call.from_user, state)
    _, this_date, ending = call.data.split("|")
    this_date = date.fromisoformat(this_date)
    
    months = ('Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь')
    lessons = user.lessons(this_date.month, this_date.year)
    
    await call.message.edit_text(
        "Даты {} занятий в {} {} года:\n{}".format(
            len(lessons),
            f"{months[this_date.month - 1][:-1]}е".lower(),
            this_date.year,
            "\n".join(list(map(lambda lesson: str(lesson.date), lessons)))
        ),
        reply_markup=get_export_month_lessons_keyboard(this_date) if ending == "export" else get_to_menu_keyboard()
    )

async def back_calendar_ml(call: CallbackQuery, state: FSMContext):
    await check_user(call.from_user, state)
    _, this_date = call.data.split("|")
    this_date = date.fromisoformat(this_date)
    
    await call.message.edit_text("Выберите месяц.", reply_markup=get_months_ml_keyboard(this_date))

async def change_lesson_status(call: CallbackQuery, state: FSMContext):
    user = await check_user(call.from_user, state)
    _, this_date, association_id = call.data.split("|")
    
    this_date = date.fromisoformat(this_date)
    association = Association.get(association_id)
    
    if association is None:
        await call.message.edit_text(
            "Ошибка, повторите выбор учителя или ученика в профиле и выберите день снова.",
            reply_markup=get_to_menu_keyboard()
        )
        return
    
    if association.association_id != user.association_id:
        await call.message.edit_text(
            "Ошибка, ваш учитель/ученик не совпадает с выбранным в профиле.",
            reply_markup=get_to_menu_keyboard()
        )
        return
    
    lesson = Lesson.get(this_date, association.association_id)
    if lesson is None:
        lesson = Lesson.add(date=this_date, description=None, status=statuses[0], association_id=association_id)
    lesson.change_status()
    
    call = CallbackQuery(id=call.id, from_user=call.from_user, chat_instance=call.chat_instance, message=call.message, inline_message_id=call.inline_message_id, data=f"day|{this_date}|selected")
    await show_lesson(call, state)

async def change_lesson_description(call: CallbackQuery, state: FSMContext):
    user = await check_user(call.from_user, state)
    _, this_date, association_id = call.data.split("|")
    
    this_date = date.fromisoformat(this_date)
    association = Association.get(association_id)
    description = ""
    lesson = Lesson.get(this_date, association.association_id)
    if lesson is not None:
        description = lesson.description
    
    if association is None:
        await call.message.edit_text(
            "Ошибка, повторите выбор учителя или ученика в профиле и выберите день снова.",
            reply_markup=get_to_menu_keyboard()
        )
        return
    
    if association.association_id != user.association_id:
        await call.message.edit_text(
            "Ошибка, ваш учитель/ученик не совпадает с выбранным в профиле.",
            reply_markup=get_to_menu_keyboard()
        )
        return
    
    await state.set_state(Description.send)
    await state.set_data({"date": this_date, "association_id": association_id})
    
    await call.message.edit_text(
        "Пришлите описание занятия. До 4000 символов.",
        reply_markup=get_back_to_lesson_from_description_keyboard(this_date, association.association_id, description not in [None, ""]),
        disable_web_page_preview=True
    )

async def delete_lesson_description(call: CallbackQuery, state: FSMContext):
    user = await check_user(call.from_user, state)
    _, this_date, association_id = call.data.split("|")
    
    this_date = date.fromisoformat(this_date)
    association = Association.get(association_id)
    
    if association is None:
        await call.message.edit_text(
            "Ошибка, повторите выбор учителя или ученика в профиле и выберите день снова.",
            reply_markup=get_to_menu_keyboard()
        )
        return
    
    if association.association_id != user.association_id:
        await call.message.edit_text(
            "Ошибка, ваш учитель/ученик не совпадает с выбранным в профиле.",
            reply_markup=get_to_menu_keyboard()
        )
        return

    lesson = Lesson.get(this_date, association.association_id)
    call = CallbackQuery(id=call.id, from_user=call.from_user, chat_instance=call.chat_instance, message=call.message, inline_message_id=call.inline_message_id, data=f"day|{this_date}|selected")
    if lesson is None:
        await show_lesson(call, state)
    
    lesson.change_description(None)

    await show_lesson(call, state)


async def show_lesson_files(call: CallbackQuery, state: FSMContext):
    user = await check_user(call.from_user, state)
    _, this_date, association_id = call.data.split("|")
    
    this_date = date.fromisoformat(this_date)
    association = Association.get(association_id)
    lesson = Lesson.get(this_date, association.association_id)
    
    if association is None:
        return await call.message.edit_text(
            "Ошибка, повторите выбор учителя или ученика в профиле и выберите день снова.",
            reply_markup=get_to_menu_keyboard()
        )
    
    if association.association_id != user.association_id:
        return await call.message.edit_text(
            "Ошибка, ваш учитель/ученик не совпадает с выбранным в профиле.",
            reply_markup=get_to_menu_keyboard()
        )
    
    files = [] if lesson is None else lesson.files()
    if len(files) > 0:
        for file in files:
            await call.message.answer_document(document=file.file_id)
        return await call.message.answer("Прикреплённые файлы", reply_markup=get_lesson_files_keyboard(this_date, association.association_id, files))

    await call.message.edit_text("Нет прикреплённых файлов", reply_markup=get_lesson_files_keyboard(this_date, association.association_id, files))

async def add_lesson_files(call: CallbackQuery, state: FSMContext):
    user = await check_user(call.from_user, state)
    _, this_date, association_id = call.data.split("|")
    
    this_date = date.fromisoformat(this_date)
    association = Association.get(association_id)
    lesson = Lesson.get(this_date, association.association_id)

    if association is None:
        return await call.message.answer(
            "Ошибка, повторите выбор учителя или ученика в профиле и выберите день снова.",
            reply_markup=get_to_menu_keyboard()
        )
    
    if association.association_id != user.association_id:
        return await call.message.answer(
            "Ошибка, ваш учитель/ученик не совпадает с выбранным в профиле.",
            reply_markup=get_to_menu_keyboard()
        )
    
    files = [] if lesson is None else lesson.files()
    if len(files) >= 8:
        return await call.message.edit_text(
            "Ошибка, файлов больше 8, удалите файлы, чтобы добавить другие.",
            reply_markup=get_add_lesson_files_keyboard(this_date, association.association_id)
        )

    await call.message.edit_text(
        "Общее кол-во файлов в уроке должно быть не больше 8. Каждый следующий документ будет загружен, но лишние файлы загружены не будут.",
        reply_markup=get_add_lesson_files_keyboard(this_date, association.association_id)
    )
    
    await state.set_state(Files.send)
    await state.set_data(data={"date": this_date, "association_id": association_id})


async def delete_lesson_file(call: CallbackQuery, state: FSMContext):
    user = await check_user(call.from_user, state)
    _, this_date, association_id, file_id = call.data.split("|")
    
    this_date = date.fromisoformat(this_date)
    association = Association.get(association_id)
    lesson = Lesson.get(this_date, association.association_id)
    
    if association is None:
        return await call.message.edit_text(
            "Ошибка, повторите выбор учителя или ученика в профиле и выберите день снова.",
            reply_markup=get_to_menu_keyboard()
        )
    
    if association.association_id != user.association_id:
        return await call.message.edit_text(
            "Ошибка, ваш учитель/ученик не совпадает с выбранным в профиле.",
            reply_markup=get_to_menu_keyboard()
        )

    lesson.delete_file(file_id)
    await call.message.edit_text(
        "Прикреплённые файлы",
        reply_markup=get_lesson_files_keyboard(this_date, association.association_id, lesson.files())
    )