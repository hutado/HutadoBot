#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Клавиатуры
"""

from telebot import types


def delete_key():
    """
    Inline кнопка Очистить
    """

    keyboard = types.InlineKeyboardMarkup()
    delete_btn = types.InlineKeyboardButton(text='Очистить', callback_data='delete_all')
    keyboard.add(delete_btn)

    return keyboard


def confirm_key():
    """
    Inline кнопка Очистить
    """

    keyboard = types.InlineKeyboardMarkup()
    confirm_btn = types.InlineKeyboardButton(text='Уверены?', callback_data='delete_confirm')
    keyboard.add(confirm_btn)

    return keyboard
