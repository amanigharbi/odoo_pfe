# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class AssignRollNo(models.TransientModel):
    '''designed for assigning roll number to a eleve'''

    _name = 'assign.roll.no'
    _description = 'Assign Roll Number'

    standard_id = fields.Many2one('ecole.standard', 'Class', required=True)
    medium_id = fields.Many2one('standard.medium', 'Medium', required=True)

    @api.multi
    def assign_rollno(self):
        '''Method to assign roll no to eleves'''
        eleve_obj = self.env['eleve.eleve']
        # Search eleve
        for rec in self:
            eleve_ids = eleve_obj.search([('standard_id', '=',
                                               rec.standard_id.id),
                                              ('medium_id', '=',
                                               rec.medium_id.id)],
                                             order="name")
            # Assign roll no according to name.
            number = 1
            for eleve in eleve_ids:
                number += 1
                eleve.write({'roll_no': number})

        return True
