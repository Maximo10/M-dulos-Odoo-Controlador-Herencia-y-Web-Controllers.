# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

#Clase del controlador web
class Main(http.Controller):
    #Decorador que indica que la url "/ligafutbol/equipo/json" atendera por HTTP, sin autentificacion
    #Devolvera texto que estará en formato JSON
    #Se puede probar accediendo a http://localhost:8069/ligafutbol/equipo/json
    @http.route('/ligafutbol/equipo/json', type='http', auth='none')
    def obtenerDatosEquiposJSON(self):
        #Obtenemos la referencia al modelo de Equipo
        equipos = request.env['liga.equipo'].sudo().search([])
        
        #Generamos una lista con informacion que queremos sacar en JSON
        listaDatosEquipos=[]
        for equipo in equipos:
             listaDatosEquipos.append([equipo.nombre,str(equipo.fecha_fundacion),equipo.jugados,equipo.puntos,equipo.victorias,equipo.empates,equipo.derrotas])
        #Convertimos la lista generada a JSON
        json_result=json.dumps(listaDatosEquipos)

        return json_result
    
    #Se puede probar accediendo a http://localhost:9001/ligafutbol/eliminarempates
    @http.route('/ligafutbol/eliminarempates', type='http', auth='none')
    def funcion_eliminar_empates(self):
        try:
            # Buscamos todos los partidos
            lista_partidos = request.env['liga.partido'].sudo().search([])
        
            #Lista de los partidos empatados
            lista_partidos_empatados=[]

            # Filtramos los partidos que terminaron en empate
            for partido in lista_partidos:

                if partido.goles_casa == partido.goles_fuera:
                    lista_partidos_empatados.append(partido)
                
                # Contamos los partidos empatados
                num_partidos_empatados=len(lista_partidos_empatados)

            #Comprobamos si existe algun partido empatado
            if num_partidos_empatados>0:

                for partido_empatado in lista_partidos_empatados:
                    # Eliminamos los partidos empatados
                    partido_empatado.unlink()

                mensaje=json.dumps({'mensaje': f'Se eliminaron {num_partidos_empatados} partidos empatado'})
            else:
                mensaje=json.dumps({'mensaje': f'No existen partidos empatado para eliminar'})
            
            # Retornamos JSON con la cantidad eliminada
            return mensaje

        except Exception as e:
                    return json.dumps({"error": str(e)})



