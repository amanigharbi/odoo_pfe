# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class emploie(models.Model):
    _description = 'emploie'
    _name = 'emploie.emploie'

    @api.depends('emploie_ids')
    def _compute_user(self):
        '''Method to compute user'''
        for rec in self:
            rec.user_ids = [enseignant.enseignant_id.employee_id.user_id.id
                            for enseignant in rec.emploie_ids
                            ]
        return True

    nom = fields.Char('Déscription')
    classe_id = fields.Many2one('ecole.classe', 'Classe Scolaire',
                                  required=True,
                                  help="selectionnez classe")
    annee_id = fields.Many2one('annee.scolaire', 'Année', required=True,
                              help="selectionnez annee scolaire")
    emploie_ids = fields.One2many('emploie.emploie.details', 'table_id', 'Calendrier')
    emploie_type = fields.Selection([('reguliere', 'reguliere')],
                                      'emploie Type', default="reguliere",
                                      inivisible=True)
    user_ids = fields.Many2many('res.users', string="Utilisateur",
                                compute="_compute_user", store=True)
    salle_classe_id = fields.Many2one('salle.classe', 'Numéro Salle')

    @api.constrains('emploie_ids')
    def _check_lecture(self):
        '''Method to check same lecture is not assigned on same day'''
        if self.emploie_type == 'reguliere':
            domain = [('table_id', 'in', self.ids)]
            ligne_ids = self.env['emploie.emploie.details'].search(domain)
            for rec in ligne_ids:
                records = [rec_check.id for rec_check in ligne_ids
                           if (rec.jour_semaine == rec_check.jour_semaine and
                               rec.heure_debut == rec_check.heure_debut and
                               rec.heure_fin == rec_check.heure_fin and
                               rec.enseignant_id.id == rec.enseignant_id.id)]
                if len(records) > 1:
                    raise ValidationError(_('''Vous ne pouvez pas définir la conférence en même temps
                                            heure% s le même jour% s pour enseignant
                                            %s..!''') % (rec.heure_debut,
                                                         rec.jour_semaine,
                                                         rec.enseignant_id.par))
                # Checks if time is greater than 24 hours than raise error
                if rec.heure_debut > 24:
                    raise ValidationError(_('''le temps de début devrait être inférieur à
                                            24 heures!'''))
                if rec.heure_fin > 24:
                    raise ValidationError(_('''L'heure de fin doit être inférieure à
                                            24 heures!'''))
            return True


class emploidetail(models.Model):
    _description = 'emploie detail'
    _name = 'emploie.emploie.details'
    _rec_name = 'table_id'

    @api.multi
    @api.constrains('enseignant_id', 'matiere_id')
    def check_enseignant(self):
        '''Check if lecture is not related to enseignant than raise error'''
        if (self.enseignant_id.id not in self.matiere_id.enseignant_ids.ids and
                self.table_id.emploie_type == 'reguliere'):
                                raise ValidationError(_('''La matière% s n'est pas affectée à
                                enseignant %s.''') % (self.matiere_id.par,
                                                       self.enseignant_id.par))

    enseignant_id = fields.Many2one('ecole.enseignant', 'Nom Enseignant',
                                 help="Selectionnez enseignant")
    matiere_id = fields.Many2one('matiere.matiere', 'Nom Matière',
                                 help="Selectionnez matiere")
    table_id = fields.Many2one('emploie.emploie', 'Calendrier')
    heure_debut = fields.Float('Heure Debut', required=True,
                              help="Heure selon format horaire de 24 heures")
    heure_fin = fields.Float('Heure Fin', required=True,
                            help="Time according to timeformat of 24 hours")
    jour_semaine = fields.Selection([('lundi', 'Lundi'),
                                 ('mardi', 'Mardi'),
                                 ('mercredi', 'Mercredi'),
                                 ('jeudi', 'Jeudi'),
                                 ('vendredi', 'Vendredi'),
                                 ('samedi', 'Samedi'),
                                 ('dimanche', 'Dimanche')], "Jour de semaine",)
    salle_classe_id = fields.Many2one('salle.classe', 'Numéro Salle')

    @api.constrains('enseignant_id', 'salle_classe_id')
    def check_enseignant_salle(self):
        emploie_rec = self.env['emploie.emploie'].search([('id', '!=',
                                                        self.table_id.id)])
        if emploie_rec:
            for data in emploie_rec:
                for record in data.emploie_ids:
                    if (data.emploie_type == 'reguliere' and
                            self.table_id.emploie_type == 'reguliere' and
                            self.enseignant_id == record.enseignant_id and
                            self.jour_semaine == record.jour_semaine and
                            self.heure_debut == record.heure_debut):
                            raise ValidationError(_('''Il y a une conférence de
                            Conférencier en même temps!'''))
                    if (data.emploie_type == 'reguliere' and
                            self.table_id.emploie_type == 'reguliere' and
                            self.salle_classe_id == record.salle_classe_id and
                            self.heure_debut == record.heure_debut):
                            raise ValidationError(_("la salle est occupé ."))


class matierematiere2(models.Model):
    _inherit = "matiere.matiere"

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False,
                access_rights_uid=None):
        '''Override method to get matiere related to enseignant'''
        enseignant_id = self._context.get('enseignant_id')
        if enseignant_id:
            for enseignant_data in self.env['ecole.enseignant'].browse(enseignant_id):
                args.append(('enseignant_ids', 'in', [enseignant_data.id]))
        return super(matierematiere2, self)._search(
            args=args, offset=offset, limit=limit, order=order, count=count,
            access_rights_uid=access_rights_uid)
