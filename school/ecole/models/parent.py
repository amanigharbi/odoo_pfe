# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class ParentRelation(models.Model):
    '''Defining a Parent relation with child'''
    _name = "parent.relation"
    _description = "Parent-child relation information"

    nom = fields.Char("Nom Du Relation", required=True)


class EcoleParent(models.Model):
    ''' Defining a enseignant information '''
    _name = 'ecole.parent'
    _description = 'Parent Information'

    @api.onchange('eleve_id')
    def onchange_eleve_id(self):
        self.classe_id = [(6, 0, [])]
        self.stand_id = [(6, 0, [])]
        classe_ids = [eleve.classe_id.id
                        for eleve in self.eleve_id]
        if classe_ids:
            stand_ids = [eleve.classe_id.classe_id.id
                         for eleve in self.eleve_id]
            self.classe_id = [(6, 0, classe_ids)]
            self.stand_id = [(6, 0, stand_ids)]
    notification_ids = fields.One2many('historique.notification', 'parent_id', 'Notification')

    partner_id = fields.Many2one('res.partner', 'User ID', ondelete="cascade",
                                 delegate=True, required=True)
    relation_id = fields.Many2one('parent.relation', "Relation Avec Enfant")
    eleve_id = fields.Many2many('eleve.eleve', 'eleves_parents_rel',
                                  'eleves_parent_id', 'eleve_id',
                                  'Fils')
    classe_id = fields.Many2many('ecole.classe',
                                   'ecole_classe_parent_rel',
                                   'class_parent_id', 'class_id',
                                   'Classe Scolaire')
    stand_id = fields.Many2many('classe.classe',
                                'classe_classe_parent_rel',
                                'classe_parent_id', 'classe_id',
                                'classe Academique')
    enseignant_id = fields.Many2one('ecole.enseignant', 'Enseignant',
                                 related="classe_id.user_id", store=True)


    @api.model
    def create(self, vals):
        parent_id = super(EcoleParent, self).create(vals)
        parent_grp_id = self.env.ref('ecole.group_ecole_parent')
        emp_grp = self.env.ref('base.group_user')
        parent_group_ids = [emp_grp.id, parent_grp_id.id]
        if vals.get('parent_create_mng'):
            return parent_id
        user_vals = {'nom': parent_id.nom,
                     'login': parent_id.email,
                     'email': parent_id.email,
                     'partner_id': parent_id.partner_id.id,
                     'groups_id': [(6, 0, parent_group_ids)]
                     }
        self.env['res.users'].create(user_vals)
        return parent_id

    @api.onchange('etat_id')
    def onchange_etat(self):
        self.pays_id = False
        if self.etat_id:
            self.pays_id = self.etat_id.pays_id.id

    class historique_notification(models.Model):
        _name = 'historique.notification'
        _description = "historique notification"

        eleve_id = fields.Many2one('eleve.eleve', 'Nom Elève')
        titre = fields.Char("Titre")
        message = fields.Char("Message")
        etat_message = fields.Boolean("Status De Message")
        parent_id = fields.Many2one('ecole.parent','Parents')
