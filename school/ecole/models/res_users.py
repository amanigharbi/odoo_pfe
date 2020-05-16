# See LICENSE file for full copyright and licensing details.

from odoo import models, api


class ResUsers(models.Model):

    _inherit = "res.users"

    @api.model
    def create(self, vals):
        '''Inherit Method to create user of group enseignant or parent'''
        vals.update({'employee_ids': False})
        user_rec = super(ResUsers, self).create(vals)
        if self._context.get('enseignant_create', False):
            enseignant_grp_id = self.env.ref('ecole.group_ecole_enseignant')
            user_base_grp = self.env.ref('base.group_user')
            contact_create = self.env.ref('base.group_partner_manager')
            groupe_enseignant_ids = [user_base_grp.id, enseignant_grp_id.id,
                                 contact_create.id]
            user_rec.write({'groups_id': [(6, 0, groupe_enseignant_ids)],
                            'company_id': self._context.get('ecole_id'),
                            'company_ids': [(4, self._context.get('ecole_id'))
                                            ]})
        return user_rec
