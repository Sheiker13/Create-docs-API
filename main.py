from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date

app = FastAPI(
    title="User Management API",
    description="""
    # User Management API

    ## Описание
    API для управления пользователями. Позволяет выполнять следующие операции:
    - Просматривать список пользователей.
    - Получать данные конкретного пользователя по ID.
    - Создавать нового пользователя.
    - Обновлять данные существующего пользователя.
    - Удалять пользователя.

    ## Аутентификация
    Данный API не требует аутентификации.

    ## Формат данных
    - Все запросы и ответы используют JSON.
    - Дата рождения передается в формате `YYYY-MM-DD`.
    - Баланс кошелька (`wallet`) передается в формате `float`.
    """,
    version="1.0.0",
)


class User(BaseModel):
    id: int
    username: str
    wallet: float
    birthdate: date


# Фейковая база данных пользователей
db_users = [
    User(id=1, username="user1", wallet=100.0, birthdate=date(1990, 1, 1)),
    User(id=2, username="user2", wallet=200.0, birthdate=date(1995, 5, 15)),
]


@app.get("/users/", response_model=List[User], tags=["Users"], summary="Получить всех пользователей")
async def read_users():
    """
    ## Описание
    Возвращает список всех пользователей.

    ## Пример запроса
    ```http
    GET /users/
    ```

    ## Ответ
    **200 OK**
    ```json
    [
        {"id": 1, "username": "user1", "wallet": 100.0, "birthdate": "1990-01-01"},
        {"id": 2, "username": "user2", "wallet": 200.0, "birthdate": "1995-05-15"}
    ]
    ```
    """
    return db_users


@app.get("/users/{user_id}", response_model=User, tags=["Users"], summary="Получить пользователя по ID")
async def read_user(user_id: int):
    """
    ## Описание
    Возвращает данные пользователя по указанному ID.

    ## Пример запроса
    ```http
    GET /users/1
    ```

    ## Ответ
    **200 OK**
    ```json
    {
        "id": 1,
        "username": "user1",
        "wallet": 100.0,
        "birthdate": "1990-01-01"
    }
    ```

    **404 Not Found**
    ```json
    {
        "detail": "User not found"
    }
    ```
    """
    user = next((user for user in db_users if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users/", response_model=User, tags=["Users"], summary="Создать нового пользователя")
async def create_user(user: User):
    """
    ## Описание
    Добавляет нового пользователя в базу данных.

    ## Пример запроса
    ```http
    POST /users/
    Content-Type: application/json
    {
        "id": 3,
        "username": "new_user",
        "wallet": 50.0,
        "birthdate": "2000-01-01"
    }
    ```

    ## Ответ
    **201 Created**
    ```json
    {
        "id": 3,
        "username": "new_user",
        "wallet": 50.0,
        "birthdate": "2000-01-01"
    }
    ```

    **400 Bad Request**
    ```json
    {
        "detail": "User with this ID already exists"
    }
    ```
    """
    if any(u.id == user.id for u in db_users):
        raise HTTPException(status_code=400, detail="User with this ID already exists")
    db_users.append(user)
    return user


@app.delete("/users/{user_id}", response_model=User, tags=["Users"], summary="Удалить пользователя")
async def delete_user(user_id: int):
    """
    ## Описание
    Удаляет пользователя по ID.

    ## Пример запроса
    ```http
    DELETE /users/1
    ```

    ## Ответ
    **200 OK**
    ```json
    {
        "id": 1,
        "username": "user1",
        "wallet": 100.0,
        "birthdate": "1990-01-01"
    }
    ```

    **404 Not Found**
    ```json
    {
        "detail": "User not found"
    }
    ```
    """
    user_index = next((i for i, u in enumerate(db_users) if u.id == user_id), None)
    if user_index is None:
        raise HTTPException(status_code=404, detail="User not found")
    deleted_user = db_users.pop(user_index)
    return deleted_user
