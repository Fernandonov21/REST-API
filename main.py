import pymysql
pymysql.install_as_MySQLdb()

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Configuración de la base de datos MySQL
SQLALCHEMY_DATABASE_URL = "mysql://admin:admin123@localhost:3307/usersdb"

# Crear el motor de SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"charset": "utf8mb4"})

# Crear la sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la base declarativa de SQLAlchemy
Base = declarative_base()

# Definición del modelo User en SQLAlchemy (ajustado para la tabla users)
class User(Base):
    __tablename__ = "users"  # Especificamos que esta clase mapea a la tabla 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)  # 'username' en vez de 'name'
    email = Column(String(255), unique=True, index=True)

# Crear las tablas en la base de datos si no existen (solo para nuevas tablas)
Base.metadata.create_all(bind=engine)

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

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta raíz
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the User API!"}

# Obtener todos los usuarios
@app.get("/users/", response_model=List[UserResponse], tags=["Users"])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# Obtener un usuario por ID
@app.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"message": "User not found"}
    return user

# Crear un nuevo usuario
@app.post("/users/", response_model=UserResponse, tags=["Users"])
def create_user(user: UserResponse, db: Session = Depends(get_db)):
    db_user = User(
        username=user.username,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
