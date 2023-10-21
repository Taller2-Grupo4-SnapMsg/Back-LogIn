# Back-LogIn
Backend destinado al log in de usuarios.

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

## Para levantar el server local:
Primero tenes que buildear la imagen que va a usar el docker-compose (solo la primera vez o cada vez que cambies algun requirement de requirements.txt)
```bash
docker build -t my-fastapi-image .
```
Despues, una vez ya tenes eso, basta con hacer:
```bash
docker-compose up
```
## Para correr los test:
Instalate pytest: 
`pip install -U pytest`
Exporta la variable de entorno PYTHONPATH asi:
`export PYTHONPATH=.$PYTHONPATH`
Exporta la variable de entorno DB_URI asi:
`export DB_URI=postgresql://admin:admin123@localhost:5432/test-back-users$DB_URI`
y haces:
`pytest /tests/*`
## Para el black:
`pip install black`

`bash black.sh`
## Para correr el coverage:
`pip install coverage`

`coverage run -m pytest /tests/*`

`coverage report -m`

Si te esta fallando un test en particular, podes probar con:
`pytest -k "nombre_test" tests/*`

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

Para hacer una migracion es tan "facil" como cambiar las tablas en `repository/tables/` y hacer:

`alembic -c repository/alembic.ini revision --autogenerate -m "mensaje de los cambios"`

La migracion siempre se va hacer sobre el url que tenga el alembic.ini, se ve algo asi:

`sqlalchemy.url = "postgresql://admin:admin123@localhost:5432/test-back-users"`

Para correr la migracion **SIEMPRE** tenes que tener el DB_URI exportado, a la base de datos que vos quieras correr la migracion.

## Para correr el entorno del back de forma local...
Requerimientos:
- postgresql
- psycopg2
- pytest
- docker
- alembic
- sqlalchemy
- docker-compose
- coverage

Todo esto va a asumir que estas corriendo todo parado en la carpeta root (backLogin), y que tenes el PYTHONPATH exportado como ".". (`export PYTHONPATH=.$PYTHONPATH`)

Vamos a estar usando docker-compose, este es el archivo que estamos usando, voy a tratar de explicar
los campos mas importantes:
```yaml
version: '3.9'
services:
  # Servicio para PostgreSQL
  postgres:
    build:
      context: ./dockerPostgres
      dockerfile: Dockerfile
    image: postgres:14
    container_name: postgres_taller2
    environment:
      POSTGRES_DB: bdd_db # aca va el nombre de la base de datos
      POSTGRES_USER: admin # User que necesitas para autentificarte
      POSTGRES_PASSWORD: admin123 # Contraseña
    ports:
      - "5432:5432"
    volumes:
      # El volumen cumple la funcion de persistir datos y las bases de datos que crees
      # adentro del postgres, la carpeta esta esta en el gitignore.
      - ./data/postgres:/var/lib/postgresql/data

  # Servicio para PgAdmin
  pgadmin:
    image: dpage/pgadmin4:7.5
    container_name: pg_admin_taller2
    depends_on:
      - postgres # No se inicializa hasta que ya esta la bdd
    environment:
      # Si queres ver la base de datos con un gestor, esto te 
      # levanta un pg admin, para entrar tenes que usar estas
      # credenciales:
      PGADMIN_DEFAULT_EMAIL: admin@gmail.com
      PGADMIN_DEFAULT_PASSWORD: admin123
    ports:
      - "5050:80"

  # Servicio para tu FastAPI application
  fastapi_app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: fastapi_app_container
    depends_on:
      - postgres # No se inicializa hasta que ya esta la bdd
    # Este volumen es el que hace que si haces cambios se actualice cuando
    # des de baja el container y lo subas.
    volumes:
      - .:/app
    environment:
      #El fast api se va a conectar automaticamente al la bdd local:
      DB_URI: postgresql://admin:admin123@postgres:5432/test-back-users
      # Si queres conectarte local a la bdd posta, tenes que modificar ese link.
    ports:
      - "8000:8000"
```
Para levantar el entorno entonces, en otra consola haces:
`docker-compose up`
En esa consola vas a tener el log de los 3 servicios, si sale algun error, va a salir por ahi.

Si todo salio bien, tenes que hacer:
`docker ps`

y te tiene que aparecer el contenedor de postgres y el de pgadmin, algo asi:

```
CONTAINER ID   IMAGE                   COMMAND                  CREATED          STATUS          PORTS                                            NAMES
ec64cc95cd5b   dpage/pgadmin4:7.5      "/entrypoint.sh"         34 minutes ago   Up 29 minutes   443/tcp, 0.0.0.0:5050->80/tcp, :::5050->80/tcp   pg_admin_taller2
37fa1b9c1d44   postgres:14             "docker-entrypoint.s…"   34 minutes ago   Up 29 minutes   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp        postgres_taller2
```
El Fast api tiene que fallar, porque todavia no tenes la base de datos creada.

Ahora deberias podes crear la base de datos, yo la llame test-back-users, pero podes llamarla como quieras.
Para crearla podes hacer:

`docker exec -it postgres_taller2 psql -U admin -d postgres -c "CREATE DATABASE \"test-back-users\";"`

Una vez hagas eso, ya vas a tener la base de datos creada, pero todavia te falta crear las tablas, para eso, tenes que hacer:

(Suponiendo que ya exportaste PYTHONPATH=.$PYTHONPATH con `export PYTHONPATH=.$PYTHONPATH`)

`alembic -c repository/alembic.ini upgrade head` 

que va a actualizar la base de datos con las tablas a su ultima version.

Ahora si, podes dar de baja los containers (Control + C, o si los corriste de forma detatched `docker-compose down`)

Si todo salio bien, ya tenes la base de datos creada y las tablas creadas, ahora tenes que exportar la variable de entorno DB_URI asi:

`export DB_URI=postgresql://admin:admin123@localhost:5432/test-back-users$DB_URI`

Entonces, si haces:

`echo $DB_URI` te tiene que aparecer:

`postgresql://admin:admin123@localhost:5432/test-back-users`

Le vantamos los containers otra vez, ahora no deberia fallar ninguno:

`docker-compose up`

`docker ps` (en otra consola):
``` bash
CONTAINER ID   IMAGE                   COMMAND                  CREATED          STATUS          PORTS                                            NAMES
48b806cd1b62   backlogin-fastapi_app   "uvicorn control.con…"   34 minutes ago   Up 29 minutes   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp        fastapi_app_container
ec64cc95cd5b   dpage/pgadmin4:7.5      "/entrypoint.sh"         34 minutes ago   Up 29 minutes   443/tcp, 0.0.0.0:5050->80/tcp, :::5050->80/tcp   pg_admin_taller2
37fa1b9c1d44   postgres:14             "docker-entrypoint.s…"   34 minutes ago   Up 29 minutes   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp        postgres_taller2
```


En `localhost:8000/docs` te tiene que aparecer la api con todos los endpoints y una breve descripcion.
donde vas a poder insertar y sacar todo lo que quieras, porque total vas a estar con la base de datos local tuya.

Una vez ya tenes todo instalado, y apagaste la compu, lo unico que tenes que hacer es:

`docker-compose up`

`export DB_URI=postgresql://admin:admin123@localhost:5432/test-back-users$DB_URI` (O el link de tu base de datos si cambiaste el nombre, usuario o contraseña)

`echo $DB_URI` (para chequear que este bien)

`echo $PYTHONPATH` (para chequear que este bien, si no lo agregas con el export)

Hasta aca, si vas bien, deberias por ejemplo poder correr los tests con:

`pytest tests/*`

Para el coverage:

`coverage run -m pytest tests/*`

`coverage report -m`

**Si, para probar cambios tenes que dar de baja el docker y volverlo a correr, la alternativa es bajarte todo local, pero estas por tu cuenta.**

## Si estas teniendo problemas... estos son los que me pasaron a mi y como los solucione:

Si algun container esta teniendo problemas al inicializarse:

`docker-compose down -v`

`docker-compose up --force-recreate`

Eso va a hacer que se borren todos los volumenes y se vuelvan a crear, por lo que vas a tener que volver a crear la base de datos y las tablas. (creo)


## Si te queres conectar a la base de datos de elephantSQL, como por ejemplo para correr una migracion...
Tenes que exportar la variable de entorno DB_URI asi:
```bash 
export DB_URI=postgresql://cwfvbvxl:jtsNDRjbVqGeBgYcYvxGps3LLlX_t-P5@berry.db.elephantsql.com:5432/cwfvbvxl$DB_URI
```
Y despues hacer:
```bash
alembic -c repository/alembic.ini upgrade head
```

Si no, tenes que cambiar el link en el docker-compose para usar el FASTAPI como localhost conectado a la bdd de elephant.

## Si no sabes usar PgAdmin...
La primera vez que entres vas a tener que "agregar un server" estableciendo una coneccion con nuestro postgres. Para eso preguntale a Alejo(?)


# Comando para verificar pylint
```
find . -type f -name "*.py" | xargs pylint   
```