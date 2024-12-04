from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# Настройка PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:qwerty@db/leadertask"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Настройка паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Модели данных
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)

class GoalDB(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(String)

class TaskDB(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id"))
    title = Column(String)
    description = Column(String)

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

    # Создание тестовых задач
    def add_task(goal_id, title, description):
        goal = db.query(GoalDB).filter(GoalDB.id == goal_id).first()
        if not goal:
            raise ValueError(f"Goal with id {goal_id} does not exist")
        task = db.query(TaskDB).filter(TaskDB.title == title).first()
        if not task:
            task = TaskDB(
                goal_id=goal_id,
                title=title,
                description=description,
            )
            db.add(task)
            db.commit()
            db.refresh(task)

    add_task(goal1.id, "Read Python documentation", "Read the official Python documentation")
    add_task(goal2.id, "Create a FastAPI project", "Create a simple FastAPI project")

    db.close()

if __name__ == "__main__":
    load_test_data()