from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import Users


# Создаем приложение
app = FastAPI()

async def get_db():
    async with SessionLocal() as session:
        yield session

@app.get("/users")
async def read_all_users(db: Session = Depends(get_db)):
    users = db.query(Users).all()
    return users