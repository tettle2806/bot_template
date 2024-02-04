import sqlite3


class DataBase:
    def __init__(self):
        self.database = sqlite3.connect('GREEKFOOD.db', check_same_thread=False)

    def manager(self, sql, *args,
                fetchone: bool = False,
                fetchall: bool = False,
                commit: bool = False):
        with self.database as db:
            cursor = db.cursor()
            cursor.execute(sql, args)
            if commit:
                result = db.commit()
            if fetchone:
                result = cursor.fetchone()
            if fetchall:
                result = cursor.fetchall()
            return result

    def create_user_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS users(
            telegram_id BIGINT PRIMARY KEY,
            first_name VARCHAR(100),
            phone VARCHAR(20)
            )
        '''
        self.manager(sql, commit=True)

    def first_registration(self, telegram_id):
        sql = '''
              INSERT INTO users(telegram_id) VALUES (?)
              '''
        self.manager(sql, telegram_id, commit=True)

    def get_user_by_id(self, telegram_id):
        sql = '''
        SELECT * FROM users WHERE telegram_id = ?
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    def get_colum_phone(self, phone):
        sql = '''
            SELECT * FROM users WHERE phone = ?
        '''

        return self.manager(sql, phone, fetchone=True)

    def full_registration(self, first_name, phone, telegram_id):
        sql = '''
            UPDATE users
            SET
            first_name = ?,
            phone = ?
            WHERE telegram_id = ?
        '''
        self.manager(sql, first_name, phone, telegram_id, commit=True)

    def drop_user_by_id(self, telegram_id):
        sql = '''
            DELETE FROM users WHERE telegram_id = ?
        '''
        self.manager(sql, telegram_id, commit=True)

    def create_categories_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS categories(
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_title VARCHAR(50) UNIQUE
        )
        '''
        self.manager(sql, commit=True)

    def insert_categories(self):
        sql = '''
            INSERT INTO categories(category_title) VALUES
            ('СУВЛАКИ'),
            ('САЛАТЫ'),
            ('КЛАБ СЭНДВИЧ'),
            ('ВТОРЫЕ БЛЮДА'),
            ('ПИЦЦА'),
            ('БУРГЕРЫ'),
            ('СУПЫ'),
            ('ХОД-ДОГ'),
            ('СОУСЫ'),
            ('КАРТОШКА'),
            ('ХЛЕБ'),
            ('КОФЕ LAVAZZA'),
            ('ICE КОФЕ'),
            ('ФИРМЕННЫЕ ЧАИ'),
            ('ЛИМОНАДЫ'),
            ('СМУЗИ'),
            ('ФРЕШ'),
            ('КОКТЕЙЛИ'),
            ('ШЕЙКИ'),
            ('НАПИТКИ')
        '''
        self.manager(sql, commit=True)

    def get_categories(self):
        sql = '''
            SELECT category_title FROM categories
        '''
        return self.manager(sql, fetchall=True)

    def get_all_categories(self):
        sql = '''
            SELECT * FROM categories
        '''
        return self.manager(sql, fetchall=True)

    def get_id_by_categories(self, category):
        sql = '''
            SELECT category_id FROM categories WHERE category_title=?
        '''
        return self.manager(sql, category, fetchone=True)

    def get_category_by_id(self, category_id):
        sql = '''
            SELECT category_title FROM categories WHERE category_id=?
        '''
        return self.manager(sql, category_id, fetchone=True)

    def create_products_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS products(
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_title VARCHAR(50) UNIQUE,
            description VARCHAR(255),
            price INTEGER,
            image TEXT,
            category_id INTEGER REFERENCES categories(category_id)
            )
        '''
        self.manager(sql, commit=True)

    def insert_products(self):
        sql = '''
           INSERT INTO products(product_title, description, price, image, category_id) VALUES
        '''
        self.manager(sql, commit=True)

    def get_products_by_category(self, category_title):
        sql = '''
            SELECT product_title FROM products WHERE category_id = (
                SELECT category_id FROM categories WHERE category_title = ?
            )
        '''
        return self.manager(sql, category_title, fetchall=True)

    def select_all_id(self):
        sql = '''
            SELECT telegram_id FROM users
        '''
        return self.manager(sql, fetchall=True)

    def delete_product(self, product_name):
        sql = '''
            DELETE FROM products where product_title=?
        '''
        self.manager(sql, product_name, commit=True)

    def select_products_by_category(self, category_id):
        sql = '''
            SELECT product_title FROM products WHERE category_id=?
        '''
        return self.manager(sql, category_id, fetchall=True)

    def delete_category(self, category_name):
        sql = '''
            DELETE FROM categories WHERE category_title=?
        '''
        self.manager(sql, category_name, commit=True)

    def drop(self):
        sql = '''
            DROP TABLE products
        '''

        self.manager(sql, commit=True)

    def insert_alone_product(self, product_title, description, price, image, category_id):
        sql = '''
            INSERT INTO products(product_title, description, price, image, category_id) VALUES (?,?,?,?,?)
        '''
        self.manager(sql, product_title, description, price, image, category_id, commit=True)

    def get_products_by_title(self, product_title):
        sql = '''
            SELECT * FROM products WHERE product_title = ?
        '''

        return self.manager(sql, product_title, fetchone=True)

    def get_all_products(self):
        sql = '''
            SELECT product_title FROM products
        '''
        return self.manager(sql, fetchall=True)

    def delete_cart(self, telegram_id):
        sql = '''
            DELETE FROM cart WHERE telegram_id = ?
        '''
        self.manager(sql, telegram_id, commit=True)

    def delete_cart_products(self, cart_id):
        sql = '''
            DELETE FROM cart_products WHERE cart_id = ?
        '''
        self.manager(sql, cart_id, commit=True)

    def create_cart_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS cart(
            cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER REFERENCES users(telegram_id),
            location VARCHAR(255),
            total_quantity INTEGER DEFAULT 0,
            total_price INTEGER DEFAULT 0,
            address VARCHAR(255),
            enter_address VARCHAR(255)
        )
        '''
        self.manager(sql, commit=True)

    def get_enter_location(self, telegram_id):
        sql = '''
        SELECT enter_address FROM cart WHERE telegram_id = ?
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    def get_address(self, telegram_id):
        sql = '''
        SELECT enter_address FROM cart WHERE telegram_id = ?
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    def insert_enter_address(self, address, telegram_id):
        sql = '''
            UPDATE cart
            SET
            enter_address = ?
            WHERE telegram_id = ?
        '''
        self.manager(sql, address, telegram_id, commit=True)

    def insert_enter_location(self, address, telegram_id):
        sql = '''
            UPDATE cart
            SET
            address = ?
            WHERE telegram_id = ?
        '''
        self.manager(sql, address, telegram_id, commit=True)

    def insert_location(self, location, telegram_id):
        sql = '''
                    UPDATE cart
                    SET
                    location = ?
                    WHERE telegram_id = ?
                '''
        self.manager(sql, location, telegram_id, commit=True)

    def create_cart_products_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS cart_products(
            cart_product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            cart_id INTEGER REFERENCES cart(cart_id),
            product_name VARCHAR(100) NOT NULL,
            final_price INTEGER NOT NULL,
            quantity INTEGER NOT NULL,

            UNIQUE(cart_id, product_name)
        )
        '''
        self.manager(sql, commit=True)

    def create_cart_for_user(self, telegram_id):
        sql = '''
        INSERT INTO cart(telegram_id) VALUES (?)
        '''
        self.manager(sql, telegram_id, commit=True)

    def delete_product_user(self, cart_id, product):
        sql = '''
        DELETE FROM cart_products WHERE cart_id = ? AND product_name = ?
        '''
        return self.manager(sql, cart_id, product, commit=True)

    def get_cart_id(self, telegram_id):
        sql = '''
        SELECT cart_id FROM cart WHERE telegram_id = ?
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    def get_product_by_id(self, product_id):
        sql = '''
        SELECT product_title, price FROM products WHERE product_id = ?
        '''
        return self.manager(sql, product_id, fetchone=True)

    def insert_cart_product(self, cart_id, product_name, quantity, final_price):
        sql = '''
        INSERT INTO cart_products(cart_id, product_name, quantity, final_price)
        VALUES (?,?,?,?)
        '''
        self.manager(sql, cart_id, product_name, quantity, final_price, commit=True)

    def update_cart_product(self, cart_id, product_name, quantity, final_price):
        sql = '''
        UPDATE cart_products
        SET
        quantity = quantity + ?,
        final_price = final_price + ?
        WHERE product_name = ? AND cart_id = ?
        '''
        self.manager(sql, quantity, final_price, product_name, cart_id, commit=True)

    def update_cart_total_price_quantity(self, cart_id):
        sql = '''
            UPDATE cart
            SET 
            total_quantity = (
                SELECT SUM(quantity) FROM cart_products WHERE cart_id = ?
            ),
            total_price = (
                SELECT SUM(final_price) FROM cart_products WHERE cart_id = ?
            )
            WHERE cart_id = ?
        '''
        self.manager(sql, cart_id, cart_id, cart_id, commit=True)

    def get_cart_total_price_quantity(self, cart_id):
        sql = '''
            SELECT total_price, total_quantity FROM cart WHERE cart_id = ?
        '''
        return self.manager(sql, cart_id, fetchone=True)

    def get_cart_products_by_cart_id(self, cart_id):
        sql = '''
            SELECT * FROM cart_products WHERE cart_id = ?
        '''
        return self.manager(sql, cart_id, fetchall=True)

    def delete_err(self):
        sql = '''
            DELETE FROM cart_products WHERE cart_product_id = 1
        '''
        self.manager(sql, commit=True)

    def select_location(self, telegram_id):
        sql = '''
            SELECT location FROM cart WHERE telegram_id = ?
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    def drop_cart(self):
        sql = '''
            DROP TABLE cart
        '''

        self.manager(sql, commit=True)

    def create_status_bot(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS on_off(
            telegram_id BIGINT PRIMARY KEY,
            status VARCHAR(10) 
            )
        '''
        self.manager(sql, commit=True)

    def insert_status(self, status):
        sql = '''
            INSERT INTO on_off(telegram_id, status) VALUES
            ((660515831), (?))
        '''
        self.manager(sql, status, commit=True)

    def update_status(self, status):
        sql = '''
        UPDATE on_off
        SET
        status = ?
        WHERE telegram_id = 660515831
        '''
        self.manager(sql, status, commit=True)

    def select_status_bot(self):
        sql = '''
            SELECT status FROM on_off WHERE telegram_id = 660515831
        '''

        return self.manager(sql, fetchone=True)
