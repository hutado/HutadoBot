#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Методы для работы с БД
"""

import sqlite3
from datetime import date
from config import DATABASE


def create_database() -> None:
    """Создание БД и таблиц, если их еще нет"""

    sql = """
        CREATE TABLE IF NOT EXISTS "List" (
            "@List" integer not null primary key,
            "Note" text not null,
            "MessageID" int not null
        );
        CREATE TABLE IF NOT EXISTS "Rss" (
            "Title" text not null primary key,
            "Date" date not null
        );
    """

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()


def article_in_db(title_: str, date_: date) -> bool:
    """Проверка наличия постов в БД"""

    sql = """
        SELECT *
        FROM "Rss"
        WHERE "Title" = :title AND "Date" = :date_
    """

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql, {'title': title_, 'date_': date_})
    result = cursor.fetchall()
    conn.close()

    return bool(result)


def add_article_to_db(title_: str, date_: date) -> None:
    """Добавление постов в БД"""

    sql = """
        INSERT INTO "Rss"
        VALUES (:title, :date_)
    """

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql, {'title': title_, 'date_': date_})
    conn.commit()
    conn.close()


def select_notes() -> str:
    """Получение списка заметок"""

    sql = """
        SELECT "@List", "Note"
        FROM "List"
    """

    message = ''
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    for row in cursor.execute(sql):
        message += '{}. {}\n'.format(row[0], row[1])

    return message or 'У вас нет заметок'


def insert_note(note: str, message_id: int) -> None:
    """Добавление заметки"""

    sql = """
        INSERT INTO "List"
        VALUES (
            (SELECT max("@List") + 1 FROM "List")
            , :note
            , :message_id
        )
    """

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql, {'note': note, 'message_id': message_id})
    conn.commit()


def update_note(note: str, message_id: int) -> None:
    """Изменение заметки"""

    sql = """
        UPDATE "List"
        SET "Note" = :note
        WHERE "MessageID" = :message_id
    """

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql, {'note': note, 'message_id': message_id})
    conn.commit()


def delete_all() -> None:
    """Очистка списка"""

    sql = '''DELETE FROM "List"'''

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
