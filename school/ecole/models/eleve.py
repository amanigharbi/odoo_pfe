# See LICENSE file for full copyright and licensing details.

import time
import base64
from datetime import date
from odoo import models, fields, api, tools, _
from odoo.modules import get_module_resource
from odoo.exceptions import except_orm
from odoo.exceptions import ValidationError
from .import ecole

# from lxml import etree
# added import statement in try-except because when server runs on
# windows operating system issue arise because this library is not in Windows.
try:
    from odoo.tools import image_colorize, image_resize_image_big
except:
    image_colorize = False
    image_resize_image_big = False


class StudentStudent(models.Model):
    ''' Defining a student information '''
    _name = 'student.student'
    _table = "student_student"
    _description = 'Student Information'

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False,
                access_rights_uid=None):
        '''Method to get student of parent having group teacher'''
        teacher_group = self.env.user.has_group('ecole.group_ecole_teacher')
        parent_grp = self.env.user.has_group('ecole.group_ecole_parent')
        login_user = self.env['res.users'].browse(self._uid)
        name = self._context.get('student_id')
        if name and teacher_group and parent_grp:
            parent_login_stud = self.env['ecole.parent'
                                         ].search([('partner_id', '=',
                                                  login_user.partner_id.id)
                                                   ])
            childrens = parent_login_stud.student_id
            args.append(('id', 'in', childrens.ids))
        return super(StudentStudent, self)._search(
            args=args, offset=offset, limit=limit, order=order, count=count,
            access_rights_uid=access_rights_uid)

    @api.depends('date_of_birth')
    def _compute_student_age(self):
        '''Method to calculate student age'''
        current_dt = date.today()
        for rec in self:
            if rec.date_of_birth:
                start = rec.date_of_birth
                age_calc = ((current_dt - start).days / 365)
                # Age should be greater than 0
                if age_calc > 0.0:
                    rec.age = age_calc

    @api.constrains('date_of_birth')
    def check_age(self):
        '''Method to check age should be greater than 5'''
        current_dt = date.today()
        if self.date_of_birth:
            start = self.date_of_birth
            age_calc = ((current_dt - start).days / 365)
            # Check if age less than 5 years
            if age_calc < 5:
                raise ValidationError(_('''Age of student should be greater
                than 5 years!'''))

    @api.model
    def create(self, vals):
        '''Method to create user when student is created'''
        if vals.get('pid', _('New')) == _('New'):
            vals['pid'] = self.env['ir.sequence'
                                   ].next_by_code('student.student'
                                                  ) or _('New')
        if vals.get('pid', False):
            vals['login'] = vals['pid']
            vals['password'] = vals['pid']
        else:
            raise except_orm(_('Error!'),
                             _('''PID not valid
                                 so record will not be saved.'''))
        if vals.get('company_id', False):
            company_vals = {'company_ids': [(4, vals.get('company_id'))]}
            vals.update(company_vals)
        if vals.get('email'):
            ecole.emailvalidation(vals.get('email'))
        res = super(StudentStudent, self).create(vals)
        teacher = self.env['ecole.teacher']
        for data in res.parent_id:
            teacher_rec = teacher.search([('stu_parent_id',
                                           '=', data.id)])
            for record in teacher_rec:
                record.write({'student_id': [(4, res.id, None)]})
        # Assign group to student based on condition
        emp_grp = self.env.ref('base.group_user')
        if res.state == 'draft':
            admission_group = self.env.ref('ecole.group_is_admission')
            new_grp_list = [admission_group.id, emp_grp.id]
            res.user_id.write({'groups_id': [(6, 0, new_grp_list)]})
        elif res.state == 'done':
            done_student = self.env.ref('ecole.group_ecole_student')
            group_list = [done_student.id, emp_grp.id]
            res.user_id.write({'groups_id': [(6, 0, group_list)]})
        return res

    @api.multi
    def write(self, vals):
        teacher = self.env['ecole.teacher']
        if vals.get('parent_id'):
            for parent in vals.get('parent_id')[0][2]:
                teacher_rec = teacher.search([('stu_parent_id',
                                               '=', parent)])
                for data in teacher_rec:
                    data.write({'student_id': [(4, self.id)]})
        return super(StudentStudent, self).write(vals)

    @api.model
    def _default_image(self):
        '''Method to get default Image'''
        image_path = get_module_resource('hr', 'static/src/img',
                                         'default_image.png')
        return tools.image_resize_image_big(base64.b64encode(open(image_path,
                                                                  'rb').read()
                                                             ))

    @api.depends('state')
    def _compute_teacher_user(self):
        for rec in self:
            if rec.state == 'done':
                teacher = self.env.user.has_group("ecole.group_ecole_teacher"
                                                  )
                if teacher:
                    rec.teachr_user_grp = True

    @api.model
    def check_current_year(self):
        '''Method to get default value of logged in Student'''
        res = self.env['academic.year'].search([('current', '=',
                                                 True)])
        if not res:
            raise ValidationError(_('''There is no current Academic Year
                                    defined!Please contact to Administator!'''
                                    ))
        return res.id

    family_con_ids = fields.One2many('student.family.contact',
                                     'family_contact_id',
                                     'Family Contact Detail',
                                     states={'done': [('readonly', True)]})
    user_id = fields.Many2one('res.users', 'User ID', ondelete="cascade",
                              required=True, delegate=True)
    student_name = fields.Char('Nom Elève', related='user_id.name',
                               store=True, readonly=True)
    pid = fields.Char('ID Elève', required=True,
                      default=lambda self: _('New'),
                      help='Personal IDentification Number')
    reg_code = fields.Char('Code Registration',
                           help='Student Registration Code')
    student_code = fields.Char('Code Elève')
    contact_phone = fields.Char('Numéro Téléphone.')
    contact_mobile = fields.Char('Numéro Portable')
    roll_no = fields.Integer('Numéro Roll.', readonly=True)
    photo = fields.Binary('Photo', default=_default_image)
    year = fields.Many2one('academic.year', 'Année Académique', readonly=True,
                           default=check_current_year)
    cast_id = fields.Many2one('student.cast', 'Réligion/Caste')
    relation = fields.Many2one('student.relation.master', 'Relation')

    admission_date = fields.Date('Date Admission ', default=date.today())
    middle = fields.Char('Deuxième Nom', required=True,
                         states={'done': [('readonly', True)]})
    last = fields.Char('Surname', required=True,
                       states={'done': [('readonly', True)]})
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],
                              'Sexe', states={'done': [('readonly', True)]})
    date_of_birth = fields.Date('Date De Naissance', required=True,
                                states={'done': [('readonly', True)]})
    mother_tongue = fields.Many2one('mother.toungue', "Langue Maternelle")
    age = fields.Integer(compute='_compute_student_age', string='Age',
                         readonly=True)
    maritual_status = fields.Selection([('célibataire', 'célibataire'),
                                        ('Marié', 'Marié')],
                                       'Marital Status',
                                       states={'done': [('readonly', True)]})
    reference_ids = fields.One2many('student.reference', 'reference_id',
                                    'Réferences',
                                    states={'done': [('readonly', True)]})
    previous_ecole_ids = fields.One2many('student.previous.ecole',
                                          'previous_ecole_id',
                                          'Détail École précédente',
                                          states={'done': [('readonly',
                                                            True)]})
    doctor = fields.Char('Doctor Name', states={'done': [('readonly', True)]})
    designation = fields.Char('Désignation')
    doctor_phone = fields.Char('Numéro Contact.')
    blood_group = fields.Char('Groupe Sanguin')
    height = fields.Float('Hauteur', help="Hieght in C.M")
    weight = fields.Float('Largeur', help="Weight in K.G")
    eye = fields.Boolean('Yeux')
    ear = fields.Boolean('Oreilles')
    nose_throat = fields.Boolean('Nez et gorge')
    respiratory = fields.Boolean('Respiratoire')
    cardiovascular = fields.Boolean('Cardiovasculaire')
    neurological = fields.Boolean('Neurologique')
    muskoskeletal = fields.Boolean('Appareil locomoteur')
    dermatological = fields.Boolean('Dermatologique')
    blood_pressure = fields.Boolean('Pression artérielle')
    remark = fields.Text('Remark', states={'done': [('readonly', True)]})
    ecole_id = fields.Many2one('ecole.ecole', 'Ecole',
                                states={'done': [('readonly', True)]})
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('terminate', 'Terminate'),
                              ('cancel', 'Cancel'),
                              ('alumni', 'Alumni')],
                             'Status', readonly=True, default="draft")
    history_ids = fields.One2many('student.history', 'student_id', 'Historique')
    descplines_ids = fields.One2many('student.desciplines', 'student_id', 'Desciplines')
    certificate_ids = fields.One2many('student.certificate', 'student_id',
                                      'Certificat')
    student_discipline_line = fields.One2many('student.descipline',
                                              'student_id', 'Descipline')
    document = fields.One2many('student.document', 'doc_id', 'Documents')
    description = fields.One2many('student.description', 'des_id',
                                  'Déscription')
    award_list = fields.One2many('student.award', 'award_list_id',
                                 'Liste des prix')
    stu_name = fields.Char('Prénom', related='user_id.name',
                           readonly=True)
    Acadamic_year = fields.Char('Année', related='year.name',
                                help='Academic Year', readonly=True)
    division_id = fields.Many2one('standard.division', 'Division')
    medium_id = fields.Many2one('standard.medium', 'Medium')
    standard_id = fields.Many2one('ecole.standard', 'Classe')
    parent_id = fields.Many2many('ecole.parent', 'students_parents_rel',
                                 'student_id',
                                 'students_parent_id', 'Parent(s)',
                                 states={'done': [('readonly', True)]})
    terminate_reason = fields.Text('Raison')
    active = fields.Boolean(default=True)
    teachr_user_grp = fields.Boolean("Groupe Enseignant",
                                     compute="_compute_teacher_user",
                                     )
    active = fields.Boolean(default=True)

    @api.multi
    def set_to_draft(self):
        '''Method to change state to draft'''
        self.state = 'draft'

    @api.multi
    def set_alumni(self):
        '''Method to change state to alumni'''
        student_user = self.env['res.users']
        for rec in self:
            rec.state = 'alumni'
            rec.standard_id._compute_total_student()
            user = student_user.search([('id', '=',
                                         rec.user_id.id)])
            rec.active = False
            if user:
                user.active = False

    @api.multi
    def set_done(self):
        '''Method to change state to done'''
        self.state = 'done'

    @api.multi
    def admission_draft(self):
        '''Set the state to draft'''
        self.state = 'draft'

    @api.multi
    def set_terminate(self):
        self.state = 'terminate'

    @api.multi
    def cancel_admission(self):
        self.state = 'cancel'

    @api.multi
    def admission_done(self):
        '''Method to confirm admission'''
        ecole_standard_obj = self.env['ecole.standard']
        ir_sequence = self.env['ir.sequence']
        student_group = self.env.ref('ecole.group_ecole_student')
        emp_group = self.env.ref('base.group_user')
        for rec in self:
            if not rec.standard_id:
                raise ValidationError(_('''SVP Séléctionnez Classe!'''))
            if rec.standard_id.remaining_seats <= 0:
                raise ValidationError(_('Seats of class %s are full'
                                        ) % rec.standard_id.standard_id.name)
            domain = [('ecole_id', '=', rec.ecole_id.id)]
            # Checks the standard if not defined raise error
            if not ecole_standard_obj.search(domain):
                raise except_orm(_('Avertissement'),
                                 _('''Standard Non trouvé dans
                                     ecole'''))
            # Assign group to student
            rec.user_id.write({'groups_id': [(6, 0, [emp_group.id,
                                                     student_group.id])]})
            # Assign roll no to student
            number = 1
            for rec_std in rec.search(domain):
                rec_std.roll_no = number
                number += 1
            # Assign registration code to student
            reg_code = ir_sequence.next_by_code('student.registration')
            registation_code = (str(rec.ecole_id.state_id.name) + str('/') +
                                str(rec.ecole_id.city) + str('/') +
                                str(rec.ecole_id.name) + str('/') +
                                str(reg_code))
            stu_code = ir_sequence.next_by_code('student.code')
            student_code = (str(rec.ecole_id.code) + str('/') +
                            str(rec.year.code) + str('/') +
                            str(stu_code))
            rec.write({'state': 'done',
                       'admission_date': time.strftime('%Y-%m-%d'),
                       'student_code': student_code,
                       'reg_code': registation_code})
        return True
class StudentDesciplines(models.Model):
    _name = 'student.desciplines'
    _description = "Student Disciplines"

    subject_id = fields.Many2one('subject.subject', 'Nom Matière')
    device_datetime = fields.Many2one('device.attendances','Date/Heure Machine')
    status=fields.Char("status")
    student_id = fields.Many2one('student.student', 'Elève')

    class TimeTable(models.Model):
        _description = 'Time Table'
        _name = 'time.table'

        @api.depends('timetable_ids')
        def _compute_user(self):
            '''Method to compute user'''
            for rec in self:
                rec.user_ids = [teacher.teacher_id.employee_id.user_id.id
                                for teacher in rec.timetable_ids
                                ]
            return True

        name = fields.Char('Description')
        standard_id = fields.Many2one('ecole.standard', 'Classe Academique',
                                      required=True,
                                      help="Select Standard")
        year_id = fields.Many2one('academic.year', 'Année', required=True,
                                  help="select academic year")
        timetable_ids = fields.One2many('time.table.line', 'table_id', 'Calendrier')
        timetable_type = fields.Selection([('regular', 'Regular')],
                                          'Time Table Type', default="regular",
                                          inivisible=True)
        user_ids = fields.Many2many('res.users', string="Utilisateur",
                                    compute="_compute_user", store=True)
        class_room_id = fields.Many2one('class.room', 'Numéro Salle')

        @api.constrains('timetable_ids')
        def _check_lecture(self):
            '''Method to check same lecture is not assigned on same day'''
            if self.timetable_type == 'regular':
                domain = [('table_id', 'in', self.ids)]
                line_ids = self.env['time.table.line'].search(domain)
                for rec in line_ids:
                    records = [rec_check.id for rec_check in line_ids
                               if (rec.week_day == rec_check.week_day and
                                   rec.start_time == rec_check.start_time and
                                   rec.end_time == rec_check.end_time and
                                   rec.teacher_id.id == rec.teacher_id.id)]
                    if len(records) > 1:
                        raise ValidationError(_('''Vous ne pouvez pas définir la conférence en même temps
                                                heure% s le même jour% s pour l'enseignant
                                                %s..!''') % (rec.start_time,
                                                             rec.week_day,
                                                             rec.teacher_id.name))
                    # Checks if time is greater than 24 hours than raise error
                    if rec.start_time > 24:
                        raise ValidationError(_('''L'heure de début doit être inférieure à
                                                24 heures!'''))
                    if rec.end_time > 24:
                        raise ValidationError(_('''L'heure de fin doit être inférieure à
                                                24 heures!'''))
                return True

