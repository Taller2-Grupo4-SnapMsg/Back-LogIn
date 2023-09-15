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
Primero tenes que crear la base de datos en tu local, por ejemplo:
test-back-users
y despues, exportar la variable de entorno DB_URI con el siguiente formato:
export DB_URI=postgresql://usuario:contraseña@localhost:puerto/test-back-users$DB_URI
Una vez hagas eso, ya podes correr los tests normalemente.

## Si te queres conectar a la base de datos de elephantSQL...
Tenes que exportar la variable de entorno DB_URI asi:
export DB_URI=postgresql://cwfvbvxl:jtsNDRjbVqGeBgYcYvxGps3LLlX_t-P5@berry.db.elephantsql.com:5432/cwfvbvxl$DB_URI

