import psycopg2
from utils.tokens import db_user, db_host, db_passwd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

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
        Выводит количество всех пользователей в таблице users.
        """
        
        # self.create_tables()
        # self.custom()
        # self.get_db()
        self.get_count_of_users()
    def create_tables(self):
        with self.conn:
            self.cur.execute(
                """
CREATE TABLE IF NOT EXISTS users(
    user_id BIGINT PRIMARY KEY UNIQUE NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    grade INTEGER DEFAULT 0,
    letter TEXT DEFAULT ''
);
"""
            )
            self.cur.execute(
                """
CREATE TABLE IF NOT EXISTS groups(
    group_id BIGINT PRIMARY KEY UNIQUE NOT NULL,
    grade INTEGER DEFAULT 0,
    letter TEXT DEFAULT ''
);
"""
            )

    def get_count_of_users(self):
        with self.conn:
            self.cur.execute("SELECT COUNT(*) FROM users WHERE is_active = TRUE;")
            count = self.cur.fetchone()[0]
            logging.info(f"Количество активных пользователей: {count}")

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
            self.cur.execute("SELECT * FROM users;")
            users = self.cur.fetchall()
            self.cur.execute("SELECT * FROM groups;")
            groups = self.cur.fetchall()
            
            logging.info(users, '\n', groups)

    def custom(self):
        """
        Специальная функция, применяется и изменяется при каких-либо тестах.
        """

        with self.conn:
            self.cur.execute("ALTER TABLE users ALTER COLUMN grade SET DEFAULT 0;")
            self.cur.execute("ALTER TABLE users ALTER COLUMN letter SET DEFAULT '';")
            self.cur.execute("UPDATE users SET grade = 0 WHERE grade IS NULL;")
            self.cur.execute("UPDATE users SET letter = '' WHERE letter IS NULL;")
            logging.info("Дефолтные значения добавлены.")
        
    def get_users(self):
        """
        Получает список всех пользователей из базы данных.

        Возвращает:
        list: Список кортежей, где каждый кортеж содержит идентификатор пользователя (user_id).

        Примечание:
        Если в базе данных нет пользователей, возвращается пустой список.
        """
        
        with self.conn:
            self.cur.execute("SELECT user_id FROM users;")
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
                "SELECT * FROM users WHERE user_id = %s;",
                (user_id,)
            )
            return self.cur.fetchone() is not None

    def add_user(self, user_id: int, grade: int, letter: str):
        """
        Добавляет нового пользователя в базу данных по заданному идентификатору.

        Параметры:
        - user_id (int): Идентификатор пользователя, который необходимо добавить в базу данных.
        - grade (int): Значение для поля grade.
        - letter (str): Значение для поля letter.
        """
        
        with self.conn:
            self.cur.execute("INSERT INTO users (grade, letter, user_id) VALUES (%s, %s, %s);", (grade, letter, user_id,))

    def update_user(self, user_id: int, grade: int, letter: str):
        """
        Обновляет данные о пользователе в базе данных по заданному идентификатору.
        
        Параметры:
        - user_id (int): Идентификатор пользователя, для которого необходимо изменить данные.
        - grade (int): Новое значение для поля grade.
        - letter (str): Новое значение для поля letter.
        """
        with self.conn:  
            self.cur.execute("UPDATE users SET grade = %s, letter = %s WHERE user_id = %s;", (grade, letter, user_id,))

    def get_user(self, user_id: int):
        """
        Получает данные о пользователе из базы данных по заданному идентификатору.

        Параметры:
        - user_id (int): Идентификатор пользователя, для которого необходимо получить данные.

        Возвращает:
        - tuple: Кортеж, содержащий данные о пользователе из таблицы users.
        
        Примечание:
        - Если пользователь с указанным user_id не найден, возвращается None.
        """
    
        with self.conn:
            self.cur.execute(
                "SELECT * FROM users WHERE user_id = %s;",
                (user_id,)
            )
            return self.cur.fetchone()

    def get_grade(self, user_id: int):
        """"""
        with self.conn:
            self.cur.execute(
                "SELECT grade, letter FROM users WHERE user_id = %s;",
                (user_id,)
            )
            return self.cur.fetchone()

    def get_active_users(self):
        """"""
        with self.conn:
            self.cur.execute("SELECT user_id, grade, letter FROM users WHERE is_active = TRUE;")
            return self.cur.fetchall()
    
    def get_user_for_schedule(self, user_id):
        """"""
        with self.conn:
            self.cur.execute(
                "SELECT user_id, grade, letter FROM users WHERE user_id = %s AND is_active = TRUE;",
                (user_id,)
            )
            return self.cur.fetchone()
    
    def get_groups(self):
        """"""
        with self.conn:
            self.cur.execute("SELECT * FROM groups;")
            return self.cur.fetchall()
    
    def add_group(self, group, grade, letter):
        """"""
        with self.conn:
            self.cur.execute("INSERT INTO groups (group_id, grade, letter) VALUES (%s, %s, %s);", (group, grade, letter,))
    
    def update_group(self, group_id, grade, letter):
        with self.conn:
            self.cur.execute("UPDATE groups SET grade = %s, letter = %s WHERE group_id = %s;", (grade, letter, group_id,))
    
    def get_group(self, group_id):
        with self.conn:
            self.cur.execute("SELECT * FROM groups WHERE group_id = %s;", (group_id,))
            return self.cur.fetchone()