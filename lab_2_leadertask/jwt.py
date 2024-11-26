from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# Секретный ключ для подписи JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Настройка паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Настройка OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Псевдо-база данных пользователей
client_db = {
    "admin": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # hashed "secret"
}

# Временное хранилище для пользователей, целей и задач
users_db = []
goals_db = []
tasks_db = []

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
    password_check = False
    if form_data.username in client_db:
        password = client_db[form_data.username]
        if pwd_context.verify(form_data.password, password):
            password_check = True

    if password_check:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires
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
    for u in users_db:
        if u.id == user.id:
            raise HTTPException(status_code=404, detail="User already exists")
    users_db.append(user)
    return user

# Поиск пользователя по логину
@app.get("/users/{username}", response_model=User)
def get_user_by_username(username: str, current_user: str = Depends(get_current_client)):
    for user in users_db:
        if user.username == username:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# Поиск пользователя по маске имени и фамилии
@app.get("/users", response_model=List[User])
def search_users_by_name(
    first_name: str, last_name: str, current_user: str = Depends(get_current_client)
):
    matching_users = [
        user
        for user in users_db
        if first_name.lower() in user.first_name.lower()
        and last_name.lower() in user.last_name.lower()
    ]
    return matching_users

# Создание цели
@app.post("/goals", response_model=Goal)
def create_goal(goal: Goal, current_user: str = Depends(get_current_client)):
    for g in goals_db:
        if g.id == goal.id:
            raise HTTPException(status_code=404, detail="Goal already exists")
    goals_db.append(goal)
    return goal

# Получение всех целей
@app.get("/goals", response_model=List[Goal])
def get_all_goals(current_user: str = Depends(get_current_client)):
    return goals_db

# Создание задачи
@app.post("/tasks", response_model=Task)
def create_task(task: Task, current_user: str = Depends(get_current_client)):
    for t in tasks_db:
        if t.id == task.id:
            raise HTTPException(status_code=404, detail="Task already exists")
    tasks_db.append(task)
    return task

# Получение всех задач цели
@app.get("/goals/{goal_id}/tasks", response_model=List[Task])
def get_goal_tasks(goal_id: int, current_user: str = Depends(get_current_client)):
    goal_tasks = [task for task in tasks_db if task.goal_id == goal_id]
    return goal_tasks

# Запуск сервера
# http://localhost:8000/openapi.json swagger
# http://localhost:8000/docs портал документации

# Запуск сервера
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)