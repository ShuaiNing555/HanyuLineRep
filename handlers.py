from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler
from data import data_manager
from database import get_db
import random 
import requests

async def start_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    async with get_db() as session:
        await data_manager.load_words_from_db(session)

    keyboard = [
        [InlineKeyboardButton('Прочитать текст', callback_data ='read_text')]
        [InlineKeyboardButton('Посмотреть незнакомые слова', callback_data ='view_unknown_words')]
        [InlineKeyboardButton('Рандом', callback_data ='random_word')]
        [InlineKeyboardButton('Помощь', callback_data ='help')]
        [InlineKeyboardButton('Выход', callback_data ='exit')]
        [InlineKeyboardButton('Викторина', callback_data= 'quiz')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привет! Выбери опцию:', reply_markup=reply_markup)

async def button_handler(update:Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'read_text':
        text = data_manager.get_random_text()['text'] 
        await query.edit_message_text(text=text)
    elif query.data == 'view_unknown_words':
        unknown_words = ', '.join(data_manager.get_known_words())
        await query.edit_message_text(text=f"Незнакомые слова: {unknown_words}")
    elif query.data == 'random_word':
        random_entry = data_manager.get_random_word()
        await query.edit_message_text(f"Слово: {random_entry['word']}, Перевод: {random_entry['translation']}")
    elif query.data == 'help':
        await query.edit_message_text(text="Вы можете читать тексты и добавлять незнакомые слова.")
    elif query.data == 'exit':
        await query.edit_message_text(text="Вы вышли из операции.")
    elif query.data == 'quiz':
        await quiz_handler(update, context)

async def add_unknown_word_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    words = text.split()
    for word in words:
        if word not in data_manager.get_known_words():
            data_manager.add_unknown_word(word)  
            await update.message.reply_text(f"Слово '{word}' добавлено в незнакомые слова.")

async def quiz_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get("https://opentdb.com/api.php?amount=1&type=multiple")
    if response.status_code == 200:
        data = response.json()
        question = data['results'][0]['question']
        correct_answer = data['results'][0]['correct_answer']
        incorrect_answers = data['results'][0]['incorrect_answers']
        all_answers = incorrect_answers + [correct_answer]
        random.shuffle(all_answers)

        context.user_data['correct_answer'] = correct_answer

        keyboard = [[InlineKeyboardButton(answer, callback_data=answer) for answer in all_answers]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(f"Вопрос: {question}", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Не удалось получить вопрос викторины.")

async def check_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_answer = update.callback_query.data
    correct_answer = context.user_data.get('correct_answer')

    if user_answer == correct_answer:
        await update.callback_query.edit_message_text("Правильно")
    else:
        await update.callback_query.edit_message_text(f"Неправильно. Правильный ответ: {correct_answer}.")