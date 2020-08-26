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

    sql_list = """
        CREATE TABLE IF NOT EXISTS "List" (
            "@List" integer not null primary key,
            "Note" text not null,
            "MessageID" int not null
        );
    """
    sql_rss = """
        CREATE TABLE IF NOT EXISTS "Rss" (
            "Title" text not null primary key,
            "Date" date not null
        );
    """

    sql_message = """
        CREATE TABLE IF NOT EXISTS "LastMessage" (
            "MessageID" int not null primary key,
            "PublishDate" datetime not null
        );
    """

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql_list)
    conn.commit()
    cursor.execute(sql_rss)
    conn.commit()
    cursor.execute(sql_message)
    conn.commit()
    conn.close()


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


def select_last_message():
    """Получение последнего сообщения, отправленного ботом"""

    sql = """
        SELECT "MessageID", "PublishDate"
        FROM "LastMessage"
    """

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.close()

    return result


def insert_last_message(message_id):
    """Вставка id сообщения"""

    sql = """
        INSERT INTO "LastMessage"
        VALUES (:message_id, datetime('now'))
    """

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql, {'message_id': message_id})
    conn.commit()
    conn.close()


def update_last_message(message_id):
    """Обновление id последнео сообщения"""

    sql = """
        UPDATE "LastMessage"
        SET "MessageID" = :message_id, "PublishDate" = datetime('now')
    """

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql, {'message_id': message_id})
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
    conn.close()


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
    conn.close()


def delete_note(list_id: int) -> None:
    """Удаление заметки"""

    sql_delete = """
        DELETE FROM "List"
        WHERE "@List" = :list_id
    """

    sql_update = """
        UPDATE "List"
        SET "@List" = "@List" - 1
        WHERE   "@List" > :list_id
    """

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql_delete, {'list_id': list_id})
    conn.commit()
    cursor.execute(sql_update, {'list_id': list_id})
    conn.commit()
    conn.close()


def delete_all() -> None:
    """Очистка списка"""

    sql = '''DELETE FROM "List"'''

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()
