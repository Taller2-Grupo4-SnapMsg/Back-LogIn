
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from repository.tables.users import User
from repository.queries.queries import create_user
from repository.tables.users import Base
from sqlalchemy.sql import text

#Esto es lo que iria en el backend para conectarme y tendria que ver como importar las funciones para utilizar la bdd

# Crear una conexión a la base de datos
engine = create_engine("postgresql://cwfvbvxl:jtsNDRjbVqGeBgYcYvxGps3LLlX_t-P5@berry.db.elephantsql.com:5432/cwfvbvxl")

# Crea las tablas en la base de datos (esto creará todas las tablas definidas en tus modelos)
Base.metadata.create_all(engine)

# Crear una sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()

data = {
    "name": "PABLO",
    "surname": "encinoza",
    "date_of_birth": "13/04/1999",
    "bio": "soy nathyyyyyy",
    "following": 15000,
    "followers": 145510,
    "snaps": 54813,
    "avatar": "linkkimagennnn",
}
new_user = create_user(session, "pablo@fi.uba.ar", "shdhhdhd", "PABLITO", data)

users = session.query(User).all()
for user in users:
    print(f"ID: {user.id}, Username: {user.username}, Password: {user.password}, Email: {user.email}, Following: {user.following}, Snaps: {user.snaps}, Avatar: {user.avatar}")
session.close()

def app():
    with engine.connect() as conn:
        stmt = text("select * from pg_database")
        #print(conn.execute(stmt).fetchall())


if __name__ == "__main__":
    app()
