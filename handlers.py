from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from data import get_random_word, add_unknown_word, get_texts, get_known_words, get_known_words

async def start_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton('Прочитать текст', callback_data ='read_text')]
        [InlineKeyboardButton('Посмотреть незнакомые слова', callback_data ='view_unknown_words')]
        [InlineKeyboardButton('Рандом', callback_data ='random_word')]
        [InlineKeyboardButton('Помощь', callback_data ='help')]
        [InlineKeyboardButton('Выход', callback_data ='exit')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привет! Выбери опцию:', reply_markup=reply_markup)

async def button_handler(update:Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'read_text':
        text = get_texts()[0]  
        await query.edit_message_text(text=text)
    elif query.data == 'view_unknown':
        unknown_words = ', '.join(get_known_words())
        await query.edit_message_text(text=f"Незнакомые слова: {unknown_words}")
    elif query.data == 'random_word':
        random_entry = get_random_word()
        await query.edit_message_text(f"Слово: {random_entry['word']}, Перевод: {random_entry['translation']}")
    elif query.data == 'help':
        await query.edit_message_text(text="Вы можете читать тексты и добавлять незнакомые слова.")
    elif query.data == 'exit':
        await query.edit_message_text(text="Вы вышли из операции.")

async def add_unknown_word_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    words = text.split()
    for word in words:
        if word not in get_known_words:
            add_unknown_word(word)
            await update.message.reply_text(f"Слово '{word}' добавлено в незнакомые слова.")

async def random_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random_entry = get_random_word()
    await update.message.reply_text(f"Слово: {random_entry['word']}, Перевод: {random_entry['translation']}")