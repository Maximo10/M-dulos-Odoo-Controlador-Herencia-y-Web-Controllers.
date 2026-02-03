# Importamos las librerías necesarias
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import json
from dotenv import load_dotenv
import os

# Cargamos las variables de entorno desde el archivo .env
load_dotenv()
# Obtenemos las variables de entorno necesarias
TELEGRAM_TOKEN = os.getenv("TOKEN_BOT_TELEGRAM")
URL_API_REST = os.getenv("URL_API_REST")
URL_API_REST_ALL_SOCIOS = os.getenv("URL_API_REST_ALL_SOCIOS")

# Definimos la función para el comando /start
async def comandos_inicio_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Varable para guardar mensajes recibidos del usuario
    mensaje_usuario = update.message.text

    # Uso de try-except para manejar posibles errores
    try:
        # Variable para separar los datos recibidos
        datos_usuario = mensaje_usuario.split(",")
        # Variable para guardar el comando recibido
        comando = datos_usuario[0].strip().lower()
        # Array para guardar los datos del socio
        datos_socio = {}

        # Recoremos los datos recibidos y los guardamos en el array
        for cada_dato in datos_usuario[1:]:
            # Variable para guardar el comando y los datos del socio
            comando_recibido, cada_dato_socio = cada_dato.split("=")
            # Agregamos los datos al array
            datos_socio[comando_recibido.strip()]= cada_dato_socio.strip()
    
        # Comando para agregar un nuevo socio
        if comando=="crear":
            # Parseamos los datos del socio a formato JSON y los mostramos por terminal
            datos_socio_json = json.dumps(datos_socio)
            print(f"Datos del socio a crear: {datos_socio_json}")
            # Hacemos la petición POST a la API REST para crear el socio
            respuesta=requests.post(URL_API_REST, json=datos_socio)
            # Mostramos la respuesta de la API REST por terminal
            print(f"Respuesta de la API REST: {respuesta.text}")
            # Enviamos un mensaje al usuario con la respuesta de la API REST
            await update.message.reply_text(f"Socio creado correctamente.\n{respuesta.text}")
        
        # Comando para obtener todos los socios
        elif comando=="consultar":
            # Hacemos la petición GET a la API REST para obtener todos los socios
            respuesta=requests.get(f"{URL_API_REST_ALL_SOCIOS}")
            # Mostramos la respuesta de la API REST por terminal
            print(f"Mostrar todos los socios: {respuesta.text}")
            # Enviamos un mensaje al usuario con la respuesta de la API REST
            await update.message.reply_text(f"Lista de socios:\n{respuesta.text}")
        
        # Comando para Eliminar un socio
        elif comando=="borrar":
            # Parseamos los datos del socio a formato JSON y los mostramos por terminal
            datos_socio_json = json.dumps(datos_socio)
            print(f"Datos del socio a eliminar: {datos_socio_json}")
            # Hacemos la petición DELETE a la API REST para elimiar el socio
            respuesta = requests.delete(f"{URL_API_REST}?data={datos_socio_json}")
            # Mostramos la respuesta de la API REST por terminal
            print(f"Respuesta de la API REST:{respuesta.text}")
            # Enviamos un mensaje al usuario con la respuesta de la API REST
            await update.message.reply_text(f"Socio eliminado correctamente.\n{respuesta.text}")
        
        # Comando para Modificar un sociuo
        elif comando=="modificar":
            # Parseamos los datos del socio a formato JSON y los mostramos por terminal
            datos_socio_json = json.dumps(datos_socio)
            print(f"Datos del socio a modificar: {datos_socio_json}")
            # Hacemos la petición PUT a la API REST para modificar el socio
            respuesta = requests.put(URL_API_REST,  json=datos_socio)
            # Mostramos la respuesta de la API REST por terminal
            print(f"Respuesta de la API REST:{respuesta.text}")            
            # Enviamos un mensaje al usuario con la respuesta de la API REST
            await update.message.reply_text(f"El socio ha sido modificado de forma correcta: {respuesta.text}")

    except Exception as e:
        print("Error en la ejecución del comando:", e)
        await update.message.reply_text(f"Error en la ejecución del comando: {e}")

# Funcio para el comando ayuda para el usuario
async def help_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje_ayuda_user='''
        *Comandos disponibles:*\n
        • Crear socio:\n
        crear, nombre=Juan, apellidos=Pérez, num_socio=1\n
        • Modificar socio:\n
        modificar, num_socio=1, nombre=Pedro\n
        • Consultar socio:\n
        consultar, num_socio=1\n
        • Borrar socio:\n
        borrar, num_socio=1
        '''
    await update.message.reply_text(mensaje_ayuda_user)

# Funcion para iniciar el bot
def main():
    app=ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    # Comando /help
    app.add_handler(CommandHandler("help", help_bot))

    # Comando para el resto de mensaje de texto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, comandos_inicio_bot))    
    
    # Mensaje de Inicio bot por terminal
    print("Bot de Telegram iniciado...")
    app.run_polling()

# Comando de ejecución
if __name__ == "__main__":
    main()

