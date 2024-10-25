from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from database import Database
from recipes import RecipeGenerator
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('SCOON_TOKEN')

db = Database()
recipe_generator = RecipeGenerator(api_key=API_TOKEN)

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Добавить продукт", callback_data='add_product')],
        [InlineKeyboardButton("Добавить блюдо", callback_data='add_dish')],
        [InlineKeyboardButton("Список продуктов", callback_data='list_products')],
        [InlineKeyboardButton("Предложить рецепт", callback_data='suggest_recipe')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите действие:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'add_product':
        query.edit_message_text(text="Введите название продукта и срок годности в формате: название срок_годности")
        context.user_data['next_action'] = 'add_product'
    elif query.data == 'add_dish':
        query.edit_message_text(text="Введите название блюда и срок годности в формате: название срок_годности")
        context.user_data['next_action'] = 'add_dish'
    elif query.data == 'list_products':
        products = db.get_products()
        if not products:
            query.edit_message_text(text='В холодильнике нет продуктов.')
        else:
            product_list = '\n'.join([f'{name} - {expiration_date}' for name, expiration_date in products])
            query.edit_message_text(text=f'Продукты в холодильнике:\n{product_list}')
    elif query.data == 'suggest_recipe':
        products = db.get_products()
        if not products:
            query.edit_message_text(text='В холодильнике нет продуктов.')
        else:
            ingredients = [product[0] for product in products]
            recipe = recipe_generator.generate_recipe(ingredients)
            query.edit_message_text(text=f'Предлагаемый рецепт: {recipe}')

def handle_message(update: Update, context: CallbackContext) -> None:
    if 'next_action' in context.user_data:
        action = context.user_data['next_action']
        if action == 'add_product':
            args = update.message.text.split()
            if len(args) != 2:
                update.message.reply_text('Используйте формат: название срок_годности')
                return
            name, expiration_date = args
            db.add_product(name, expiration_date)
            update.message.reply_text(f'Продукт {name} добавлен с сроком годности {expiration_date}')
        elif action == 'add_dish':
            args = update.message.text.split()
            if len(args) != 2:
                update.message.reply_text('Используйте формат: название срок_годности')
                return
            name, eat_by_date = args
            db.add_dish(name, eat_by_date)
            update.message.reply_text(f'Блюдо {name} добавлено с сроком годности {eat_by_date}')
        del context.user_data['next_action']
