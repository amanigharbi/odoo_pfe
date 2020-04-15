from odoo import models, fields, api



class statistique_eleve(models.TransientModel):
    _name = 'statistique.eleve'
    _description = "statistique eleve"
    Classe = fields.Many2many('ecole.standard', 'statistique_eleve_ecole_standard_rel', 'statistique_eleve_id', 'ecole_standard_id',
                                  'standard_id')
    Academic_year= fields.Many2one('academic.year','academic_year.name')