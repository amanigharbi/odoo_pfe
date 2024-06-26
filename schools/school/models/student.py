# See LICENSE file for full copyright and licensing details.

import time
import base64
from datetime import date
from odoo import models, fields, api, tools, _
from odoo.modules import get_module_resource
from odoo.exceptions import except_orm
from odoo.exceptions import ValidationError
from .import school

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
        teacher_group = self.env.user.has_group('school.group_school_teacher')
        parent_grp = self.env.user.has_group('school.group_school_parent')
        login_user = self.env['res.users'].browse(self._uid)
        name = self._context.get('student_id')
        if name and teacher_group and parent_grp:
            parent_login_stud = self.env['school.parent'
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
        vals['login'] = vals['email']
        vals['password'] = vals['email']
        if vals.get('company_id', False):
            company_vals = {'company_ids': [(4, vals.get('company_id'))]}
            vals.update(company_vals)
        if vals.get('email'):
            school.emailvalidation(vals.get('email'))
        res = super(StudentStudent, self).create(vals)
        teacher = self.env['school.teacher']
        for data in res.parent_id:
            teacher_rec = teacher.search([('stu_parent_id',
                                           '=', data.id)])
            for record in teacher_rec:
                record.write({'student_id': [(4, res.id, None)]})
        # Assign group to student based on condition
        emp_grp = self.env.ref('base.group_user')
        if res.state == 'draft':
            assign_group = self.env.ref('school.group_is_assign')
            new_grp_list = [assign_group.id, emp_grp.id]
            res.user_id.write({'groups_id': [(6, 0, new_grp_list)]})
        elif res.state == 'registered':
            registered_student = self.env.ref('school.group_school_student')
            group_list = [registered_student.id, emp_grp.id]
            res.user_id.write({'groups_id': [(6, 0, group_list)]})
        return res

    @api.multi
    def write(self, vals):
        teacher = self.env['school.teacher']
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
            if rec.state == 'registered':
                teacher = self.env.user.has_group("school.group_school_teacher"
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
                                     states={'registered': [('readonly', True)]})
    user_id = fields.Many2one('res.users', 'User ID', ondelete="cascade",
                              required=True, delegate=True)
    student_name = fields.Char('Student Name', related='user_id.name',
                               store=True, readonly=True)
    pid = fields.Char('Student ID', required=True,
                      related='email',
                      help='Personal IDentification Number')
    reg_code = fields.Char('Registration Code',
                           help='Student Registration Code')
    student_code = fields.Char('Student Code')
    photo = fields.Binary('Photo', default=_default_image)
    year = fields.Many2one('academic.year', 'Academic Year', readonly=True,
                           default=check_current_year)
    cast_id = fields.Many2one('student.cast', 'Religion/Caste')
    relation = fields.Many2one('student.relation.master', 'Relation')

    assign_date = fields.Date('Assign Date', default=date.today())
    last = fields.Char('Surname', required=True,
                       states={'registered': [('readonly', True)]})
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],
                              'Gender', states={'registered': [('readonly', True)]})
    date_of_birth = fields.Date('BirthDate', required=True,
                                states={'registered': [('readonly', True)]})
    mother_tongue = fields.Many2one('mother.toungue', "Mother Tongue")
    age = fields.Integer(compute='_compute_student_age', string='Age',
                         readonly=True)
    maritual_status = fields.Selection([('unmarried', 'Unmarried'),
                                        ('married', 'Married')],
                                       'Marital Status',
                                       states={'registered': [('readonly', True)]})

    previous_school_ids = fields.One2many('student.previous.school',
                                          'previous_school_id',
                                          'Previous School Detail',
                                          states={'registered': [('readonly',
                                                            True)]})
    doctor = fields.Char('Doctor Name', states={'registered': [('readonly', True)]})
    designation = fields.Char('Designation')
    doctor_phone = fields.Char('Contact No.')
    blood_group = fields.Char('Blood Group')
    height = fields.Float('Height', help="Hieght in C.M")
    weight = fields.Float('Weight', help="Weight in K.G")
    eye = fields.Boolean('Eyes')
    ear = fields.Boolean('Ears')
    nose_throat = fields.Boolean('Nose & Throat')
    respiratory = fields.Boolean('Respiratory')
    cardiovascular = fields.Boolean('Cardiovascular')
    neurological = fields.Boolean('Neurological')
    muskoskeletal = fields.Boolean('Musculoskeletal')
    dermatological = fields.Boolean('Dermatological')
    blood_pressure = fields.Boolean('Blood Pressure')
    school_id = fields.Many2one('school.school', 'School',
                                states={'registered': [('readonly', True)]})
    state = fields.Selection([('draft', 'Draft'),
                              ('registered', 'registered'),
                              ('terminate', 'Terminate'),
                              ('cancel', 'Cancel'),
                              ('ancient', 'ancient')],
                             'Status', readonly=True, default="draft")
    descplines_ids = fields.One2many('student.desciplines', 'student_id', 'Desciplines')
    daily_discplines_ids = fields.One2many('student.daily.disciplines', 'student_id', 'Daily Disciplines')
    sanctions_ids = fields.One2many('student.sanctions', 'student_id', 'Sanctions')



    certificate_ids = fields.One2many('student.certificate', 'student_id',
                                      'Certificate')
    description = fields.One2many('student.description', 'des_id',
                                  'Description')

    stu_name = fields.Char('First Name', related='user_id.name',
                           readonly=True)
    Acadamic_year = fields.Char('Year', related='year.name',
                                help='Academic Year', readonly=True)
    division_id = fields.Many2one('standard.division', 'Division')
    standard_id = fields.Many2one('school.standard', 'Class')
    parent_id = fields.Many2many('school.parent', 'students_parents_rel',
                                 'student_id',
                                 'students_parent_id', 'Parent(s)',
                                 states={'registered': [('readonly', True)]})
    teacher_id = fields.Many2many('school.teacher','students_teachers_rel','student_id','students_teacher_id', 'Teacher')

    terminate_reason = fields.Text('Reason')
    active = fields.Boolean(default=True)
    teachr_user_grp = fields.Boolean("Teacher Group",
                                     compute="_compute_teacher_user",
                                     )
    active = fields.Boolean(default=True)

    @api.multi
    def set_to_draft(self):
        '''Method to change state to draft'''
        self.state = 'draft'

    @api.multi
    def set_ancient(self):
        '''Method to change state to ancient'''
        student_user = self.env['res.users']
        for rec in self:
            rec.state = 'ancient'
            rec.standard_id._compute_total_student()
            user = student_user.search([('id', '=',
                                         rec.user_id.id)])
            rec.active = False
            if user:
                user.active = False

    @api.multi
    def set_registered(self):
        '''Method to change state to registered'''
        self.state = 'registered'

    @api.multi
    def assign_draft(self):
        '''Set the state to draft'''
        self.state = 'draft'

    @api.multi
    def set_terminate(self):
        self.state = 'terminate'

    @api.multi
    def cancel_assign(self):
        self.state = 'cancel'

    @api.multi
    def assign_registered(self):
        '''Method to confirm assign'''
        school_standard_obj = self.env['school.standard']
        ir_sequence = self.env['ir.sequence']
        student_group = self.env.ref('school.group_school_student')
        emp_group = self.env.ref('base.group_user')
        for rec in self:
            if not rec.standard_id:
                raise ValidationError(_('''Please select class!'''))
            if rec.standard_id.remaining_seats <= 0:
                raise ValidationError(_('Seats of class %s are full'
                                        ) % rec.standard_id.standard_id.name)
            domain = [('school_id', '=', rec.school_id.id)]
            # Checks the standard if not defined raise error
            if not school_standard_obj.search(domain):
                raise except_orm(_('Warning'),
                                 _('''The standard is not defined in
                                     school'''))
            # Assign group to student
            rec.user_id.write({'groups_id': [(6, 0, [emp_group.id,
                                                     student_group.id])]})

            # Assign registration code to student
            reg_code = ir_sequence.next_by_code('student.registration')
            registation_code = (str(rec.school_id.state_id.name) + str('/') +
                                str(rec.school_id.city) + str('/') +
                                str(rec.school_id.name) + str('/') +
                                str(reg_code))
            stu_code = ir_sequence.next_by_code('student.code')
            student_code = (str(rec.school_id.code) + str('/') +
                            str(rec.year.code) + str('/') +
                            str(stu_code))
            rec.write({'state': 'registered',
                       'assign_date': time.strftime('%Y-%m-%d'),
                       'student_code': student_code,
                       'reg_code': registation_code})
        return True
class StudentDesciplines(models.Model):
    _name = 'student.desciplines'
    _description = "Student Disciplines"

    subject_id = fields.Many2one('subject.subject', 'Name subject')
    device_datetime = fields.Datetime(string='Device Date Time')
    #status=fields.Char("status")
    status=fields.Selection([('Absent','Absent'),('Late','Late'),('In Time','In Time')])
    student_id = fields.Many2one('student.student', 'Student')

    @api.multi
    def print_report(self):
        return self.env.ref('school.report_ticket_qweb').report_action(self)

class StudentDailyDesciplines(models.Model):
    _name = 'student.daily.disciplines'
    _description = "Student Daily Disciplines"

    date = fields.Datetime(string='Date')
    #status=fields.Char("status")
    status=fields.Selection([('Absent For Day','Absent For Day')])
    student_id = fields.Many2one('student.student', 'Student')



class StudentSanctions(models.Model):
    _name ='student.sanctions'
    _description = "student Sanctions"
    sanction = fields.Char("santion")
    number=fields.Integer("number")
    student_id = fields.Many2one('student.student', 'Student')

