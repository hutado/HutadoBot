#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Основной файл бота
В начале обработчки команд
В конце запуск бота
"""

import os
import telebot

import database
import keyboard
from config import BOT_TOKEN



BOT = telebot.TeleBot(BOT_TOKEN)


def _send_message(chat_id, text, _keyboard=''):
    """
    Обертка отправки сообщений
    """

    BOT.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode='Markdown',
        reply_markup=_keyboard
    )

###################
#    Commands     #
###################

@BOT.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """
    Обработка Inline кнопок
    """

    user_id = call.message.chat.id
    _keyboard = ''

    if call.data == 'delete_all':
        _keyboard = keyboard.confirm_key()

    elif call.data == 'delete_confirm':
        database.delete_all(user_id)

    text = database.select_notes(user_id)
    BOT.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text=text, reply_markup=_keyboard)


@BOT.message_handler(commands=['start'])
def start_commnad(message):
    """
    Обработка команды /start
    """

    user_id = message.chat.id

    database.create_database(user_id)
    text = database.select_notes(user_id)

    _send_message(user_id, text, keyboard.delete_key())


@BOT.message_handler(content_types=["text"])
def standart_message(message):
    """
    Добавление/изменение сообщения
    """

    user_id = message.chat.id

    if message.reply_to_message is not None:
        database.update_note(user_id, message.text, message.reply_to_message.message_id)
    else:
        database.insert_note(user_id, message.text, message.message_id)

    text = database.select_notes(user_id)
    BOT.delete_message(user_id, message.message_id - 1)

    _send_message(user_id, text, keyboard.delete_key())


###################
# Starting Server #
###################

if __name__ == '__main__':
    BOT.polling(none_stop=True)
