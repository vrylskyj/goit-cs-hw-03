import psycopg2
from faker import Faker

# Налаштування підключення до бази даних
try:
    conn = psycopg2.connect(
        dbname="postgres",     # Назва вашої бази даних PostgreSQL
        user="postgres",       # Користувач PostgreSQL
        password="mysecretpassword",  # Пароль користувача PostgreSQL
        host="localhost",      # Адреса хоста PostgreSQL (зазвичай localhost)
        port="5432"            # Порт PostgreSQL (зазвичай 5432)
    )
except Exception as e:
    print(f"Не вдалося підключитися до бази даних: {e}")
    exit(1)

cursor = conn.cursor()

# Ініціалізація Faker
fake = Faker()

# Кількість записів, які потрібно створити
num_users = 10
num_tasks = 30

# Створення таблиць, якщо вони ще не існують
try:
    # Створення таблиці users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            fullname VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        )
    """)

    # Створення таблиці status
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS status (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        )
    """)

    # Додавання початкових статусів
    cursor.execute("INSERT INTO status (name) VALUES ('new'), ('in progress'), ('completed') ON CONFLICT DO NOTHING")

    # Створення таблиці tasks
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            status_id INTEGER REFERENCES status(id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    
    # Підтвердження змін у структурі бази даних
    conn.commit()

except psycopg2.Error as e:
    print(f"Помилка при створенні таблиць: {e}")
    conn.rollback()
    exit(1)

# Створення випадкових користувачів
try:
    for _ in range(num_users):
        fullname = fake.name()
        email = fake.unique.email()
        cursor.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))
    conn.commit()

except psycopg2.Error as e:
    print(f"Помилка при вставці користувачів: {e}")
    conn.rollback()

# Створення випадкових завдань
try:
    for _ in range(num_tasks):
        title = fake.sentence(nb_words=6)
        description = fake.text()
        status_id = fake.random_int(min=1, max=3)
        user_id = fake.random_int(min=1, max=num_users)
        cursor.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                       (title, description, status_id, user_id))
    conn.commit()

except psycopg2.Error as e:
    print(f"Помилка при вставці завдань: {e}")
    conn.rollback()

finally:
    # Закриття курсора та підключення
    cursor.close()
    conn.close()

    print(f"Inserted {num_users} users and {num_tasks} tasks into the database.")
