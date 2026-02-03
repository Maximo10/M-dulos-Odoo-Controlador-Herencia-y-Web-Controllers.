# -*- coding: utf-8 -*-
# Importamos clases necesarias de Odoo para definir controladores HTTP
from odoo import http
from odoo.http import request

# Importamos bibliotecas externas necesarias para generar imágenes en memoria
import base64                    # Para codificar la imagen en base64 (para mostrarla en HTML)
from io import BytesIO           # Para trabajar con flujos de memoria
import random                    # Para generar pixeles de colores aleatorios
from PIL import Image            # Importamos Pillow para generar imágenes

class imagen_aleatoria(http.Controller):
    '''
    Ejemplo de URL: http://localhost:9001/generador/imagenaleatoria?ancho=300&alto=200
    '''
    #Ruta expuesta publicamente  (auth='public'), sin restricciones CORS (cors='*')
    @http.route('/generador/imagenaleatoria',auth='public', cors='*', type='http')
    def crearImagenAleatoria(self, ancho, alto ):
        #covertimos los parametros en enteros
        ancho=int(ancho)
        alto=int(alto)

        #creamos la imagen RGB en la memoria
        imagen=Image.new('RGB',(ancho,alto))
        #Acedemos a los pixeles para colorearlos
        pixeles=imagen.load()

        # Coloreamos cada pixel aleatoriamente
        for pixel_x in range(ancho):
            for pixel_y in range(alto):
                pixeles[pixel_x,pixel_y]=(
                    random.randint(0,255), #Rojo
                    random.randint(0,255), #Verde
                    random.randint(0,255)  #Azul
                )
            
        # Guardamos la imagen en memoria
        buffer = BytesIO()
        # Determinamos el formto de la imagen en caso de que se desee guardar
        imagen.save(buffer, format='PNG')
        # Empleamos base64.b64encode para convertir los bytes en texto html 
        imagen_codificada = base64.b64encode(buffer.getvalue()).decode('utf-8')

        # Devolvemos HTML con la imagen incrustada
        return f'<img src="data:image/png;base64,{imagen_codificada}" />'