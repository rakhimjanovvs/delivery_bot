import sqlite3

# Подключение к БД
connection = sqlite3.connect('delivery.db', check_same_thread=False)
# Python + SQL
sql = connection.cursor()
# Создание таблицы
sql.execute('CREATE TABLE IF NOT EXISTS users (tg_id INTEGER, name TEXT, num TEXT);')
sql.execute('CREATE TABLE IF NOT EXISTS products (pr_id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'pr_name TEXT, pr_des TEXT, pr_count INTEGER, pr_price REAL, pr_photo TEXT);')
sql.execute('CREATE TABLE IF NOT EXISTS cart (user_id INTEGER, user_product TEXT, user_pr_amount INTEGER);')

# Клиентская сторона

## Методы пользователя

# Регистрация
def register(tg_id, name, num):
    sql.execute('INSERT INTO users VALUES (?, ?, ?);', (tg_id, name, num))
    # Фиксация
    connection.commit()

# Проверка на наличие поль
def check_user(tg_id):
    if sql.execute('SELECT * FROM users WHERE tg_id=?', (tg_id, )).fetchone():
        return True
    else:
        return False

## Методы для продуктов
# Получить все товары
def get_all_pr():
    return sql.execute('SELECT * FROM products;').fetchall()

# Вывод товаров для кнопок
def get_pr_buttons():
    return [i[:2] for i in get_all_pr() if i [3] > 0]

# Вывод определённого товара
def get_exact_pr(pr_id):
    return sql.execute('SELECT * FROM products WHERE pr_id=?;', (pr_id,)).fetchone()

# Вывод цены товара по названию
def get_pr_price(pr_name):
    return sql.execute('SELECT pr_price FROM products WHERE pr_name=?;', (pr_name,)).fetchone()[0]

## Методы корзины
# Добвление в корзины
def add_to_cart(user_id, user_product, user_pr_amount):
    sql.execute('INSERT INTO cart VALUES (?, ?, ?);', (user_id, user_product, user_pr_amount))
    # Фиксация изменений
    connection.commit()

# Очистка корзины
def clear_cart(user_id):
    sql.execute('DELETE FROM cart WHERE user_id=?;', (user_id,))
    # Фиксация изменений
    connection.commit()

# Вывод корзины
def show_cart(user_id):
    return sql.execute('SELECT * FROM cart WHERE user_id=?;', (user_id,)).fetchall()

# Оформление заказа
def make_order(user_id):
    # Получение товары, которые взял пользователь и их количество
    product_names = sql.execute('SELECT user_product FROM cart WHERE user_id=?;', (user_id,)).fetchall()
    product_counts = sql.execute('SELECT user_pr_amount FROM cart WHERE user_id=?;', (user_id,)).fetchall()

    # Получаем количества товаров на складе
    stock = [sql.execute('SELECT pr_count FROM products WHERE pr_name=?;', (i[0],)).fetchone() for i in product_names]

    totals = []

    for t in range(len(product_names)):
        totals.append(stock[t][0] - product_counts[t][0])

    for c in range(len(totals)):
        sql.execute('UPDATE products SET pr_count=? WHERE pr_name=?;', (totals[c], product_names[c][0]))

    # Фиксация изменений
    connection.commit()
    return stock, totals


# АДМИНСКАЯ СТОРОНА #
# Добавление продукта в БД
def add_pr_to_db(pr_name, pr_des, pr_count, pr_price, pr_photo):
    if (pr_name,) in sql.execute('SELECT pr_name FROM products').fetchall():
        return False
    else:
        sql.execute('INSERT INTO products (pr_name, pr_des, pr_count, pr_price, pr_photo) VALUES (?, ?, ?, ?, ?);', (pr_name, pr_des, pr_count, pr_price, pr_photo))
        # Фиксация изменений
        connection.commit()
