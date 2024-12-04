from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pymongo import MongoClient

# Настройка PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:qwerty@db/leadertask"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Настройка MongoDB
MONGO_URI = "mongodb://mongo:27017/"
client = MongoClient(MONGO_URI)
mongo_db = client["leadertask"]
tasks_collection = mongo_db["tasks"]

# Секретный ключ для подписи JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Настройка паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Настройка OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Модели данных
class User(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    hashed_password: str
    email: str

class Goal(BaseModel):
    id: int
    user_id: int
    title: str
    description: str

class Task(BaseModel):
    id: int
    goal_id: int
    title: str
    description: str

# SQLAlchemy models
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

# Зависимости для получения текущего пользователя
async def get_current_client(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        else:
            return username
    except JWTError:
        raise credentials_exception

# Создание и проверка JWT токенов
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Маршрут для получения токена
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.username == form_data.username).first()
    db.close()

    if user and pwd_context.verify(form_data.password, user.hashed_password):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Создание нового пользователя
@app.post("/users", response_model=User)
def create_user(user: User, current_user: str = Depends(get_current_client)):
    db = SessionLocal()
    db_user = UserDB(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return user

# Поиск пользователя по логину
@app.get("/users/{username}", response_model=User)
def get_user_by_username(username: str, current_user: str = Depends(get_current_client)):
    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.username == username).first()
    db.close()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Поиск пользователя по маске имени и фамилии
@app.get("/users", response_model=List[User])
def search_users_by_name(
    first_name: str, last_name: str, current_user: str = Depends(get_current_client)
):
    db = SessionLocal()
    users = (
        db.query(UserDB)
        .filter(
            UserDB.first_name.ilike(f"%{first_name}%"), UserDB.last_name.ilike(f"%{last_name}%")
        )
        .all()
    )
    db.close()
    return users

# Создание цели
@app.post("/goals", response_model=Goal)
def create_goal(goal: Goal, current_user: str = Depends(get_current_client)):
    db = SessionLocal()
    db_goal = GoalDB(**goal.dict())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    db.close()
    return goal

# Получение всех целей
@app.get("/goals", response_model=List[Goal])
def get_all_goals(current_user: str = Depends(get_current_client)):
    db = SessionLocal()
    goals = db.query(GoalDB).all()
    db.close()
    return goals

# Создание задачи
@app.post("/tasks", response_model=Task)
def create_task(task: Task, current_user: str = Depends(get_current_client)):
    task_data = task.dict()
    tasks_collection.insert_one(task_data)
    return task

# Получение всех задач цели
@app.get("/goals/{goal_id}/tasks", response_model=List[Task])
def get_goal_tasks(goal_id: int, current_user: str = Depends(get_current_client)):
    tasks = list(tasks_collection.find({"goal_id": goal_id}))
    return tasks

# Запуск сервера
# http://localhost:8000/openapi.json swagger
# http://localhost:8000/docs портал документации

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)