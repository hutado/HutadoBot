#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Основной файл бота
В начале обработчки команд
В конце запуск бота
"""


import telebot
import datetime

import database
import keyboard
from config import BOT_TOKEN


BOT = telebot.TeleBot(BOT_TOKEN)


def _send_message(chat_id: int, text: str, _keyboard='') -> None:
    """Обертка отправки сообщений"""

    last_message = database.select_last_message()
    if last_message:
        date_ = datetime.datetime.strptime(last_message[1], '%Y-%m-%d %H:%M:%S')
        if date_ > datetime.datetime.now() - datetime.timedelta(3):
            BOT.delete_message(chat_id, last_message[0])

    result = BOT.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode='Markdown',
        reply_markup=_keyboard
    )

    if last_message:
        database.update_last_message(result.message_id)
    else:
        database.insert_last_message(result.message_id)

###################
#    Commands     #
###################

@BOT.callback_query_handler(func=lambda call: True)
def callback_inline(call: telebot.types.CallbackQuery) -> None:
    """Обработка Inline кнопок"""

    _keyboard = ''

    if call.data == 'delete_all':
        _keyboard = keyboard.confirm_key()

    elif call.data == 'delete_confirm':
        database.delete_all()

    text = database.select_notes()
    BOT.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=_keyboard
    )


@BOT.message_handler(commands=['start'])
def start_commnad(message: telebot.types.Message) -> None:
    """Обработка команды /start"""

    database.create_database()

    _send_message(message.chat.id, database.select_notes(), keyboard.delete_key())


@BOT.message_handler(commands=['list'])
def list_commnad(message: telebot.types.Message) -> None:
    """Обработка команды /list"""

    _send_message(message.chat.id, database.select_notes(), keyboard.delete_key())


@BOT.message_handler(content_types=["text"])
def standart_message(message: telebot.types.Message) -> None:
    """Добавление/изменение сообщения"""

    if message.reply_to_message is not None:
        database.update_note(message.text, message.reply_to_message.message_id)
    else:
        database.insert_note(message.text, message.message_id)

    _send_message(message.chat.id, database.select_notes(), keyboard.delete_key())


###################
# Starting Server #
###################

if __name__ == '__main__':
    BOT.polling(none_stop=True)
