import psycopg2
from psycopg2 import sql
from utils.tokens import db_user, db_host, db_passwd

class Database:
    def __init__(self):
        """
        Инициализирует класс, подключается к БД.
        """
        
        self.conn = psycopg2.connect(
            user=f"{db_user}", password=f"{db_passwd}",
            host=f"{db_host}", port="5432",
            database="schoolproject"
            )
        self.cur = self.conn.cursor()
        self.conn.autocommit = True

    def start(self):
        """
        Создаёт таблицу users, если таковой не существует. Выводит всех пользователей в таблице.
        """
        
        with self.conn:
            self.create_tables()
            self.get_db()

    def create_tables(self):
        with self.conn:
            self.cur.execute(
                """
CREATE TABLE IF NOT EXISTS users(
    user_id SERIAL PRIMARY KEY UNIQUE NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    grade INTEGER,
    letter TEXT
);
"""
            )

    def get_db(self):
        """
        Выводит всю таблицу users из базы данных.

        Эта функция используется для вывода всех записей из таблицы users в базе данных.

        Параметры:
        - self: Объект класса Database, который содержит подключение к базе данных.

        Возвращаемое значение:
        - list: Список кортежей, где каждый кортеж содержит информацию о пользователе из таблицы users.

        Примечание:
        - Если в базе данных нет пользователей, функция вернет пустой список.
        """

        with self.conn:
            self.cur.execute("SELECT * FROM users")
            users = self.cur.fetchall()
            print(users)

    def custom(self):
        """
        Специальная функция, применяется и изменяется при каких-либо тестах.
        """

        with self.conn:
            pass

    def get_users(self):
        """
        Получает список всех пользователей из базы данных.

        Возвращает:
        list: Список кортежей, где каждый кортеж содержит идентификатор пользователя (user_id).

        Примечание:
        Если в базе данных нет пользователей, возвращается пустой список.
        """
        
        with self.conn:
            self.cur.execute("SELECT user_id FROM users")
            return self.cur.fetchall()

    def user_exists(self, user_id: int):
        """
        Проверяет, существует ли пользователь в базе данных по заданному идентификатору.

        Параметры:
        user_id (int): Идентификатор пользователя, который необходимо проверить.

        Возвращает:
        bool: True, если пользователь с указанным user_id существует в базе данных, иначе False.
        """
    
        with self.conn:
            self.cur.execute(
                "SELECT * FROM users WHERE user_id = %s",
                (user_id,)
            )
            return self.cur.fetchone() is not None

    def add_user(self, user_id: int):
        """
        Добавляет нового пользователя в базу данных по заданному идентификатору.

        Параметры:
        - user_id (int): Идентификатор пользователя, который необходимо добавить в базу данных.
        """

        with self.conn:
            self.cur.execute("INSERT INTO users (user_id) VALUES (%s)", (user_id,))
