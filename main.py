"""
    Archivo que se encarga de manejar las operaciones
    del superadministrador, además de la sección de registrarse
    al principio
"""
import os
from pprint import pprint

# Librería de conexión
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId

# librerías para utilizar FastAPI
from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr

# Librearias de FastAPI para la seguridad
from fastapi.middleware.cors import CORSMiddleware

# Librearías para métodos específicos
from datetime import datetime
from email.message import EmailMessage
import ssl
import smtplib

# Creamos nuestro objeto de FastAPI
app = FastAPI()

# Constante de la URI
URI = os.environ['URI']

#  Conectamos con nuestro Cluster de MongoDB
CLIENTE = MongoClient(URI, server_api=ServerApi('1'))

# Obtenemos una referencia de la base de datos
DB = CLIENTE['administrativos']

# Obtenemos la colección correspondiente
USUARIOS = DB['usuarios']
EMAILS = DB['emails']
EMAILS_ENVIADOS = DB['correos_enviados']

# Permitimos los origenes para poder conectarse
origins = [
    "http://0.0.0.0:8000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:80"
]

# Agregamos las opciones de origenes, credneciales, métodos y cabeceras
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Clases modelo para los datos ingresados
class Usuarios(BaseModel):
    nombres: str
    apellidos: str
    email: EmailStr
    contraseña: str
    rol: int
    estado: int

class Usuarios_Contraseña(BaseModel):
    nombres: str
    apellidos: str
    email: EmailStr
    rol: int
    estado: int

class Correos_enviados(BaseModel):
    titulo: str
    contenido: str

# Ruta para las operaciones CRUD de usuario
@app.get("/usuarios", status_code=status.HTTP_200_OK, summary="Endpoint que devuelve todos los usuario")
async def obtener_usuarios():
    """
        # Endpoint para obtener los datos de la API

        # Códigos de etruestado:
            * 200 - Existe el contenido
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener todos los datos de la base de datos
        datos = USUARIOS.find({'status': 0})
        # Iteramos sobre la variable que almacena dichos datos para ser agregados a una lista
        for dato in datos:
            # Convertimos el _id a str para evitar problemas y lo agregamos a la lista
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

# Ruta para las operaciones CRUD de usuario
@app.get("/usuarios_suspendidos", status_code=status.HTTP_200_OK, summary="Endpoint que devuelve todos los usuario")
async def obtener_usuarios_suspendidos():
    """
        # Endpoint para obtener los datos de la API

        # Códigos de etruestado:
            * 200 - Existe el contenido
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener todos los datos de la base de datos
        datos = USUARIOS.find({'status': 1})
        # Iteramos sobre la variable que almacena dichos datos para ser agregados a una lista
        for dato in datos:
            # Convertimos el _id a str para evitar problemas y lo agregamos a la lista
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.post("/crear_usuario", status_code=status.HTTP_201_CREATED, summary="Endpoint para agregar un nuevo usuario")
async def crear_usuarios(usuario: Usuarios):
    """
        # Endpoint para crear un nuevo usuario

        # Códigos de estado:
            * 201 - creado con exito
    """
    respuesta = False
    try:
        # Creamos un nuevo diccionario con los datos guardados en la clase usuarios
        nuevo_documento = {
            "fname":usuario.nombres,
            "lname":usuario.apellidos,
            "email": usuario.email,
            "password":usuario.contraseña,
            "role":usuario.rol,
            "status":usuario.estado,
            "created": datetime.utcnow()
        }
        # Insertamos el nuevo documento guardando la respuesta de la consulta
        resultado_ingresado = USUARIOS.insert_one(nuevo_documento)

        # En caso de haber una respuesta correcta, muestra el mensaje confirmatorio con el id
        if resultado_ingresado.inserted_id:
            respuesta = True
        return respuesta
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.get("/buscar_usuario/{id_usuario}", status_code=status.HTTP_200_OK, summary="Endpoint para buscar un usuario")
async def buscar_usuario(id_usuario: str):
    """
        # Endpoint que se encarga de buscar un uusario mediante su identificador

        # Códigos de estado:
            * 200 - Existe el documento
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener todos los datos de la base de datos
        datos = USUARIOS.find({'_id': ObjectId(id_usuario)})
        # Iteramos sobre la variable que almacena dichos datos para ser agregados a una lista
        for dato in datos:
            # Convertimos el _id a str para evitar problemas y lo agregamos a la lista
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.get("/buscar_usuario_email/{email}", status_code=status.HTTP_200_OK, summary="Endpoint para buscar un usuario")
async def buscar_usuario(email: EmailStr):
    """
        # Endpoint que se encarga de buscar un uusario mediante su identificador

        # Códigos de estado:
            * 200 - Existe el documento
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener todos los datos de la base de datos
        datos = USUARIOS.find({'email': email})
        # Iteramos sobre la variable que almacena dichos datos para ser agregados a una lista
        for dato in datos:
            # Convertimos el _id a str para evitar problemas y lo agregamos a la lista
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.put("/actualizar_usuario_contra/{id_usuario}", status_code=status.HTTP_200_OK, summary="Endpoint para actualizar usuarios con nueva contraseña")
async def actualizar_usuario_contraseña(id_usuario: str, usuario: Usuarios):
    """
        # Endpoint para actualizar un usuario en base a su identificador con nueva contraseña

        # Códigos de estado:
            * 200 - Actualizado con exito
    """
    try:
        # Creamos un nuevo diccionario con los datos guardados en la clase usuarios
        nuevo_documento = {
            "fname":usuario.nombres,
            "lname":usuario.apellidos,
            "email": usuario.email,
            "password":usuario.contraseña,
            "role":usuario.rol,
            "status":usuario.estado,
            "created": datetime.utcnow()
        }
        # Insertamos el nuevo documento guardando la respuesta de la consulta
        resultado_actualizado = USUARIOS.update_one({'_id': ObjectId(id_usuario)}, {'$set': nuevo_documento})

        # En caso de haber una respuesta correcta, muestra el mensaje confirmatorio con el id
        if resultado_actualizado.modified_count == 1:
            return "Actualizado correctamente"
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.put("/actualizar_usuario/{id_usuario}", status_code=status.HTTP_200_OK, summary="Endpoint para actualizar usuarios")
async def actualizar_usuario(id_usuario: str, usuario: Usuarios_Contraseña):
    """
        # Endpoint para actualizar un usuario en base a su identificador

        # Códigos de estado:
            * 200 - Actualizado con exito
    """
    try:
        # Creamos un nuevo diccionario con los datos guardados en la clase usuarios
        nuevo_documento = {
            "fname":usuario.nombres,
            "lname":usuario.apellidos,
            "email": usuario.email,
            "role":usuario.rol,
            "status":usuario.estado,
            "created": datetime.utcnow()
        }
        # Insertamos el nuevo documento guardando la respuesta de la consulta
        resultado_actualizado = USUARIOS.update_one({'_id': ObjectId(id_usuario)}, {'$set': nuevo_documento})

        # En caso de haber una respuesta correcta, muestra el mensaje confirmatorio con el id
        if resultado_actualizado.modified_count == 1:
            return "Actualizado correctamente"
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.delete("/eliminar_usuario/{id_usuario}", status_code=status.HTTP_200_OK, summary="Endpoint para eliminar un usuario")
async def eliminar_usuario(id_usuario: str):
    """
        # Endpoint para eliminar un usuario de la base de datos en base a su identificador

        # Códigos de estado:
            * 200 - Eliminado con exito
    """
    respuesta = False
    try:
        # Realizamos la consulta para eliminar el documento en base a su identificador
        resultado = USUARIOS.delete_one({'_id': ObjectId(id_usuario)})
        # En caso de recibir un mensaje exitoso, imprime un mensaje
        if resultado.deleted_count == 1:
            respuesta = True
        return respuesta
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

# Ruta para las operaciones de Email
@app.get("/emails", status_code=status.HTTP_200_OK, summary="Endpoint que devuelve el historial de emails")
async def obtener_emails():
    """
        # Endpoint que se encarga de obtener todos los emails registrados

        # Códigos de estado:
            * 200 - Existe el contenido
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener todos los datos de la base de datos
        datos = EMAILS.find()
        # Iteramos sobre la variable que almacena dichos datos
        for dato in datos:
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.post("/registrar_email", status_code=status.HTTP_201_CREATED, summary="Endpoint para agregar un nuevo email")
async def registrar_email(correo: EmailStr):
    try:
        # Creamos un nuevo diccionario con los datos necesarios
        nuevo_documetno = {
            "email":correo,
            "upload_at": datetime.utcnow()
        }
        # Insertamos el nuevo documento guardando la respuesta
        resultado_ingresado = EMAILS.insert_one(nuevo_documetno)

        # En caso de haber un respuesta exitosa, muestra el mensaje
        if resultado_ingresado.inserted_id:
            return f"Ingresado correctamente: {resultado_ingresado.inserted_id}"
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"


@app.get("/buscar_email/{id_email}", status_code=status.HTTP_200_OK, summary="Endpoint para buscar un email")
async def buscar_email(id_email: str):
    """
        # Endpoint que se encarga de buscar un email específico

        # Códigos de estado:
            * 200 - Existe el contenido
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener todos los datos que coincidan con el criterio de búsqueda
        datos = EMAILS.find({'_id': ObjectId(id_email)})
        # Iteramos sobre la variable que almacena dichos datos
        for dato in datos:
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"


@app.delete("/eliminar_email/{id_email}", status_code=status.HTTP_200_OK, summary="Endpoint para eliminar un usuario")
async def eliminar_email_usuario(id_email: str):
    """
        # Endpoint para eliminar un usuario de la base de datos en base a su identificador

        # Códigos de estado:
            * 200 - Eliminado con exito
    """
    respuesta = False
    try:
        # Realizamos la consulta para eliminar el documento en base a su identificador
        resultado = EMAILS.delete_one({'_id': ObjectId(id_email)})
        # En caso de recibir un mensaje exitoso, imprime un mensaje
        if resultado.deleted_count == 1:
            respuesta = True
        return respuesta
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"


# Operaciones con el historias del Email's
@app.get("/emails_enviados", status_code=status.HTTP_200_OK, summary="Endpoint que devuelve el historial de emails")
async def obtener_emails_enviados():
    """
        # Endpoint que se encarga de obtener todos los emails enviados

        # Códigos de estado:
            * 200 - Existe el contenido
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener todos los datos de la base de datos
        datos = EMAILS_ENVIADOS.find()
        # Iteramos sobre la variable que almacena dichos datos
        for dato in datos:
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.post("/enviar_email", status_code=status.HTTP_201_CREATED, summary="Endpoint para agregar enviar un nuevo email")
async def enviar_email(correo: Correos_enviados):
    """
        # Endpoint para enviar un email a los usuarios registrados

        # Códigos de estado:
            * 200 - Enviado correctamente
    """
    try:
        # Guardamos el email de donde se envia el correo así como su contraeña de acceso
        email_sender = "varrapa25@gmail.com"
        password = "kvyo gmzw lcdx btlw"

        # Obtenemos los emails que tenemos en nuestra base de datos
        emails = await obtener_emails()
        destinatarios = []

        # Iteramos sobre el array para solo obtener los emails
        for email in emails:
            destinatarios.append(email['email'])

        # Guardamos a los emails que recibirán el mensaje
        email_receiver = destinatarios

        # Guardamos el Asunto y el cuerpo del mensaje
        subject = correo.titulo

        body = f"""
        <html>
            <head>
                <title>{subject}</title>
            </head>
            <body>
            {correo.contenido}
            </body>
        </html>
        """

        # Generamos un objeto de tipo EmailMessage y asignamos los valores que hemos ido guardando
        em = EmailMessage()
        em["From"] = email_sender
        em["To"] = email_receiver
        em["Subject"] = subject
        em.set_content(body, subtype='html')

        context = ssl.create_default_context()

        # Enviamos el mensaje utilizando smtplib
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())


        # Creamos un nuevo diccionario con los datos utilizados anteriormente
        nuevo_documento = {
            "msg_to": email_receiver,
            "msg_from": email_sender,
            "title":subject,
            "content":body,
            "send_at": datetime.utcnow()
        }

        # insertamos el nuevo documento guardando la respuesta
        resultado_ingresado = EMAILS_ENVIADOS.insert_one(nuevo_documento)

        # En caso de haber una respuesta exitosa, muestra el mensaje
        if resultado_ingresado.inserted_id:
            return f"Ingresado correctamente: {resultado_ingresado.inserted_id}"

    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"

@app.get("/buscar_email_enviados/{id_email}", status_code=status.HTTP_200_OK, summary="Endpoint para buscar un email")
async def buscar_email_enviados(id_email: str):
    """
        # Endpoint que se encarga de buscar un email enviado específico

        ## Códigos de estado:
            * 200 - Existe el contenido
    """
    try:
        respuesta = []
        # Hacemos la consulta para obtener todos los datos que coincidan con el criterio de búsqueda
        datos = EMAILS_ENVIADOS.find({'_id': ObjectId(id_email)})
        pprint(datos)
        # Iteramos sobre la variable que almacena dichos datos
        for dato in datos:
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)
        return respuesta
    # En caso de haber un error, regresa el error ocurrido
    except Exception as error:
        return f"Ocurrió un error: {error}"
