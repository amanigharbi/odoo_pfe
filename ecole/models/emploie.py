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

    name = fields.Char('Déscription')
    standard_id = fields.Many2one('ecole.standard', 'Classe Académique',
                                  required=True,
                                  help="Select Standard")
    year_id = fields.Many2one('academic.year', 'Année', required=True,
                              help="select annee academique")
    emploie_ids = fields.One2many('emploie.emploie.line', 'table_id', 'Calendrier')
    emploie_type = fields.Selection([('regular', 'Regular')],
                                      'emploie Type', default="regular",
                                      inivisible=True)
    user_ids = fields.Many2many('res.users', string="Utilisateur",
                                compute="_compute_user", store=True)
    class_room_id = fields.Many2one('class.room', 'Numéro Salle')

    @api.constrains('emploie_ids')
    def _check_lecture(self):
        '''Method to check same lecture is not assigned on same day'''
        if self.emploie_type == 'regular':
            domain = [('table_id', 'in', self.ids)]
            line_ids = self.env['emploie.emploie.line'].search(domain)
            for rec in line_ids:
                records = [rec_check.id for rec_check in line_ids
                           if (rec.week_day == rec_check.week_day and
                               rec.start_time == rec_check.start_time and
                               rec.end_time == rec_check.end_time and
                               rec.enseignant_id.id == rec.enseignant_id.id)]
                if len(records) > 1:
                    raise ValidationError(_('''You cannot set lecture at same
                                            time %s  at same day %s for enseignant
                                            %s..!''') % (rec.start_time,
                                                         rec.week_day,
                                                         rec.enseignant_id.name))
                # Checks if time is greater than 24 hours than raise error
                if rec.start_time > 24:
                    raise ValidationError(_('''Start Time should be less than
                                            24 hours!'''))
                if rec.end_time > 24:
                    raise ValidationError(_('''End Time should be less than
                                            24 hours!'''))
            return True


class emploieLine(models.Model):
    _description = 'emploie Line'
    _name = 'emploie.emploie.line'
    _rec_name = 'table_id'

    @api.multi
    @api.constrains('enseignant_id', 'subject_id')
    def check_enseignant(self):
        '''Check if lecture is not related to enseignant than raise error'''
        if (self.enseignant_id.id not in self.subject_id.enseignant_ids.ids and
                self.table_id.emploie_type == 'regular'):
            raise ValidationError(_('''The subject %s is not assigned to
                                    enseignant %s.''') % (self.subject_id.name,
                                                       self.enseignant_id.name))

    enseignant_id = fields.Many2one('ecole.enseignant', 'Nom Enseignant',
                                 help="Select enseignant")
    subject_id = fields.Many2one('subject.subject', 'Nom Matière',
                                 help="Select Subject")
    table_id = fields.Many2one('emploie.emploie', 'Calendrier')
    start_time = fields.Float('Heure Debut', required=True,
                              help="Time according to timeformat of 24 hours")
    end_time = fields.Float('Heure Fin', required=True,
                            help="Time according to timeformat of 24 hours")
    week_day = fields.Selection([('lundi', 'Lundi'),
                                 ('mardi', 'Mardi'),
                                 ('mercredi', 'Mercredi'),
                                 ('jeudi', 'Jeudi'),
                                 ('vendredi', 'Vendredi'),
                                 ('samedi', 'Samedi'),
                                 ('dimanche', 'Dimanche')], "Jour de semaine",)
    class_room_id = fields.Many2one('class.room', 'Numéro Salle')

    @api.constrains('enseignant_id', 'class_room_id')
    def check_enseignant_room(self):
        emploie_rec = self.env['emploie.emploie'].search([('id', '!=',
                                                        self.table_id.id)])
        if emploie_rec:
            for data in emploie_rec:
                for record in data.emploie_ids:
                    if (data.emploie_type == 'regular' and
                            self.table_id.emploie_type == 'regular' and
                            self.enseignant_id == record.enseignant_id and
                            self.week_day == record.week_day and
                            self.start_time == record.start_time):
                            raise ValidationError(_('''There is a lecture of
                            Lecturer at same time!'''))
                    if (data.emploie_type == 'regular' and
                            self.table_id.emploie_type == 'regular' and
                            self.class_room_id == record.class_room_id and
                            self.start_time == record.start_time):
                            raise ValidationError(_("The room is occupied."))


class SubjectSubject2(models.Model):
    _inherit = "subject.subject"

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False,
                access_rights_uid=None):
        '''Override method to get subject related to enseignant'''
        enseignant_id = self._context.get('enseignant_id')
        if enseignant_id:
            for enseignant_data in self.env['ecole.enseignant'].browse(enseignant_id):
                args.append(('enseignant_ids', 'in', [enseignant_data.id]))
        return super(SubjectSubject2, self)._search(
            args=args, offset=offset, limit=limit, order=order, count=count,
            access_rights_uid=access_rights_uid)
