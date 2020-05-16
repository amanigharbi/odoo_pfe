from odoo import models, fields, api
class historique_notification(models.Model):
    _name = 'historique.notification'
    _description = "historique notification"

    eleve_id =fields.Many2one('eleve.eleve','Nom Elève')
    title=fields.Char("Titre")
    message = fields.Char("Message")
    etat_message=fields.Boolean("Status Message")
    parent_id = fields.Many2one('ecole.parent', 'Parents')
