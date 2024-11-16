from ..loader import bot
from telebot.types import Message

@bot.message_handler(commands=['/start'])
def reaction_start(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    bot.send_message(chat_id, f'Salom, Bing chilling ukyam, {message.from_user.first_name}')
