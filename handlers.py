from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from data import DataManager
from database import get_db
import logging
import httpx

data_manager = DataManager()

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton('Получить случайное слово', callback_data='random_word')],
        [InlineKeyboardButton('Прочитать текст', callback_data='read_text')],
        [InlineKeyboardButton('Посмотреть незнакомые слова', callback_data='view_unknown_words')],
        [InlineKeyboardButton('Помощь', callback_data='help')],
        [InlineKeyboardButton('Викторина', callback_data='quiz')],
        [InlineKeyboardButton('Выход', callback_data='exit')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text('Выберите опцию:', reply_markup=reply_markup)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = await get_db()  
    await data_manager.load_words_from_db(session)  

    keyboard = [
        [InlineKeyboardButton('Получить случайное слово', callback_data='random_word')],
        [InlineKeyboardButton('Прочитать текст', callback_data='read_text')],
        [InlineKeyboardButton('Посмотреть незнакомые слова', callback_data='view_unknown_words')],
        [InlineKeyboardButton('Помощь', callback_data='help')],
        [InlineKeyboardButton('Викторина', callback_data='quiz')],
        [InlineKeyboardButton('Выход', callback_data='exit')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привет! Выбери опцию:', reply_markup=reply_markup)

async def random_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random_entry = data_manager.get_random_word()
    if random_entry:
        word = random_entry['word']
        translation = random_entry['translation']
        
        context.user_data['current_word'] = word
        context.user_data['current_translation'] = translation
        
        keyboard = [
            [InlineKeyboardButton('Добавить незнакомое слово', callback_data='add_unknown_word')],
            [InlineKeyboardButton('Получить другое слово', callback_data='random_word')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.answer()  
        await update.callback_query.message.reply_text(f"Слово: {word}, Перевод: {translation}", reply_markup=reply_markup)
    else:
        await update.callback_query.answer()  
        await update.callback_query.message.reply_text("Нет доступных слов.")

async def add_unknown_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_word = context.user_data.get('current_word')
    current_translation = context.user_data.get('current_translation')
    
    if current_word and current_translation:
        user_id = update.effective_user.id  
        data_manager.add_unknown_word(user_id, current_word)  
        await update.callback_query.answer()  
        await update.callback_query.message.reply_text(f"Слово '{current_word}' добавлено в незнакомые слова.")
    else:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text("Нет слова для добавления.")
    
    await main_menu(update, context)

        
async def view_unknown_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    unknown_words = ', '.join(data_manager.get_known_words())
    if unknown_words:
        await update.callback_query.message.reply_text(f"Незнакомые слова: {unknown_words}")
    else:
        await update.callback_query.message.reply_text("Нет незнакомых слов.")
    

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'add_unknown_word':
        await add_unknown_word(update, context)
    if query.data == 'read_text':
        text = data_manager.get_random_text()['text']  
        await query.edit_message_text(text=text)  
        await main_menu(update, context)  
    elif query.data == 'view_unknown_words':
        await view_unknown_words(update, context)
    elif query.data == 'help':
        await query.edit_message_text(text="Вы можете читать тексты и добавлять незнакомые слова.")
        await main_menu(update, context)  
    elif query.data == 'exit':
        await query.edit_message_text(text="Вы вышли из операции.")
        await main_menu(update, context)  
    elif query.data == 'quiz':
        await quiz_handler(update, context)
    elif query.data == 'random_word':
        await random_word(update, context)
    await main_menu(update, context)

async def fetch_quiz_question():
    url = "https://opentdb.com/api.php?amount=1&type=multiple" 
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        if data['response_code'] == 0:  
            question_data = data['results'][0]
            question = question_data['question']
            correct_answer = question_data['correct_answer']
            all_answers = question_data['incorrect_answers'] + [correct_answer]
            return question, correct_answer, all_answers
        else:
            logging.error("Ошибка при получении вопроса из API")
            return None, None, None

async def quiz_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer() 

        question, correct_answer, all_answers = await fetch_quiz_question()
        
        if question is None:
            await update.callback_query.message.reply_text("Не удалось получить вопрос викторины.")
            return

        context.user_data['correct_answer'] = correct_answer

        keyboard = [[InlineKeyboardButton(answer, callback_data=answer) for answer in all_answers]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.callback_query.message.reply_text(f"Вопрос: {question}", reply_markup=reply_markup)
    else:
        logging.warning("update.callback_query is None")
        await update.callback_query.message.reply_text("Не удалось получить вопрос викторины.")
    await main_menu(update, context)