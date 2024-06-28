from pymongo import MongoClient
from bson.objectid import ObjectId

# Підключення до MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['cats_database']  # Назва вашої бази даних
collection = db['cats_collection']  # Назва вашої колекції

# Читання всіх записів з колекції
def read_all_cats():
    cats = collection.find()
    for cat in cats:
        print(cat)

# Читання інформації про конкретного кота за ім'ям
def read_cat_by_name(name):
    cat = collection.find_one({"name": name})
    if cat:
        print(cat)
    else:
        print(f"Кіт з ім'ям '{name}' не знайдено.")

# Оновлення віку кота за ім'ям
def update_cat_age(name, new_age):
    result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.modified_count > 0:
        print(f"Вік кота '{name}' оновлено до {new_age} років.")
    else:
        print(f"Кіт з ім'ям '{name}' не знайдено.")

# Додавання нової характеристики до списку features кота за ім'ям
def add_cat_feature(name, new_feature):
    result = collection.update_one({"name": name}, {"$push": {"features": new_feature}})
    if result.modified_count > 0:
        print(f"Додано нову характеристику '{new_feature}' коту '{name}'.")
    else:
        print(f"Кіт з ім'ям '{name}' не знайдено.")

# Видалення запису з колекції за ім'ям тварини
def delete_cat_by_name(name):
    result = collection.delete_one({"name": name})
    if result.deleted_count > 0:
        print(f"Кіт з ім'ям '{name}' видалено з колекції.")
    else:
        print(f"Кіт з ім'ям '{name}' не знайдено.")

# Видалення всіх записів з колекції
def delete_all_cats():
    result = collection.delete_many({})
    print(f"Видалено {result.deleted_count} записів.")

if __name__ == "__main__":
    # Приклад викликів функцій
    read_all_cats()
    read_cat_by_name("barsik")
    update_cat_age("barsik", 4)
    add_cat_feature("barsik", "муркотливий")
    delete_cat_by_name("barsik")
    delete_all_cats()

