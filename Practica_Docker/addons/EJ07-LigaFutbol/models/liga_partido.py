# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LigaPartido(models.Model):
    #Nombre y descripcion del modelo
    _name = 'liga.partido'
    _description = 'Un partido de la liga'


    #Atributos del modelo


    #PARA CUANDO NO HAY UN ATRIBUTO LLAMADO NAME PARA MOSTRAR LOS Many2One en Vistas
    # https://www.odoo.com/es_ES/forum/ayuda-1/how-defined-display-name-in-custom-many2one-91657
    
   

    #Nombre del equipo que juega en casa casa
    equipo_casa = fields.Many2one(
        'liga.equipo',
        string='Equipo local',
    )
    #Goles equipo de casa
    goles_casa= fields.Integer()

    #Nombre del equipo que juega fuera
    equipo_fuera = fields.Many2one(
        'liga.equipo',
        string='Equipo visitante',
    )
    #Goles equipo de casa
    goles_fuera= fields.Integer()

    # Nuevo campo para las jornadas
    jornada=fields.Integer()
    
    #Constraints de atributos
    @api.constrains('equipo_casa')
    def _check_mismo_equipo_casa(self):
        for record in self:
            if not record.equipo_casa:
                raise models.ValidationError('Debe seleccionarse un equipo local.')
            if record.equipo_casa == record.equipo_fuera:
                raise models.ValidationError('Los equipos del partido deben ser diferentes.')


     #Constraints de atributos
    @api.constrains('equipo_fuera')
    def _check_mismo_equipo_fuera(self):
        for record in self:
            if not record.equipo_fuera:
                raise models.ValidationError('Debe seleccionarse un equipo visitante.')
            if record.equipo_fuera and record.equipo_casa == record.equipo_fuera:
                raise models.ValidationError('Los equipos del partido deben ser diferentes.')




    
    '''
    Funcion para actualizar la clasificacion de los equipos, re-calculandola entera
    '''
    def actualizoRegistrosEquipo(self):
        #Recorremos partidos y equipos
        for recordEquipo in self.env['liga.equipo'].search([]):
            #Como recalculamos todo, ponemos de cada equipo todo a cero
            recordEquipo.victorias=0
            recordEquipo.empates=0
            recordEquipo.derrotas=0
            recordEquipo.goles_a_favor=0
            recordEquipo.goles_en_contra=0
            recordEquipo.puntos=0

            for recordPartido in self.env['liga.partido'].search([]):  
                #Si es el equipo de casa
                if recordPartido.equipo_casa.nombre==recordEquipo.nombre:
                    #Si los goles del equipo de casa es mayor que el visitante
                    if recordPartido.goles_casa>recordPartido.goles_fuera:
                        #Añadimos una victoria al equpo de casa
                        recordEquipo.victorias=recordEquipo.victorias+1
                        #Si la diferencia de los goles del equipo de casa es >=4
                        if(recordPartido.goles_casa-recordPartido.goles_fuera)>=4:
                            #Añadimos 7 puntos al equipo de casa
                            recordEquipo.puntos=recordEquipo.puntos+7
                        else:
                            #Añadimos 3 puntos al equipo de casa
                            recordEquipo.puntos=recordEquipo.puntos+3
                    #Si los goles del equipo de casa es menor que el visitante
                    elif recordPartido.goles_casa<recordPartido.goles_fuera:
                        #Añadimos una derrota al equipo de casa
                        recordEquipo.derrotas=recordEquipo.derrotas+1
                        #Si la diferencia de los goles del equipo visitante es >=4
                        if(recordPartido.goles_fuera-recordPartido.goles_casa)>=4:
                            #Añadimos 7 puntos al equipo de casa
                            recordEquipo.puntos=recordEquipo.puntos-1    
                    #Si los goloes de ambos equipos son iguales
                    else:
                        #Añadimos un empate al equipo de casa
                        recordEquipo.empates=recordEquipo.empates+1
                        #Añadimos un punto al equipo de casa
                        recordEquipo.puntos=recordEquipo.puntos+1

                    #Sumamos goles a favor y en contra
                    recordEquipo.goles_a_favor=recordEquipo.goles_a_favor+recordPartido.goles_casa
                    recordEquipo.goles_en_contra=recordEquipo.goles_en_contra+recordPartido.goles_fuera
                
                #Si es el equipo de fuera
                if recordPartido.equipo_fuera.nombre==recordEquipo.nombre:
                    #Si los goles del equipo visitante son mayores que el de casa
                    if recordPartido.goles_casa<recordPartido.goles_fuera:
                        #Añadimos una victoria al equipo visitante
                        recordEquipo.victorias=recordEquipo.victorias+1
                        #Si la diferencia de goles del equipo visitante es >=4
                        if (recordPartido.goles_fuera-recordPartido.goles_casa)>=4:
                            #Añadimos 7 puntos al visitante
                            recordEquipo.puntos=recordEquipo.puntos+7
                        else:
                            #Añadimo 3 puntos normales
                            recordEquipo.puntos=recordEquipo.puntos+3

                    #Si los goles del equipo visitante son menores que el de casa
                    elif recordPartido.goles_casa>recordPartido.goles_fuera:
                        #Añadimos un derota al equipo visitante
                        recordEquipo.derrotas=recordEquipo.derrotas+1
                        #Si la diferencia de goles es mayor a 4
                        if(recordPartido.goles_casa-recordPartido.goles_fuera)>=4:
                            recordEquipo.puntos=recordEquipo.puntos-1
                    else:
                        recordEquipo.empates=recordEquipo.empates+1
                        recordEquipo.puntos=recordEquipo.puntos+1

                    #Sumamos goles a favor y en contra
                    recordEquipo.goles_a_favor=recordEquipo.goles_a_favor+recordPartido.goles_fuera
                    recordEquipo.goles_en_contra=recordEquipo.goles_en_contra+recordPartido.goles_casa


    #API onchange para cuando se modifica un partido
    #Aunque onchange envia un registro, hacemos codigo para recalcular 
    #http://www.geninit.cn/developer/reference/orm.html  
    @api.onchange('equipo_casa', 'goles_casa', 'equipo_fuera', 'goles_fuera')
    def actualizar(self):
        self.actualizoRegistrosEquipo()
    

    #Sobrescribo el borrado (unlink)
    def unlink(self):
        #Borro el registro, que es lo que hace el metodo normalmente
        result=super(LigaPartido,self).unlink()
        #Añado que llame a actualizoRegistroEquipo()
        self.actualizoRegistrosEquipo()
        return result

    #Sobreescribo el metodo crear
    @api.model
    def create(self, values):
        #hago lo normal del metodo create
        result = super().create(values)
        #Añado esto: llamo a la funcion que actualiza la clasificacion
        self.actualizoRegistrosEquipo()
        #hago lo normal del metodo create
        return result

    #Funcion botones para alterar los goles de los partidos
    def sumar_dos_goles_equipo_casa(self):
        partidos = self.search([])
        for partido_local in partidos:
            partido_local.goles_casa = partido_local.goles_casa+2
        #Llamada a actualizoRegistrosEquipo
        self.actualizoRegistrosEquipo()
    
    def sumar_dos_goles_equipo_fuera(self):
        partidos = self.search([])
        for partido_visitante in partidos:
            partido_visitante.goles_fuera = partido_visitante.goles_fuera+2
        #Llamada a actualizoRegistrosEquipo
        self.actualizoRegistrosEquipo()

        