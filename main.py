"""
    Archivo que se encarga de manejar las validaciones de inicio
    de sesión para el acceso al dashboard de administración, encargandose
    del super administrador y del administrador.
"""

import os

# Librería de conexión
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Lirearías para utilizar FastAPI
from fastapi import FastAPI, status
from pydantic import  EmailStr

# Importamos CORS para el acceso
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer


# Librerías de FastAPI para la seguridad
from fastapi.middleware.cors import CORSMiddleware

# Creamos nuestro objeto de FastAPI
app = FastAPI()

security = HTTPBasic()

securirtyBearer = HTTPBearer()

# Constante de la URI
URI = os.environ['URI']

#  Conectamos con nuestro Cluster de MongoDB
CLIENTE = MongoClient(URI, server_api=ServerApi('1'))

# Obtenemos una referencia de la base de datos
DB = CLIENTE['administrativos']

# Obtenemos la colección correspondiente
USUARIOS = DB['usuarios']


# Permitimos los origenes para poder conectarse
origins = [
    "http://0.0.0.0:8000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:80"
]

# Agergamos las opciones de origenes, credenciales, métodos y cabeceras
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


async def obtenener_rol(email: EmailStr, password: str):
    respuesta = []
    try:
        # Hacemos la consulta para obtener el rol del usuario
        datos = USUARIOS.find_one({'email': email, 'password': password})
        if datos != None:
            datos['_id'] = str(datos['_id'])
            respuesta.append(datos)
        return respuesta
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f'Ocurrió un error: {error}'


@app.get("/validar_usuario/", status_code=status.HTTP_200_OK, summary="Endpoint para validar el inicio de sesión")
async def validar_usuario(crendetials: HTTPBasicCredentials = Depends(security)):
    """
        # Endpoint para validar el inicio de sesión del dashboard de administración
        validando su existencia y su rol dentro de la aplicación

        # Códigos de estado:
            * 200 - Existe el usuario
    """
    try:
        # Obtenemos el usuario y la contraseña utilizando  BasicCredententials
        email = crendetials.username
        contraseña = crendetials.password

        # Obtenemos el rol de usuario utilizando su contraseña e email
        rol_usuario = await obtenener_rol(email, contraseña)
        print(rol_usuario)
        return rol_usuario
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f'Ocurrió un error: {error}'
