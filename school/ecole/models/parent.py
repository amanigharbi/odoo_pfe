# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class ParentRelation(models.Model):
    '''Defining a Parent relation with child'''
    _name = "parent.relation"
    _description = "Parent-child relation information"

    name = fields.Char("Relation name", required=True)


class EcoleParent(models.Model):
    ''' Defining a enseignant information '''
    _name = 'ecole.parent'
    _description = 'Parent Information'

    @api.onchange('eleve_id')
    def onchange_eleve_id(self):
        self.standard_id = [(6, 0, [])]
        self.stand_id = [(6, 0, [])]
        standard_ids = [eleve.standard_id.id
                        for eleve in self.eleve_id]
        if standard_ids:
            stand_ids = [eleve.standard_id.standard_id.id
                         for eleve in self.eleve_id]
            self.standard_id = [(6, 0, standard_ids)]
            self.stand_id = [(6, 0, stand_ids)]

    partner_id = fields.Many2one('res.partner', 'User ID', ondelete="cascade",
                                 delegate=True, required=True)
    relation_id = fields.Many2one('parent.relation', "Relation with Child")
    eleve_id = fields.Many2many('eleve.eleve', 'eleves_parents_rel',
                                  'eleves_parent_id', 'eleve_id',
                                  'Children')
    standard_id = fields.Many2many('ecole.standard',
                                   'ecole_standard_parent_rel',
                                   'class_parent_id', 'class_id',
                                   'Academic Class')
    stand_id = fields.Many2many('standard.standard',
                                'standard_standard_parent_rel',
                                'standard_parent_id', 'standard_id',
                                'Academic Standard')
    enseignant_id = fields.Many2one('ecole.enseignant', 'enseignant',
                                 related="standard_id.user_id", store=True)

    @api.model
    def create(self, vals):
        parent_id = super(EcoleParent, self).create(vals)
        parent_grp_id = self.env.ref('ecole.group_ecole_parent')
        emp_grp = self.env.ref('base.group_user')
        parent_group_ids = [emp_grp.id, parent_grp_id.id]
        if vals.get('parent_create_mng'):
            return parent_id
        user_vals = {'name': parent_id.name,
                     'login': parent_id.email,
                     'email': parent_id.email,
                     'partner_id': parent_id.partner_id.id,
                     'groups_id': [(6, 0, parent_group_ids)]
                     }
        self.env['res.users'].create(user_vals)
        return parent_id

    @api.onchange('state_id')
    def onchange_state(self):
        self.country_id = False
        if self.state_id:
            self.country_id = self.state_id.country_id.id
