# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class TerminateReason(models.TransientModel):
    _name = "terminate.reason"
    _description = "Terminate Reason"

    reason = fields.Text('Reason')

    @api.multi
    def save_terminate(self):
        '''Method to terminate eleve and change state to terminate'''
        self.env['eleve.eleve'
                 ].browse(self._context.get('active_id')
                          ).write({'state': 'terminate',
                                   'terminate_reason': self.reason,
                                   'active': False})
        eleve_obj = self.env['eleve.eleve'].\
            browse(self._context.get('active_id'))
        eleve_obj.standard_id._compute_total_eleve()
        user = self.env['res.users'].\
            search([('id', '=', eleve_obj.user_id.id)])
        eleve_reminder = self.env['eleve.reminder'].\
            search([('stu_id', '=', eleve_obj.id)])
        for rec in eleve_reminder:
            rec.active = False
        if user:
            user.active = False
