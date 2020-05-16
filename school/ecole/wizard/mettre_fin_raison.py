# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class mettre_finReason(models.TransientModel):
    _name = "mettre_fin.reason"
    _description = "mettre_fin Reason"

    reason = fields.Text('Reason')

    @api.multi
    def save_mettre_fin(self):
        '''Method to mettre_fin eleve and change etat to mettre_fin'''
        self.env['eleve.eleve'
                 ].browse(self._context.get('active_id')
                          ).write({'etat': 'mettre_fin',
                                   'mettre_fin_raison': self.reason,
                                   'active': False})
        eleve_obj = self.env['eleve.eleve'].\
            browse(self._context.get('active_id'))
        eleve_obj.classe_id._compute_total_eleve()
        user = self.env['res.users'].\
            search([('id', '=', eleve_obj.user_id.id)])
        eleve_rappel = self.env['eleve.rappel'].\
            search([('ele_id', '=', eleve_obj.id)])
        for rec in eleve_rappel:
            rec.active = False
        if user:
            user.active = False
