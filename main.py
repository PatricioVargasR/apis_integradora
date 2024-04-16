"""
    Archivo que se encarga de manejar las operaciones del usuario
    de la página web
"""

import os

# Librería de conexión
from pymongo import DESCENDING
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId

# Librerías para utilizar FastAPI
from fastapi import FastAPI, status, Response
from pydantic import BaseModel, EmailStr

# Librerías de FastAPI para la seguridad
from fastapi.middleware.cors import CORSMiddleware

# Librerías de métodos especificos
from datetime import datetime

# Creamos nuestro objeto de FastAPI
app = FastAPI()

# Constante de la URI
URI = os.environ['URI']

#  Conectamos con nuestro Cluster de MongoDB
CLIENTE = MongoClient(URI, server_api=ServerApi('1'))

# Obtenemos una referenccia de la base de datos
DB = CLIENTE['administrativos']

# Obtenemos la colección correspondiente
CATEGORIA = DB['categorias']
PUBLICACIONES = DB['publicaciones']
CURIOSIDAD = DB['curiosidades']
IMAGENES = DB['imagenes']
EFEMERIDE = DB['efemerides']
USUARIO = DB['emails']
TEXTO = DB['dispositivos']

# Permitimos los origines para poder conectarse
origins = [
    "http://0.0.0.0:8000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:80"
]

# Agregamos las opciones de origines, credenciales, métodos y headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Clase para registrar el email
class Usuario(BaseModel):
    email: EmailStr

@app.get("/")
def presentacion():
    return {"Desarrollador por": ["Janneth", "David", "Patricio"]}

# Rutas para las operaciones CRUD de Categorias
@app.get("/categorias", status_code=status.HTTP_200_OK, summary="Endpoint para listar datos de categorías")
async def obtener_categorias():
    """
        # Endpoint para obtener datos de la API

        # Códigos de estado:
            * 200 - Existe el contenido
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener todos los datos de la colección
        datos = CATEGORIA.find({'navbar_status':0, 'status':0}).limit(12)

        # Iteramos sobre la variable que almacena dichos datos para guardarlos en una lista
        for dato in datos:
            # Convertimos el _id a str para evitar problemas y agregamos a la lista
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error regresa el error ocurrido
    except Exception as error:
        return f'Ocurrió un error: {error}'


@app.get("/buscar_categoria/{slug_categoria}", status_code=status.HTTP_200_OK, summary="Endpoint para buscar una categoría específica")
async def obtener_categoria(slug_categoria: str):
    """
        # Endpoint para obtener una categoría específica de la API

        # Códigos de estado:
            * 200 - Existe el documento
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener los documentos que cumplan el criterío de búsqueda
        datos = CATEGORIA.find({'slug': slug_categoria, 'status': 0}).limit(1)
        # Iteramos sobre la variable que almacena dichos datos para guardarlos en una lista
        for dato in datos:
            # Convertimos el _id a str para evitar problemas y agregamos a la lista
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error regresa el error ocurrido
    except Exception as error:
        return f'Ocurrió un error: {error}'

# Rutas para las operaciones CRUD de Posts
@app.get("/posts", status_code=status.HTTP_200_OK, summary="Endpoint para listar todas las publicaciones")
async def obtener_posts():
    """
        # Endpoint que se encarga de obtener todas las publicaciones

        # Códigos de estado:
            * 200 - Existe el contenido
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener todos los dato de publicaciones
        datos = PUBLICACIONES.find({'status': 0}).sort('_id', DESCENDING).limit(3)
        # Iteramos sobre la variable que almacena dichos datos
        for dato in datos:
            # convertimos el _id a str para evitar problemas y lo agregamos a la lista
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error; regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"


@app.get("/buscar_post_categoria/{id_categoria}", status_code=status.HTTP_200_OK, summary="Endpoint para buscar una publicación")
async def buscar_post_categoria(id_categoria: str):
    """
        # Endpoint que se encarga de buscar una publicación en base a su categoria

        # Códigos de estado:
            * 200 - Existe el contenido
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener los documentos que cumplan con el criterio de búsqueda
        datos = PUBLICACIONES.find({'category_id': id_categoria, 'status':0}).sort('_id', DESCENDING)
        # Iteramos sobre la variable que almacena dichos datos para guardarlos en una lista
        for dato in datos:
            # Convertimos el _id a str para evitar problema sy lo añadimos a la lista
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.get("/buscar_post/{slug}", status_code=status.HTTP_200_OK, summary="Endpoint para buscar una publicación")
async def buscar_post(slug: str):
    """
        # Endpoint que se encarga de buscar una publicación en base a su identificador

        # Códigos de estado:
            * 200 - Existe el contenido
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener los documentos que cumplan con el criterio de búsqueda
        datos = PUBLICACIONES.find({'slug': slug}).limit(1)
        # Iteramos sobre la variable que almacena dichos datos para guardarlos en una lista
        for dato in datos:
            # Convertimos el _id a str para evitar problema sy lo añadimos a la lista
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"


# Rutas para las operaciones CRUD de Curiosidades
@app.get("/curiosidades", status_code=status.HTTP_200_OK, summary="Enpoint que devuelve todas las curiosidades")
async def obtener_curiosidades():
    """
        # Endpoint que se encarga de obtener todas las curiosidades de la base de datos
        # Códigos de estado:
            * 200 - Existe el recurso
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener todos los datos de la colección
        datos = CURIOSIDAD.find({'status': 0}).limit(1)
        # Iteramos sobre la variable que alma dichos datos para guardarlos en una lista
        for dato in datos:
            # Conviertimos el _id a str para evitar problemas y agregamos a la lista
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un errro regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.get("/buscar_curiosidad/{id_curiosidad}", status_code=status.HTTP_200_OK, summary="Endpoint para buscar una curiosidad en específico")
async def obtener_curiosidad(id_curisiosidad: str):
    """
        # Endpoint para obtener una curiosidad específica de la base de datos

        # Códigos de estado:
            * 200 - Existe el documento
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener los documentos que cumplan con el criterio de búsqueda
        datos = CURIOSIDAD.find({'_id': ObjectId(id_curisiosidad)})
        # Iteramos sobre la variable que almacena dichos datos
        for dato in datos:
            # Convertimos el _id a str para evitar problemas y agregamos a la lista
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

# Rutas para las operaciones CRUD de Imagenes
@app.get("/imagenes", status_code=status.HTTP_200_OK, summary="Endpoint para listar datos de las imagenes")
async def obtener_imagenes():
    """
        # Endpoint para obtener datos de la API

        # Códigos de estado:
            * 200 - Existe el contenido
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener todos los datos de imagenes
        datos = IMAGENES.find()
        # Iteramos sobre la variable que almacena dichos datos
        for dato in datos:
            # Convertimos el _id a str para evitar problemas y agregamos a la lista
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.get("/buscar_imagen/{id_imagen}", status_code=status.HTTP_200_OK, summary="Endpoint para buscar una imagen específica")
async def obtener_imagen(id_imagen: str):
    """
        # Endpoint para obtener una imagen específica de la API

        # Códigos de estado:
            * 200 - Existe el documento
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener los documentos que cumplan con el criterio de búsqueda
        datos = IMAGENES.find({'_id': ObjectId(id_imagen)})
        # Iteramos sobre la variable que almacena dichos datos para guardarlos en una lista
        for dato in datos:
            # Convertimos el _id a str para evitar problemas y lo añadimos a la lista
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # en caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"


# Rutas para las operaciones CRUD de Efemeride
@app.get("/efemerides", status_code=status.HTTP_200_OK, summary="Enndpoint para listar datos de las efemerides")
async def obtener_efemerides():
    """
        # Endpoint para obtener datos de la API

        # Códigos de estado:
            * 200 - Existe el contenido
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener todos los datos de la colección
        datos = EFEMERIDE.find({'status':0}).sort('_id', DESCENDING).limit(1)
        # Iteramos sobre la variable que almacena dichos datos para luego ser guardados
        # en una lista
        for dato in datos:
            # Convertimos el _id a str para evitar problemas
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.get("/buscar_efemeride/{id_efemeride}", status_code=status.HTTP_200_OK, summary="Endpoint para buscar una efemeride")
async def obtener_efemeride(id_efemeride: str):
    """
        # Endpoint para obtener una efemeride específica de la base de datos

        # Códigos de estado:
            * 200 - Existe el documento
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener los documentos que cumplan el criterio de búsqeuda
        datos = EFEMERIDE.find({'_id':ObjectId(id_efemeride)})
        # iteramos sobre la variable que almacena dichos datos
        for dato in datos:
            # Convertimos el _id a str para evitar problemas y agregamos a la lista
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error, regresa el erro ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.post("/enviar_email/", status_code = status.HTTP_201_CREATED, summary="Endpoint para suscribirse")
async def enviar_email(usuario: Usuario):
    """
        # Endpoint para suscribirse mediante el email que suba el usuario

        # Códigos de estado.
            * 201 - Registro con exito
    """
    respuesta = False
    try:
        # Creamos un nuevo documento
        nuevo_documento = {
            "email":usuario.email,
            "upload_at": datetime.utcnow()
        }
        # Insertamos el documento guardando la respuesta recibida
        resultado_ingresado = USUARIO.insert_one(nuevo_documento)

        # En caso de haber respuesta correcta, cambiamos la variable
        if resultado_ingresado.inserted_id:
            respuesta = True
        return respuesta
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.get("/textos/{identificador}", status_code=status.HTTP_200_OK, summary="Endpoint para verificar los textos")
async def recuperar_textos(identificador: str):
    try:
        # Separar el identificador
        identificador, *otros = identificador.split('.')

        # Consultar la base de datos
        resultado_obtenido = TEXTO.find_one({'_id': ObjectId(identificador)}, {'texto_pantalla': 1})

        # Verificar si se encontraron resultados
        if not resultado_obtenido:
            return "No hay datos"

        # Cambiar el tipo de dato de la clave _id
        resultado_obtenido['_id'] = str(resultado_obtenido['_id'])

        # Formatear el texto si es una lista
        texto = resultado_obtenido.get('texto_pantalla', '')
        texto_formateado = '\n'.join(texto) if isinstance(texto, list) else texto

        # Devolver la respuesta
        return Response(content=str(texto_formateado), media_type="text/plain") if otros else resultado_obtenido['texto_pantalla']

    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.get("/textos_estado/{identificador}", status_code = status.HTTP_200_OK, summary="Endpoint para verificar el estado")
async def recuperar_estado(identificador: str):
    """
        # Endpoint para obtener el estado del dispositivo de la base de datos

        # Códigos de estado.
            * 200 - Obtenidos con exito
    """
    try:
        # Separamos el identificador
        identificador, *otros = identificador.split('.')

        # Consultamos en la base de datos
        resultado_obtenido = TEXTO.find_one({'_id': ObjectId(identificador)}, {'estado': 1})

        # Verificar si se encontraron resultados
        if not resultado_obtenido:
            return "No hay datos"

        # Cambiamos el tipo de dato de la clave _id
        resultado_obtenido['_id'] = str(resultado_obtenido['_id'])

        # Formateamos el texto si es una lista
        texto = resultado_obtenido.get('estado', '')
        texto_formateado = '\n'.join(texto) if isinstance(texto, list) else texto

        # Devolvemos la respuesta
        return Response(content=str(texto_formateado), media_type="text/plain") if otros else resultado_obtenido['estado']
    except Exception as error:
        return f"Ocurrió un error: {error}"