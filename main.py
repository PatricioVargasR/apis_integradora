"""
    Archivo que se encarga de manejar las operaciones de
    inicio de sesión para el administrador además de las
    operaciones CRUD del administrador.
"""
from typing import List
import os

# Librería de conexión
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from bson import ObjectId

# Librerías para utilizar FastAPI
from fastapi import FastAPI, File, UploadFile, status
from pydantic import BaseModel

# Librerías de FastAPI para la seguridad
from fastapi.middleware.cors import CORSMiddleware

# Librerías para métodos específico
from datetime import datetime
import base64


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
DISPOSITIVOS = DB['dispositivos']

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

# Clases módelo para los datos ingresados
class Categoria(BaseModel):
    nombre: str
    slug: str
    descripcion: str
    meta_titulo: str
    meta_descripcion: str
    meta_palabrasClave: list
    estado_navegacion: int
    estado: int

class Publicaciones(BaseModel):
    id_categoria: str
    nombre: str
    slug: str
    descripcion: str
    meta_titulo: str
    meta_descripcion: str
    meta_palabrasClaves: list
    estado: int

class Curiosidad(BaseModel):
    descripcion: str
    estado: bool

class Efemeride(BaseModel):
    nombre: str
    fecha_efemeride: str
    descripcion: str
    estado: int

class Dispositivos(BaseModel):
    obra_asociada: str
    texto_pantalla: dict
    estado: int


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
        datos = CATEGORIA.find()
        # Iteramos sobre la variable que almacena dichos datos para guardarlos en una lista
        for dato in datos:
            # Convertimos el _id a str para evitar problemas y agregamos a la lista
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error regresa el error ocurrido
    except Exception as error:
        return f'Ocurrió un error: {error}'


@app.post("/crear_categorias", status_code=status.HTTP_201_CREATED, summary="Endpoint para ingresar una nueva categoría")
async def crear_categorias(categoria: Categoria):
    """
        # Endpoint para insertar una nueva categoría

        # Códigos de estado:
            * 201 - Creado correctamente
    """
    respuesta = False
    try:
        # Creamos un nuevo diccionario con los datos guardados en la clase categoria
        nuevo_documento = {
            "name": categoria.nombre,
            "slug":categoria.slug,
            "description":categoria.descripcion,
            "meta_title":categoria.meta_titulo,
            "meta_description":categoria.meta_descripcion,
            "meta_keywords":categoria.meta_palabrasClave,
            "navbar_status":categoria.estado_navegacion,
            "status":categoria.estado,
            "created": datetime.utcnow()
        }
        # Insertamos el nuevo documento guardando la respuesta de la consulta
        resultado_ingresado = CATEGORIA.insert_one(nuevo_documento)

        # En caso de haber una respuesta muestra el mensaje confirmatorio con el id
        if resultado_ingresado.inserted_id:
            respuesta = True
        return respuesta
    # En caso de haber un error regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.get("/buscar_categoria/{id_categoria}", status_code=status.HTTP_200_OK, summary="Endpoint para buscar una categoría específica")
async def obtener_categoria(id_categoria: str):
    """
        # Endpoint para obtener una categoría específica de la API

        # Códigos de estado:
            * 200 - Existe el documento
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener los documentos que cumplan el criterío de búsqueda
        datos = CATEGORIA.find({'_id': ObjectId(id_categoria)})
        # Iteramos sobre la variable que almacena dichos datos para guardarlos en una lista
        for dato in datos:
            # Convertimos el _id a str para evitar problemas y agregamos a la lista
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error regresa el error ocurrido
    except Exception as error:
        return f'Ocurrió un error: {error}'

@app.get("/buscar_categoria_slug/{slug}", status_code=status.HTTP_200_OK, summary="Endpoint para buscar una categoría específica")
async def obtener_categoria(slug: str):
    """
        # Endpoint para obtener una categoría específica de la API

        # Códigos de estado:
            * 200 - Existe el documento
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener los documentos que cumplan el criterío de búsqueda
        datos = CATEGORIA.find({'slug': slug})
        # Iteramos sobre la variable que almacena dichos datos para guardarlos en una lista
        for dato in datos:
            # Convertimos el _id a str para evitar problemas y agregamos a la lista
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error regresa el error ocurrido
    except Exception as error:
        return f'Ocurrió un error: {error}'


@app.put("/actualizar_categorias/{id_categoria}", status_code=status.HTTP_200_OK, summary="Endpoint para actualizar categorías")
async def actualizar_categorias(id_categoria: str, categoria: Categoria):
    """
        # Endpoint para actualizar una categoría específica de la API

        # Códigos de estado:
            * 200 - Actualizado correctamente
    """
    try:
        # Creamos un nuevo diccionario con los datos guardados en la clase categoria
        nuevo_documento = {
            "name": categoria.nombre,
            "slug":categoria.slug,
            "description":categoria.descripcion,
            "meta_title":categoria.meta_titulo,
            "meta_description":categoria.meta_descripcion,
            "meta_keywords":categoria.meta_palabrasClave,
            "navbar_status":categoria.estado_navegacion,
            "status":categoria.estado,
            "created": datetime.utcnow()
        }
        # Guardamos la respueta de la consulta realizada para actualizar un documento
        resultado_actualizado = CATEGORIA.update_one({'_id': ObjectId(id_categoria)},{'$set': nuevo_documento})
        # Verificamos que sea exitosa y muestra un mensaje en caso de que sea así
        if resultado_actualizado.modified_count == 1:
            return "Actualizado con exito"
    # En caso de haber un error, regresamos el error correspondiente
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.delete("/eliminar_categorias/{id_categoria}", status_code=status.HTTP_200_OK, summary="Endpont para eliminar una categoría")
async def eliminar_categoria(id_categoria: str):
    """
        # Endpoint que se encarga de eliminar una categoría en base a su nombre de la base de datos
        # Códigos de estado:
            * 200 - Eliminado correctamente
    """
    respuesta = False
    try:
        # Realizamos la consulta para eliminar un documento en base a su identificador
        resultado = CATEGORIA.delete_one({"_id": ObjectId(id_categoria)})
        # En caso de recibir un mensaje de satisfactorio imprime el mensaje
        if resultado.deleted_count == 1:
            respuesta = True
        return respuesta
    # En caso de haber un error, regresa el error correspondiente
    except Exception as error:
        return f"Ocurrió un error: {error}"

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
        datos = PUBLICACIONES.find()
        # Iteramos sobre la variable que almacena dichos datos
        for dato in datos:
            # convertimos el _id a str para evitar problemas y lo agregamos a la lista
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error; regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.post("/crear_posts", status_code=status.HTTP_201_CREATED, summary="Endpoint para crear publicación")
async def crear_posts(
    id_categoria: str,
    nombre: str,
    slug: str,
    descripcion: str,
    meta_titulo: str,
    meta_descripcion: str,
    meta_palabrasClaves: List[str],
    estado: int,
    file: UploadFile = File(...)
):
    """
        # Endpoint para crear una nueva publicación

        # Códigos de estado:
            * 201 - Creado correctamente
    """
    respuesta = False
    try:
        # lee la imagen como bytes
        imagen_bytes = file.file.read()

        # Convierte la imagen a base64
        imagen_base64 = base64.b64encode(imagen_bytes).decode('ascii')

        # Creamos un nuevo diccionario con los datos guardados en los query params
        nuevo_documento = {
            "category_id": id_categoria,
            "name": nombre,
            "slug": slug,
            "description": descripcion,
            "image": imagen_base64,
            "meta_title": meta_titulo,
            "meta_description": meta_descripcion,
            "meta_keyword": meta_palabrasClaves,
            "status": estado,
            "created": datetime.utcnow()
        }
        # Insetamos el nuevo documento guarndando la respuesta de la consulta
        resultado_ingresado = PUBLICACIONES.insert_one(nuevo_documento)

        # En caso de haber una respuesta exitosa, muestra el mensaje
        if resultado_ingresado.inserted_id:
            respuesta = True
        return respuesta
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.get("/buscar_post/{id_post}", status_code=status.HTTP_200_OK, summary="Endpoint para buscar una imagen")
async def buscar_post(id_post: str):
    """
        # Endpoint que se encarga de buscar una publicación en base a su identificador

        # Códigos de estado:
            * 200 - Existe el contenido
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener los documentos que cumplan con el criterio de búsqueda
        datos = PUBLICACIONES.find({'_id': ObjectId(id_post)})
        # Iteramos sobre la variable que almacena dichos datos para guardarlos en una lista
        for dato in datos:
            # Convertimos el _id a str para evitar problema sy lo añadimos a la lista
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.get("/buscar_post_slug/{slug_post}", status_code=status.HTTP_200_OK, summary="Endpoint para buscar una publicación")
async def buscar_post_slug(slug_post: str):
    """
        # Endpoint que se encarga de buscar una publicación en base a su slug

        # Códigos de estado:
            * 200 - Existe el contenido
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener los documentos que cumplan con el criterio de búsqueda
        datos = PUBLICACIONES.find({'slug': slug_post}, {'_id': 1})
        # Iteramos sobre la variable que almacena dichos datos para guardarlos en una lista
        for dato in datos:
            # Convertimos el _id a str para evitar problema sy lo añadimos a la lista
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.put("/actualizar_post_nuevaImagen/{id_posts}", status_code=status.HTTP_200_OK, summary="Endpoint para actualizar una publicación con imagen")
async def actualizar_posts_imagen(
    id_posts:str,
    id_categoria: str,
    nombre: str,
    slug: str,
    descripcion: str,
    meta_titulo: str,
    meta_descripcion: str,
    meta_palabrasClaves: List[str],
    estado: int,
    file: UploadFile = File(...)
):
    """
        # Endpoint para actualizar una publicación con una nueva imagen

        # Códigos de estado:
            * 201 - Creado correctamente
    """
    respuesta = False
    try:
        # lee la imagen como bytes
        imagen_bytes = file.file.read()

        # Convierte la imagen a base64
        imagen_base64 = base64.b64encode(imagen_bytes).decode('ascii')

        # Creamos un nuevo diccionario con los datos guardados en los query params
        nuevo_documento = {
            "category_id": id_categoria,
            "name": nombre,
            "slug": slug,
            "description": descripcion,
            "image": imagen_base64,
            "meta_title": meta_titulo,
            "meta_description": meta_descripcion,
            "meta_keyword": meta_palabrasClaves,
            "status": estado,
            "created": datetime.utcnow()

        }
        # Insetamos el nuevo documento guarndando la respuesta de la consulta
        resultado_actualizado = PUBLICACIONES.update_one({'_id':ObjectId(id_posts)}, {'$set': nuevo_documento})

        # En caso de haber una respuesta exitosa, muestra el mensaje
        if resultado_actualizado.modified_count == 1:
            respuesta = True
        return respuesta
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.put("/actualizar_post/{id_posts}", status_code=status.HTTP_200_OK, summary="Endpoint para actualizar una publicación")
async def actualizar_posts(id_posts:str, publicacion: Publicaciones):
    """
        # Endpoint para actualizar una publicación

        # Códigos de estado:
            * 201 - Creado correctamente
    """
    respuesta = False
    try:
        # Creamos un nuevo diccionario con los datos guardados en los query params
        nuevo_documento = {
            "category_id": publicacion.id_categoria,
            "name": publicacion.nombre,
            "slug": publicacion.slug,
            "description": publicacion.descripcion,
            "meta_title": publicacion.meta_titulo,
            "meta_description": publicacion.meta_descripcion,
            "meta_keyword": publicacion.meta_palabrasClaves,
            "status": publicacion.estado,
            "created": datetime.utcnow()

        }
        # Insetamos el nuevo documento guarndando la respuesta de la consulta
        resultado_actualizado = PUBLICACIONES.update_one({'_id':ObjectId(id_posts)}, {'$set': nuevo_documento})

        # En caso de haber una respuesta exitosa, muestra el mensaje
        if resultado_actualizado.modified_count == 1:
            respuesta = True
        return respuesta
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.delete("/eliminar_post/{id_posts}", status_code=status.HTTP_200_OK, summary="Enpoint para eliminar una publicación")
async def eliminar_post(id_posts: str):
    """
        # Endpoint para eliminar una publicación en base a su identificador

        # Códigos de estado:
            * 200 - Actualizado correctamente
    """
    try:
        # Realizamos la consulta para eliminar un documento
        resultado = PUBLICACIONES.delete_one({'_id': ObjectId(id_posts)})
        # En caso de recibir un mensaje exitoso, imprime el mensaje
        if resultado.deleted_count == 1:
            return 'Eliminado con éxito'
    # En caso de haber un error regresa el error ocurrido
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
        datos = CURIOSIDAD.find()
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
async def obtener_curiosidad(id_curiosidad: str):
    """
        # Endpoint para obtener una curiosidad específica de la base de datos

        # Códigos de estado:
            * 200 - Existe el documento
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener los documentos que cumplan con el criterio de búsqueda
        datos = CURIOSIDAD.find({'_id': ObjectId(id_curiosidad)})
        # Iteramos sobre la variable que almacena dichos datos
        for dato in datos:
            # Convertimos el _id a str para evitar problemas y agregamos a la lista
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.put("/actualizar_curiosidad/{id_curiosidad}", status_code=status.HTTP_200_OK, summary="Endpoint para actualizar curiosidades")
async def actualizar_curiosidad(id_curiosidad: str, curiosidad: Curiosidad):
    """
        # Endpoint para actualizar una curiosidad específica de la API

        # Códigos de estado:
            * 200 - Actualizado correctamente
    """
    respuesta = False
    try:
        # Creamos un nuevo diccionario con los datos en la clase curiosidad
        nuevo_documento = {
            "description":curiosidad.descripcion,
            "status":curiosidad.estado,
            "created": datetime.utcnow()
        }
        # Guardamos la respuesta de la consulta realizada para actualizar un documento
        resultado_actualizado = CURIOSIDAD.update_one({'_id': ObjectId(id_curiosidad)}, {'$set': nuevo_documento})

        # En caso de haber una respuesta muestra el mensaje
        if resultado_actualizado.modified_count == 1:
            respuesta = True
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

@app.post("/crear_imagenes", status_code=status.HTTP_201_CREATED, summary="Endpoint para ingresar una nueva imagen")
async def crear_imagenes(
    nombre: str,
    estado: int,
    file: UploadFile = File(...)

):
    """
        # Endpoint para insertar una nueva categoría

        # Códigos de estado:
            * 201 - Creado correctamente
    """
    respuesta = True
    try:
        # Lee la imagen como bytes
        imagen_bytes = file.file.read()

        # Convierte la imagen a base64
        imagen_base64 = base64.b64encode(imagen_bytes).decode('ascii')

        # Creamos un nuevo diccionario con los datos guardados los query params
        nuevo_documento = {
            "name":nombre,
            "image":imagen_base64,
            "status":estado,
            "upload_at": datetime.utcnow()
        }
        # Insertamos el nuevo documento guardando la respuesta de la consulta
        resultado_ingresado = IMAGENES.insert_one(nuevo_documento)

        # En caso de haber una respuesta exitosa, muestra el mensaje
        if resultado_ingresado.inserted_id:
            respuesta = True
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

@app.put("/actualizar_imagen_nueva/{id_imagen}", status_code=status.HTTP_200_OK, summary="Endpoint para actualizar una imagen")
async def actualizar_imagen_nueva(
    id_imagen: str,
    nombre: str,
    estado: int,
    file: UploadFile = File(...)
):
    """
        # Endpoint para actualizar una imagen específica de la API

        # Códigos de estado:
            * 200 - Actualizado correctamente
    """
    try:
        # Lee la imagen como bytes
        imagen_bytes = file.file.read()

        # Convierte la imagen a base64
        imagen_base64 = base64.b64encode(imagen_bytes).decode('ascii')

        # Creamos un nuevo diccionario con los datos guardados los query params
        nuevo_documento = {
            "name":nombre,
            "image":imagen_base64,
            "status":estado,
            "upload_at": datetime.utcnow()
        }
        # Insertamos el nuevo documento guardando la respuesta de la consulta
        resultado_ingresado = IMAGENES.update_one({'_id': ObjectId(id_imagen)}, {'$set': nuevo_documento})

        # En caso de haber una respuesta exitosa, muestra el mensaje
        if resultado_ingresado.modified_count == 1:
            return 'Actualizado con éxito'
        # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.put("/actualizar_imagen/{id_imagen}", status_code=status.HTTP_200_OK, summary="Endpoint para actualizar con una nueva imagen")
async def actualizar_imagen(
    id_imagen: str,
    nombre: str,
    estado: int,
):
    """
        # Endpoint para actualizar una imagen con una imagen nueva específica de la API

        # Códigos de estado:
            * 200 - Actualizado correctamente
    """
    respuesta = False
    try:
        # Creamos un nuevo diccionario con los datos guardados los query params
        nuevo_documento = {
            "name":nombre,
            "status":estado,
            "upload_at": datetime.utcnow()
        }
        # Insertamos el nuevo documento guardando la respuesta de la consulta
        resultado_ingresado = IMAGENES.update_one({'_id': ObjectId(id_imagen)}, {'$set': nuevo_documento})

        # En caso de haber una respuesta exitosa, muestra el mensaje
        if resultado_ingresado.modified_count == 1:
            respuesta = True
        return respuesta
        # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.delete("/eliminar_imagen/{id_imagen}", status_code=status.HTTP_200_OK, summary="Endpoint para eliminar una imagen")
async def eliminar_imagen(id_imagen: str):
    """
        # Endpoint que se encarga de eliminar una imagen en base a su identificador

        # Códigos de estado:
            * 200 - Eliminado correctamente
    """
    try:
        # Realizamos la consulta para eliminar un documento
        resultado = IMAGENES.delete_one({'_id': ObjectId(id_imagen)})
        # En caso de recibir un mensaje exitoso, imprime el mensaje
        if resultado.deleted_count == 1:
            return 'Eliminado con éxito'
    # En caso de haber un error regresa el error ocurrido
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
        datos = EFEMERIDE.find()
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

@app.post("/crear_efemerides", status_code=status.HTTP_201_CREATED, summary="Endpoint para ingresar una nueva efemeride")
async def crear_efemerides(efemeride: Efemeride):
    """
        # Endpoint para insertar una nueva efemeride

        # Códigos de estado:
            * 201 - Creado correctamente
    """
    try:

        # Creamos un nuevo diccionario con los datos guardados en la colección efemeride
        nuevo_documento = {
            "name":efemeride.nombre,
            "date": datetime.strptime(efemeride.fecha_efemeride, '%Y-%m-%d'),
            "description":efemeride.descripcion,
            "status":efemeride.estado,
            "created":datetime.utcnow()
        }
        # Insertamos el nuevo documento guardando la respuesta de la consulta
        resultado_ingresado = EFEMERIDE.insert_one(nuevo_documento)

        # En caos de haber una respueta exitosa, muestra el mensaje
        if resultado_ingresado.inserted_id:
            return f"Ingresado correctamente {resultado_ingresado.inserted_id}"
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

@app.put("/actualizar_efemeride/{id_efemeride}", status_code=status.HTTP_200_OK, summary="Endpoint para actualizar efemerides")
async def actualizar_efemeride(id_efemeride: str, efemeride: Efemeride):
    """
        # Endpoint para actualizar una efemeride específica

        # Códigos de estado:
            * 200 - Actualizado correctamente
    """
    respuesta = False
    try:
        # Creamos un nuevo diccionario con los datos en la clase de efemeride
        nuevo_documento = {
            "name":efemeride.nombre,
            "date": datetime.strptime(efemeride.fecha_efemeride, '%Y-%m-%d'),
            "description":efemeride.descripcion,
            "status":efemeride.estado,
            "created":datetime.utcnow()
        }
        # Insertamos el nuevo documento guardando la respuesta de la consulta
        resultado_actualizado = EFEMERIDE.update_one({'_id': ObjectId(id_efemeride)},{'$set': nuevo_documento})

        # En caos de haber una respueta exitosa, muestra el mensaje
        if resultado_actualizado.modified_count == 1:
            respuesta = True
        return respuesta
    # En caso de haber un error regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.delete("/eliminar_efemeride/{id_efemeride}", status_code=status.HTTP_200_OK, summary="Endpoint para eliminar una efemeride")
async def eliminar_efemeride(id_efemeride: str):
    """
        # Endpoint que se encarga de eliminar una efemeride

        # Códigos de estado:
            * 200 - Eliminado correctamente
    """
    respuesta = False
    try:
        # Realizamos la consulta para eliminar el documento correspondiente
        resultado = EFEMERIDE.delete_one({'_id': ObjectId(id_efemeride)})
        # En caso de recebir un mensaje satisfactorio imprime el mensaje correspondiente
        if resultado.deleted_count == 1:
            respuesta = True
        return respuesta
    except Exception as error:
        return f"Ocurrió un error: {error}"


# Acciones para los dispositivos Iot
@app.get("/dispositivos", status_code=status.HTTP_200_OK, summary="Endpoint para obtener todos los dispositivo")
async def obtener_dispositivos():
    """
        # Endpoint para obtener a todos los dispositivos de la base de datos

        # Códigos de estado:
            * 200 - Existe el contenido
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener todos los datos de la colección de la base de datos
        datos = DISPOSITIVOS.find()
        # Iteramos sobre la variable que almacena dichos datos para guardarlos en la lista
        for dato in datos:
            # convertimos el _id a str para evitar problemas y agregamos a la lista
            dato ['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrión un error: {error}"

@app.post("/agregar_dispositivo", status_code=status.HTTP_201_CREATED, summary="Endoint para agregar un nuevo dispositivo")
async def agregar_dispositivo(dispositivo: Dispositivos):
    """
        # Endpoint para ingrear un nuevo dispositivo a la base de datos

        # Códigos de estado:
            * 201 - Actualizado con exito
    """
    respuesta = False
    try:
        # Creamos un nuevo diccionari con los datos guardados en la clase Dispositivos
        nuevo_documento = {
            "obra_asociada": dispositivo.obra_asociada,
            "estado": dispositivo.estado,
            "texto_pantalla": dispositivo.texto_pantalla,
            "creado": datetime.utcnow()
        }
        # Insertamos el nuevo documento guardando la respuesta de la consulta
        resultado_ingresado = DISPOSITIVOS.insert_one(nuevo_documento)

        # En caso de haber una respuesta correcta, muestra el mensaje
        if resultado_ingresado.inserted_id:
            respuesta = True
        return respuesta
    except Exception as error:
        return f"Ocurrión un error: {error}"


@app.get("/buscar_dispositivo/{id_dispositivo}", status_code=status.HTTP_200_OK, summary="Endpoin para buscar un dispositivo")
async def buscar_dispositivo(id_dispositivo: str):
    """
        # Endpoint para buscar un dispositivo en base a su identificador

        # Códigos de estado:
            * 200 - Existe el contenido
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener todos los datos de la colección de la base de datos
        datos = DISPOSITIVOS.find({'_id': ObjectId(id_dispositivo)})
        # Iteramos sobre la variable que almacena dichos datos para guardarlos en la lista
        for dato in datos:
            # convertimos el _id a str para evitar problemas y agregamos a la lista
            dato ['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrión un error: {error}"


@app.put("/actualizar_dispositivo/{id_dispositivo}", status_code=status.HTTP_200_OK, summary="Endpoint para actualizar dispositivos")
async def actualizar_dispositivos(id_dispositivo: str, dispositivo:Dispositivos):
    """
        # Endpoint para actualizar un dispositivo en base a su identificador

        # Códigos de estado:
            * 200 - Actualizado con exito
    """
    resultado = False
    try:
        # Creamos un nuevo diccionari con los datos guardados en la clase Dispositivos
        nuevo_documento = {
            "obra_asociada": dispositivo.obra_asociada,
            "estado": dispositivo.estado,
            "texto_pantalla": dispositivo.texto_pantalla,
            "creado": datetime.utcnow()
        }
        # Actualizamos el  documento guardando la respuesta de la consulta
        resultado_ingresado = DISPOSITIVOS.update_one({'_id': ObjectId(id_dispositivo)}, {'$set': nuevo_documento})

        # En caso de haber una respuesta correcta, muestra el mensaje
        if resultado_ingresado.modified_count == 1:
            resultado = True
        return resultado
    except Exception as error:
        return f"Ocurrión un error: {error}"

@app.delete("/eliminar_dispositivo/{id_dispositivo}", status_code=status.HTTP_200_OK, summary="Endpoint para eliminar un dispositivo")
async def eliminar_dispositivo(id_dispositivo: str):
    """
        # Endpoint para eliminar un dispositivo de la base de datos en base a su identificador

        # Códigos de estado:
            * 200 - Eliminado correctamente
    """
    respuesta = False
    try:
        # Realizamos la consulta para eliminar un documento en base a su identificaodr
        resultado = DISPOSITIVOS.delete_one({'_id': ObjectId(id_dispositivo)})
        # En caso de recibir un mensaje satisfactorio imprime el mensaje
        if resultado.deleted_count == 1:
            respuesta = True
        return respuesta
    except Exception as error:
        return f"Ocurrión un error: {error}"

