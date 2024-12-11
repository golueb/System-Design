import time
from pymongo import MongoClient
from passlib.context import CryptContext

# Настройка MongoDB
MONGO_URI = "mongodb://mongo:27017/"
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client["leadertask"]
tasks_collection = mongo_db["tasks"]

# Настройка паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Загрузка тестовых данных
def load_test_data():
    # Проверка существования задачи перед добавлением
    def add_task(goal_id, title, description):
        task = tasks_collection.find_one({"title": title})
        if not task:
            task_data = {
                "goal_id": goal_id,
                "title": title,
                "description": description,
            }
            tasks_collection.insert_one(task_data)

    # Создание тестовых задач
    add_task(1, "Read Python documentation", "Read the official Python documentation")
    add_task(2, "Create a FastAPI project", "Create a simple FastAPI project")

def wait_for_db(retries=10, delay=5):
    for _ in range(retries):
        try:
            mongo_client.admin.command('ismaster')
            print("MongoDB is ready!")
            return
        except Exception as e:
            print(f"MongoDB not ready yet: {e}")
            time.sleep(delay)
    raise Exception("Could not connect to MongoDB")

if __name__ == "__main__":
    wait_for_db()
    load_test_data()