import pymysql
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

# Configuración de la base de datos MySQL
MYSQL_HOST = "localhost"
MYSQL_PORT = 3307
MYSQL_USER = "admin"
MYSQL_PASSWORD = "admin123"
MYSQL_DB = "usersdb"

# Conectar a la base de datos MySQL
def get_db_connection():
    connection = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        charset='utf8mb4'
    )
    return connection

# FastAPI setup
app = FastAPI(
    title="User API",
    description="A simple API that manages users.",
    version="1.0.0"
)

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las URLs (ajústalo para producción)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

# Pydantic model para la respuesta de la API
class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

# Ruta raíz
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the User API!"}

# Obtener todos los usuarios
@app.get("/users/", response_model=List[UserResponse], tags=["Users"])
def get_users():
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users

# Obtener un usuario por ID
@app.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def get_user(user_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT id, username, email FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    if not user:
        return {"message": "User not found"}
    return user

# Crear un nuevo usuario
@app.post("/users/", response_model=UserResponse, tags=["Users"])
def create_user(user: UserResponse):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO users (username, email) VALUES (%s, %s)",
        (user.username, user.email)
    )
    connection.commit()
    user_id = cursor.lastrowid
    cursor.close()
    connection.close()

    return {**user.dict(), "id": user_id}

