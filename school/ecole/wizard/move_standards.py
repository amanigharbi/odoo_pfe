# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class MoveStandards(models.TransientModel):
    _name = 'move.standards'
    _description = "Move Standards"

    academic_year_id = fields.Many2one('academic.year', 'annee academique',
                                       required=True)

    @api.multi
    def move_start(self):
        '''Code for moving eleve to next standard'''
        academic_obj = self.env['academic.year']
        ecole_stand_obj = self.env['ecole.standard']
        standard_obj = self.env["standard.standard"]
        eleve_obj = self.env['eleve.eleve']
        for stud in eleve_obj.search([('state', '=', 'done')]):
            year_id = academic_obj.next_year(stud.year.sequence)
            academic_year = academic_obj.search([('id', '=', year_id)],
                                                limit=1)
            standard_seq = stud.standard_id.standard_id.sequence
            next_class_id = standard_obj.next_standard(standard_seq)

            # Assign the annee academique
            if next_class_id:
                division = (stud.standard_id.division_id.id or False)
                next_stand = ecole_stand_obj.\
                    search([('standard_id', '=', next_class_id),
                            ('division_id', '=', division),
                            ('ecole_id', '=', stud.ecole_id.id),
                            ('medium_id', '=', stud.medium_id.id)])
                if next_stand:
                    std_vals = {'year': academic_year.id,
                                'standard_id': next_stand.id}
                    # Move eleve to next standard
                    stud.write(std_vals)
        return True
