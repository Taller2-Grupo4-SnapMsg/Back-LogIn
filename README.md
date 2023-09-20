# Back-LogIn
Backend destinado al log in de usuarios.

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

## Para levantar el server local:
`bash run.sh`
Eso te va a levantar un docker que se instala las dependencias y cuando termine en `localhost:8000/docs` vas a tener la api con todos
los endpoints y una breve descripcion.
## Para correr los test:
Instalate pytest: 
`pip install -U pytest`
y haces:
`pytest /tests/user_tests.py`
## Para el black:
`pip install black`

`black *`
## Para correr el coverage:
`pip install coverage`

`coverage run -m pytest /tests/user_tests.py`

`coverage report -m`

Si te esta fallando un test en particular, podes probar con:
`pytest tests/user_tests -k "nombre_test"`

## Si te esta molestando pylint...
Probablemente sea por la variable de entorno PYTHONPATH, deberias hacer:
`export PYTHONPATH=.$PYTHONPATH`
y ahi te deberia andar el pre-commit...

## Para correr alembic, la herramienta de migraciones...
Si tu $PYTHONPATH es ".", te vas a tener que parar en la carpeta root (backLogin)
y hacer:
`alembic -c repository/alembic.ini <comando>`

Por ejemplo:
`alembic -c repository/alembic.ini current` para ver la version actual de la base de datos.

## Para correr los tests con tu base de datos local...
Requerimientos:
- postgresql
- psycopg2
- pytest
- docker
- alembic
- sqlalchemy
- docker-compose (si vas a usar el docker-compose que uso yo)
- coverage (opcional)

Todo esto va a asumir que estas corriendo todo parado en la carpeta root (backLogin), y que tenes el PYTHONPATH exportado como ".". (`export PYTHONPATH=.$PYTHONPATH`)

Primero tenes que levantar una base de datos local, yo lo hago con docker, usando este docker-compose:
```yaml
version: '3.9'
services:
  # Servicio para PostgreSQL
  postgres:
    build:
      context: .
      dockerfile: Dockerfile
    image: postgres:14
    container_name: bdd_postgres_db
    restart: always
    environment:
      POSTGRES_DB: bdd_db
      POSTGRES_USER: admin # Aca va tu usuario, podes cambiarlo, podes no hacerlo, da igual
      POSTGRES_PASSWORD: admin123
    ports:
      - "5432:5432"
    volumes:
      - ./data/postgres:/var/lib/postgresql/data
      - base_de_datos:/home/alex/Desktop/baseDeDatos/taller1/volume

  # Servicio para PgAdmin, esto es un visor para la bdd, no hace falta realmente.
  pgadmin:
    image: dpage/pgadmin4:7.5
    container_name: bdd_pg_admin
    restart: always
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@gmail.com
      PGADMIN_DEFAULT_PASSWORD: admin123
    ports:
      - "5050:80"

volumes:
  base_de_datos:
```
En la carpeta que tengas el docker-compose, haces:
`docker-compose up -d` (el -d es para que sea en segundo plano, si no queres eso, no lo pongas)

Si todo salio bien, tenes que hacer:
`docker ps`

y te tiene que aparecer el contenedor de postgres y el de pgadmin, algo asi:

```
CONTAINER ID   IMAGE                COMMAND                  CREATED       STATUS          PORTS                                            NAMES
91bea9d64dcb   postgres:14          "docker-entrypoint.s…"   2 weeks ago   Up 42 minutes   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp        bdd_postgres_db
6e37125df12b   dpage/pgadmin4:7.5   "/entrypoint.sh"         2 weeks ago   Up 42 minutes   443/tcp, 0.0.0.0:5050->80/tcp, :::5050->80/tcp   bdd_pg_admin
```
Si todo salio bien, podes crear la base de datos, yo la llame test-back-users, pero podes llamarla como quieras.
Para crearla podes hacer:

`docker exec -it bdd_postgres_db psql -U admin -d postgres -c "CREATE DATABASE \"test-back-users\";"`

Una vez hagas eso, ya vas a tener la base de datos creada, pero todavia te falta crear las tablas, para eso, tenes que hacer:

`alembic -c repository/alembic.ini upgrade head` 

(Su poniendo que ya exportaste PYTHONPATH=.$PYTHONPATH con `export PYTHONPATH=.$PYTHONPATH`)

Si todo salio bien, ya tenes la base de datos creada y las tablas creadas, ahora tenes que exportar la variable de entorno DB_URI asi:

`export DB_URI=postgresql://admin:admin123@localhost:5432/test-back-users$DB_URI`

Entonces, hasta aca, si haces:

`echo $DB_URI` te tiene que aparecer:

`postgresql://admin:admin123@localhost:5432/test-back-users`

`echo $PYTHONPATH` (podes tener varios) te tiene que aparecer :

`.`

`docker ps` te tiene que aparecer: (si lo hiciste con el docker-compose)

(los dos procesos de arriba)

Una vez hagas eso, ya podes correr los tests normalemente.

`pytest tests/user_tests.py`

y si corres el docker del proyecto (`bash run.sh`)

En `localhost:8000/docs` te tiene que aparecer la api con todos los endpoints y una breve descripcion.
donde vas a poder insertar y sacar todo lo que quieras, porque total vas a estar con la base de datos local tuya.

Una vez ya tenes todo instalado, y apagaste la compu, lo unico que tenes que hacer es:

`docker-compose up -d` (donde este tu docker-compose)

`export DB_URI=postgresql://admin:admin123@localhost:5432/test-back-users$DB_URI` (O el link de tu base de datos si cambiaste el nombre, usuario o contraseña)

`echo $DB_URI` (para chequear que este bien)

`echo $PYTHONPATH` (para chequear que este bien, si no lo agregas con el export)

`pytest tests/user_tests.py`

Para el coverage:

`coverage run -m pytest tests/user_tests.py`

`coverage report -m`


## Si te queres conectar a la base de datos de elephantSQL...
Tenes que exportar la variable de entorno DB_URI asi:
export DB_URI=postgresql://cwfvbvxl:jtsNDRjbVqGeBgYcYvxGps3LLlX_t-P5@berry.db.elephantsql.com:5432/cwfvbvxl$DB_URI

