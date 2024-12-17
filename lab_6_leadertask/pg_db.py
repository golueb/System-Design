import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from jwt import Base, UserDB, GoalDB
from passlib.context import CryptContext

# Настройка PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:qwerty@db/leadertask"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Настройка паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Загрузка тестовых данных
def load_test_data():
    db = SessionLocal()

    # Проверка существования пользователя перед добавлением
    def add_user(username, first_name, last_name, hashed_password, email):
        user = db.query(UserDB).filter(UserDB.username == username).first()
        if not user:
            user = UserDB(
                username=username,
                first_name=first_name,
                last_name=last_name,
                hashed_password=hashed_password,
                email=email,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    # Создание мастер-пользователя
    admin_user = add_user(
        username="admin",
        first_name="Admin",
        last_name="Admin",
        hashed_password=pwd_context.hash("secret"),
        email="admin@example.com",
    )

    # Создание тестовых пользователей
    user1 = add_user(
        username="user1",
        first_name="Steven",
        last_name="King",
        hashed_password=pwd_context.hash("password1"),
        email="steven.king@example.com",
    )

    user2 = add_user(
        username="user2",
        first_name="Arthur",
        last_name="Hailey",
        hashed_password=pwd_context.hash("password2"),
        email="arthur.hailey@example.com",
    )

    # Создание тестовых целей
    def add_goal(user_id, title, description):
        goal = db.query(GoalDB).filter(GoalDB.title == title).first()
        if not goal:
            goal = GoalDB(
                user_id=user_id,
                title=title,
                description=description,
            )
            db.add(goal)
            db.commit()
            db.refresh(goal)
        return goal

    goal1 = add_goal(admin_user.id, "Learn Python", "Learn Python programming language")
    goal2 = add_goal(user1.id, "Learn FastAPI", "Learn FastAPI framework")

    db.close()

def wait_for_db(retries=10, delay=5):
    for _ in range(retries):
        try:
            engine.connect()
            print("PostgreSQL is ready!")
            return
        except Exception as e:
            print(f"PostgreSQL not ready yet: {e}")
            time.sleep(delay)
    raise Exception("Could not connect to PostgreSQL")

if __name__ == "__main__":
    wait_for_db()
    load_test_data()