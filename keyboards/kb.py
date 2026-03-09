from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from random import randint

class Keyboard:
    def __init__(self):
        self.cache = {}
        self.buttons = [InlineKeyboardButton(text="Умножение на 2", callback_data="x2"),
                   InlineKeyboardButton(text="Умножение на 3", callback_data="x3"),
                   InlineKeyboardButton(text="Умножение на 4", callback_data="x4"),
                   InlineKeyboardButton(text="Умножение на 5", callback_data="x5"),
                   InlineKeyboardButton(text="Умножение на 6", callback_data="x6"),
                   InlineKeyboardButton(text="Умножение на 7", callback_data="x7"),
                   InlineKeyboardButton(text="Умножение на 8", callback_data="x8"),
                   InlineKeyboardButton(text="Умножение на 9", callback_data="x9"),
                   InlineKeyboardButton(text="Вся таблица", callback_data="all_table")]
    

    def multiplicate(self):
        kb_builder = InlineKeyboardBuilder()
        
        kb_builder.add(*self.buttons)
        kb_builder.adjust(1)

        return kb_builder.as_markup()
    
    
    def generate_multiplicate_answers(self, ans):
        if ans in self.cache:
            return self.cache[ans]
        used_answers = {ans}
        while len(used_answers) < 12:
            if 10 <= ans <= 99:
                used_answers.add(randint(10, ans + 12))
            else:
                used_answers.add(randint(1, ans + 12))

        buttons = [KeyboardButton(text=str(a)) for a in sorted(used_answers)]

        keyboard_with_answers = ReplyKeyboardMarkup(
            keyboard=[buttons[i:i+3] for i in range(0, 12, 3)],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        self.cache[ans] = keyboard_with_answers
        return keyboard_with_answers