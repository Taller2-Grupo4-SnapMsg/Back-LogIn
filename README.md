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