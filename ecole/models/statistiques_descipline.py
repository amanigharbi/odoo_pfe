from odoo import models, fields, api

class statistiques_descipline(models.TransientModel):
    _name = 'statistiques.descipline'
    _description = "statique descipline"
    standard_id = fields.Many2one('ecole.standard', 'Classe')
    Acadamic_year = fields.Char('Année', related='year.name',
                                help='annee academique', readonly=True)
