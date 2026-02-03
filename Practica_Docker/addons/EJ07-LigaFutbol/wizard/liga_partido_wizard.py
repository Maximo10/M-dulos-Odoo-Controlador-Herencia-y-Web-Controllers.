# -*- coding: utf-8 -*-
from odoo import models, fields

class LigaPartidoWizard(models.TransientModel):
    #Nombre y Descripción 
    _name='liga.partido.wizard'
    _descripcion='Wizard para crear partidos de liga'

    # Campos del modelo que usaremos en el Wizard
    equipo_casa=fields.Many2one('liga.equipo', string='Equipo de Casa', required=True)
    equipo_fuera=fields.Many2one('liga.equipo', string='Equipo Visitante', required=True)

    goles_casa=fields.Integer(string='Goles Equipo de Casa', default=0)
    goles_fuera=fields.Integer(string='Goles Equipo Visitante', default=0)

    # Nuevo campo para las jornadas 
    jornada=fields.Integer(string='Jornada', required=False, default=1)

    # Funcion para que se llame desde el Wizard
    def add_liga_partido(self):
        # Obtenemos referencia al modelo destino
        ligaPartidoModel = self.env['liga.partido']
        # Recorremos porque self referencia a todo el modelo
        for wiz in self:
            # Creamos un registro en "liga.partido"
            ligaPartidoModel.create({
                'equipo_casa': wiz.equipo_casa.id,
                'equipo_fuera': wiz.equipo_fuera.id,
                'goles_casa': wiz.goles_casa,
                'goles_fuera': wiz.goles_fuera,
                'jornada': wiz.jornada,
            })
            