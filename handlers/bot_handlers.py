from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from keyboards.kb import Keyboard
from aiogram.fsm.context import FSMContext
from collections import defaultdict
from random import randint, choice


from math_examples.creating_examples import generate_examples_and_keyboards, generate_examples_and_kb_full_table
from states_floder.states import MultiplyState
from database.db import DatabaseBot


user_router = Router()
user_db = DatabaseBot()
kb_class = Keyboard()
mul_table = defaultdict(int, {"1":[[1,1,1],[1,2,2],[1,3,3],[1,4,4],[1,5,5],[1,6,6],[1,7,7],[1,8,8],[1,9,9]],"2":[[2,1,2],[2,2,4],[2,3,6],[2,4,8],[2,5,10],[2,6,12],[2,7,14],[2,8,16],[2,9,18]],"3":[[3,1,3],[3,2,6],[3,3,9],[3,4,12],[3,5,15],[3,6,18],[3,7,21],[3,8,24],[3,9,27]],"4":[[4,1,4],[4,2,8],[4,3,12],[4,4,16],[4,5,20],[4,6,24],[4,7,28],[4,8,32],[4,9,36]],"5":[[5,1,5],[5,2,10],[5,3,15],[5,4,20],[5,5,25],[5,6,30],[5,7,35],[5,8,40],[5,9,45]],"6":[[6,1,6],[6,2,12],[6,3,18],[6,4,24],[6,5,30],[6,6,36],[6,7,42],[6,8,48],[6,9,54]],"7":[[7,1,7],[7,2,14],[7,3,21],[7,4,28],[7,5,35],[7,6,42],[7,7,49],[7,8,56],[7,9,63]],"8":[[8,1,8],[8,2,16],[8,3,24],[8,4,32],[8,5,40],[8,6,48],[8,7,56],[8,8,64],[8,9,72]],"9":[[9,1,9],[9,2,18],[9,3,27],[9,4,36],[9,5,45],[9,6,54],[9,7,63],[9,8,72],[9,9,81]]})


@user_router.message(CommandStart())
async def start_bot(message: Message):
    keyboard = kb_class.multiplicate()
    await user_db.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    await message.answer(text=f"Привет, {message.from_user.first_name}! 🎓 С моей помощью ты выучишь таблицу умножения быстро и легко. Давай тренироваться.", reply_markup=keyboard)


@user_router.message(Command(commands="help"))
async def help(message: Message):
    await message.answer('''📖 <b>Как пользоваться ботом</b>\n
Основные разделы меню:\n
🎓 <b>Тренировка</b> - Главный раздел. Выбирай конкретные числа и начинай решать примеры.\n
📊 <b>Мои достижения</b> - Твоя личная статистика: количество решенных примеров, процент и количество правильных ответов.\n
🏆 <b>Зал славы</b> - Список лучших игроков. Решай примеры лучше всех, чтобы попасть в зал славы и занять почетное место в пятерке лидеров!\n
🆘 <b>Помощь</b> - Как пользоваться ботом.\n
<b>Совет:</b> чем регулярнее ты тренируешься, тем выше твоя позиция в глобальном рейтинге!''', parse_mode="HTML")


@user_router.callback_query(F.data == "all_table")
async def mul_all_table(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.edit_reply_markup(reply_markup=None)

    examples, keyboard_with_answers = await generate_examples_and_kb_full_table(kb_class)

    await state.update_data(examples = examples, current_step = 1, amount_correctly_solved_examples = 0, keyboard_with_answers = keyboard_with_answers)

    num1, num2, ans = examples[0]

    await callback.message.answer(text=f"{num1} × {num2} = ?", reply_markup=keyboard_with_answers[0])
    await state.set_state(MultiplyState.answering)



@user_router.callback_query(F.data.startswith("x"))
async def mul_on_certain_num(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.edit_reply_markup(reply_markup=None)

    factor = int(callback.data[1])
    examples, keyboard_with_answers = await generate_examples_and_keyboards(factor, kb_class)

    await state.update_data(examples = examples, current_step = 1, amount_correctly_solved_examples = 0, keyboard_with_answers = keyboard_with_answers)

    num1, num2, ans = examples[0]

    await callback.message.answer(text=f"{num1} × {num2} = ?", reply_markup=keyboard_with_answers[0])
    await state.set_state(MultiplyState.answering)


@user_router.message(MultiplyState.answering)
async def check_and_give_answers(message: Message, state: FSMContext):
    data = await state.get_data()
    step = data["current_step"]
    examples = data["examples"]
    amount_correct = data["amount_correctly_solved_examples"]
    right_answer = examples[step - 1][2]

    if not message.text.isdigit():
        await message.reply("Выбери ответ в виде цифры.")
        return

    if int(message.text) == right_answer:
        await message.reply("✅ Правильно!", reply_markup=ReplyKeyboardRemove())
        amount_correct += 1
        await user_db.update_stats(message.from_user.id, True)
    else:
        await message.reply(
            f"❌ Неверно. Правильный ответ: <b>{right_answer}</b>", reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
        await user_db.update_stats(message.from_user.id, False)

    if step < 10:
        step += 1
        await state.update_data(current_step=step, amount_correctly_solved_examples=amount_correct)
        num1, num2, ans = examples[step - 1]
        keyboard = data["keyboard_with_answers"][step - 1]
        await message.answer(text=f"{num1} × {num2} = ?", reply_markup=keyboard)
    else:
        await message.answer(f"Тренировка завершена.\nТвой результат:\n✅ Верно: {amount_correct} из 10")
        await state.clear()


@user_router.message(Command(commands="top"))
async def get_top_users(message: Message):
    top_users = await user_db.get_user_stats()
    text = "🏆 <b>Топ 5 легенд умножения:</b>\n\n"
    for i, (first_name, score) in enumerate(top_users, start=1):
        name = first_name
        text += f"{i}. {name} - {score} ✅\n"
    
    text = text.replace("1.", "1. 🥇").replace("2.", "2. 🥈").replace("3.", "3. 🥉").replace("4.", "4. 🎉").replace("5.", "5. 🎉")
    place, correctly_solved_examples = await user_db.check_position_of_leaderboard(message.from_user.id)

    if place > 5:
        text += f"\n\n📊 <b>Твой результат:</b>\n{place} место - {correctly_solved_examples} ✅\n"
        text += "<i>Продолжай решать, чтобы попасть в топ!</i>"
    await message.answer(text, parse_mode="HTML")


@user_router.message(Command(commands="profile"))
async def view_profile(message: Message):
    profile = await user_db.get_profile_statistics(message.from_user.id)
    for row in profile:
        amount_solved_examples, amount_correctly_solved_examples, first_name = row
    text = f"📊 {first_name}\n\n"
    text += f"💪 Решено примеров: {amount_solved_examples}\n"
    text += f"✅ Верных ответов: {amount_correctly_solved_examples}\n"

    if amount_correctly_solved_examples != 0:
        text += f"🎯 Точность: {round(amount_correctly_solved_examples / amount_solved_examples * 100)}%\n"
    else:
        text += f"🎯 Точность: {0}%\n"

    place, correctly_solved_examples = await user_db.check_position_of_leaderboard(message.from_user.id)
    text += f"🏆 Место в рейтинге: {place}"

    await message.answer(text=text)