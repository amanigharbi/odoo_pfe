# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class Moveclasses(models.TransientModel):
    _name = 'move.classes'
    _description = "Move classes"

    annee_scolaire_id = fields.Many2one('annee.scolaire', 'annee academique',
                                       required=True)

    @api.multi
    def move_debut(self):
        '''Code for moving eleve to next classe'''
        scolaire_obj = self.env['annee.scolaire']
        ecole_stand_obj = self.env['ecole.classe']
        classe_obj = self.env["classe.classe"]
        eleve_obj = self.env['eleve.eleve']
        for stud in eleve_obj.search([('etat', '=', 'terminé')]):
            annee_id = scolaire_obj.next_annee(stud.annee.sequence)
            annee_scolaire = scolaire_obj.search([('id', '=', annee_id)],
                                                limit=1)
            classe_seq = stud.classe_id.classe_id.sequence
            next_class_id = classe_obj.next_classe(classe_seq)

            # Assign the annee academique
            if next_class_id:
                division = (stud.classe_id.division_id.id or False)
                next_stand = ecole_stand_obj.\
                    search([('classe_id', '=', next_class_id),
                            ('division_id', '=', division),
                            ('ecole_id', '=', stud.ecole_id.id)])
                if next_stand:
                    std_vals = {'annee': annee_scolaire.id,
                                'classe_id': next_stand.id}
                    # Move eleve to next classe
                    stud.write(std_vals)
        return True
