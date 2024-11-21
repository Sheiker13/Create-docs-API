from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date

app = FastAPI(
    title="User Management API",
    description="""
API для управления пользователями. Позволяет выполнять следующие операции:
- Просматривать список пользователей.
- Получать данные конкретного пользователя по ID.
- Создавать нового пользователя.
- Обновлять данные существующего пользователя.
- Удалять пользователя.
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


@app.get(
    "/users/",
    response_model=List[User],
    summary="Получить всех пользователей",
    description="Возвращает список всех пользователей из базы данных.",
    tags=["Users"],
)
async def read_users():
    """
    ## Пример запроса
    ```http
    GET /users/
    ```

    ## Ответ
    - **200 OK**: Возвращает список пользователей.
    ```json
    [
        {"id": 1, "username": "user1", "wallet": 100.0, "birthdate": "1990-01-01"},
        {"id": 2, "username": "user2", "wallet": 200.0, "birthdate": "1995-05-15"}
    ]
    ```
    """
    return db_users


@app.get(
    "/users/{user_id}",
    response_model=User,
    summary="Получить пользователя по ID",
    description="Возвращает данные пользователя по указанному ID. Если пользователь не найден, возвращает ошибку 404.",
    tags=["Users"],
)
async def read_user(user_id: int):
    """
    ## Пример запроса
    ```http
    GET /users/1
    ```

    ## Ответы
    - **200 OK**: Возвращает данные пользователя.
    ```json
    {
        "id": 1,
        "username": "user1",
        "wallet": 100.0,
        "birthdate": "1990-01-01"
    }
    ```
    - **404 Not Found**: Пользователь не найден.
    """
    user = next((user for user in db_users if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post(
    "/users/",
    response_model=User,
    summary="Создать нового пользователя",
    description="Добавляет нового пользователя в базу данных. Если пользователь с таким ID уже существует, возвращает ошибку 400.",
    tags=["Users"],
)
async def create_user(user: User):
    """
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

    ## Ответы
    - **201 Created**: Пользователь успешно добавлен.
    - **400 Bad Request**: Пользователь с таким ID уже существует.
    """
    if any(u.id == user.id for u in db_users):
        raise HTTPException(status_code=400, detail="User with this ID already exists")
    db_users.append(user)
    return user


@app.put(
    "/users/{user_id}",
    response_model=User,
    summary="Обновить данные пользователя",
    description="Обновляет данные пользователя с указанным ID. Если пользователь не найден, возвращает ошибку 404.",
    tags=["Users"],
)
async def update_user(user_id: int, updated_user: User):
    """
    ## Пример запроса
    ```http
    PUT /users/1
    Content-Type: application/json
    {
        "username": "updated_user",
        "wallet": 150.0,
        "birthdate": "1991-01-01"
    }
    ```

    ## Ответы
    - **200 OK**: Данные пользователя успешно обновлены.
    - **404 Not Found**: Пользователь с таким ID не найден.
    """
    for db_user in db_users:
        if db_user.id == user_id:
            db_user.username = updated_user.username
            db_user.wallet = updated_user.wallet
            db_user.birthdate = updated_user.birthdate
            return db_user
    raise HTTPException(status_code=404, detail="User not found")


@app.delete(
    "/users/{user_id}",
    response_model=User,
    summary="Удалить пользователя",
    description="Удаляет пользователя с указанным ID из базы данных. Если пользователь не найден, возвращает ошибку 404.",
    tags=["Users"],
)
async def delete_user(user_id: int):
    """
    ## Пример запроса
    ```http
    DELETE /users/1
    ```

    ## Ответы
    - **200 OK**: Пользователь успешно удалён.
    - **404 Not Found**: Пользователь с таким ID не найден.
    """
    user_index = next((i for i, u in enumerate(db_users) if u.id == user_id), None)
    if user_index is None:
        raise HTTPException(status_code=404, detail="User not found")
    deleted_user = db_users.pop(user_index)
    return deleted_user
