import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import TOKEN, SUPERADMIN_ID
from database import add_question, delete_all_questions, get_random_questions

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()
permission_text = "⛔ You do not have permission to use this command!"
text_add_quessuccess="✅ Question added successfully!"
# text_add_questext = "❌ Please write your question after /add_questions."
text_delete_success = "✅ All questions have been deleted!"
text_no_quest = "❌ No questions have been added yet."

def main_menu(is_admin=False):
    keyboard = InlineKeyboardBuilder()

    if is_admin:
        keyboard.button(text="➕ Add Questions", callback_data="add_question")
        keyboard.button(text="🗑️ Delete all questions", callback_data="delete_all")

    keyboard.button(text="🎯 Start test", callback_data="start_test")
    keyboard.button(text="🔄 Update", callback_data="refresh_menu")

    return keyboard.as_markup()


# 🔰 Botni ishga tushirish
@dp.message(lambda message: message.text == "/start")
async def start_handler(message: Message):
    user_first_name = message.from_user.first_name
    is_admin = message.from_user.id == SUPERADMIN_ID
    await message.answer(f"Hello, {user_first_name}! \nWelcome to the SmartBola 😊 \n"
            "To start the test, send the command /start_test"
            "\nGood luck!👇",reply_markup=main_menu(is_admin))


# 🎯 Testni boshlash
@dp.callback_query(lambda call: call.data == "start_test")
async def start_test_handler(call: CallbackQuery):
    questions = get_random_questions(5)
    if questions:
        await call.message.answer("\n\n".join(questions))
    else:
        await call.message.answer(text_no_quest)


# ➕ Savol qo‘shish (faqat superadmin uchun)
@dp.callback_query(lambda call: call.data == "add_question")
async def add_question_prompt(call: CallbackQuery):
    if call.from_user.id != SUPERADMIN_ID:
        await call.answer(permission_text, show_alert=True)
        return

    await call.message.answer("📝 Send me new questions:")
    dp.message.register(process_add_question)


async def process_add_question(message: Message):
    if message.from_user.id != SUPERADMIN_ID:
        return

    add_question(message.text)
    await message.answer(text_add_quessuccess, reply_markup=main_menu(True))


# 🗑️ Barcha savollarni o‘chirish (faqat superadmin)
@dp.callback_query(lambda call: call.data == "delete_all")
async def delete_all_handler(call: CallbackQuery):
    if call.from_user.id != SUPERADMIN_ID:
        await call.answer(permission_text, show_alert=True)
        return

    delete_all_questions()
    await call.message.answer(text_delete_success, reply_markup=main_menu(True))


# 🔄 Yangilash
@dp.callback_query(lambda call: call.data == "refresh_menu")
async def refresh_menu(call: CallbackQuery):
    is_admin = call.from_user.id == SUPERADMIN_ID
    await call.message.edit_text("🔄 Updated! Main menu:", reply_markup=main_menu(is_admin))


# 🚀 Botni ishga tushirish
async def main():
    await dp.start_polling(bot)
    return loop.run_until_complete(main)


if __name__ == "__main__":
    asyncio.run(main())