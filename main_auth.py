from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext

# Создаем приложение
app = FastAPI()

# Настройка безопасности
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Фейковая база данных
fake_users_db = {
    "user1": {
        "username": "user1",
        "full_name": "John Doe",
        "email": "user1@example.com",
        "hashed_password": pwd_context.hash("password1"),
    }
}

# Модель для пользователя
class User(BaseModel):
    username: str
    email: str
    full_name: str | None = None

# Модель для данных пользователя с паролем
class UserInDB(User):
    hashed_password: str

# Функция для получения пользователя из базы данных
def get_user(db, username: str):
    user = db.get(username)
    if user:
        return UserInDB(**user)

# Проверка пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Аутентификация пользователя
def authenticate_user(username: str, password: str):
    user = get_user(fake_users_db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# Эндпоинт для получения токена
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user.username, "token_type": "bearer"}

# Эндпоинт для проверки авторизации
@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    user = get_user(fake_users_db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user