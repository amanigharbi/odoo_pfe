# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
# from .pyfcm import  FCMNotification


class ParentRelation(models.Model):
    '''Defining a Parent relation with child'''
    _name = "parent.relation"
    _description = "Parent-child relation information"

    name = fields.Char("Relation name", required=True)


class SchoolParent(models.Model):
    ''' Defining a Teacher information '''
    _name = 'school.parent'
    _description = 'Parent Information'

    @api.onchange('student_id')
    def onchange_student_id(self):
        self.standard_id = [(6, 0, [])]
        self.stand_id = [(6, 0, [])]
        standard_ids = [student.standard_id.id
                        for student in self.student_id]
        if standard_ids:
            stand_ids = [student.standard_id.standard_id.id
                         for student in self.student_id]
            self.standard_id = [(6, 0, standard_ids)]
            self.stand_id = [(6, 0, stand_ids)]

    notification_ids = fields.One2many('history.notification', 'parent_id', 'Notification')
    partner_id = fields.Many2one('res.partner', 'User ID', ondelete="cascade",
                                 delegate=True, required=True)
    relation_id = fields.Many2one('parent.relation', "Relation with Child")



    student_id = fields.Many2many('student.student', 'students_parents_rel',
                                  'students_parent_id', 'student_id',
                                  'Children')
    standard_id = fields.Many2many('school.standard',
                                   'school_standard_parent_rel',
                                   'class_parent_id', 'class_id',
                                   'Academic Class')
    stand_id = fields.Many2many('standard.standard',
                                'standard_standard_parent_rel',
                                'standard_parent_id', 'standard_id',
                                'Academic Standard')
    teacher_id = fields.Many2one('school.teacher', 'Teacher',
                                 related="standard_id.user_id", store=True)
    registration_id_mobile= fields.Char('Registration mobile')

    @api.model
    def create(self, vals):
        parent_id = super(SchoolParent, self).create(vals)
        parent_grp_id = self.env.ref('school.group_school_parent')
        emp_grp = self.env.ref('base.group_user')
        parent_group_ids = [emp_grp.id, parent_grp_id.id]
        if vals.get('parent_create_mng'):
            return parent_id
        user_vals = {'name': parent_id.name,
                     'login': parent_id.email,
                     'email': parent_id.email,
                     'partner_id': parent_id.partner_id.id,
                     'groups_id': [(6, 0, parent_group_ids)]
                     }
        self.env['res.users'].create(user_vals)
        return parent_id

    @api.onchange('state_id')
    def onchange_state(self):
        self.country_id = False
        if self.state_id:
            self.country_id = self.state_id.country_id.id
class history_notification(models.Model):
        _name = 'history.notification'
        _description = "history notification"

        student_id = fields.Many2one('student.student', 'Name student')
        title = fields.Char("Title")
        message = fields.Char("Message")
        status_message = fields.Selection([('In Progress','In Progress'),('Sent','Sent'),],'Status of Message')
        parent_id = fields.Many2one('school.parent','Parents')
        def get_notif(title,message,reg_id):
                push_service = FCMNotification(api_key="AAAAHTeART0:APA91bF8366zxEmL8KA5cwv6tDvH9mg8_iemweE_WkUDf0fvssh-4um9Cbf0o9ucINkQa2w_7LCcblAjl2rBO9d2u4Od9I5wn-7Qlb7E4nLDQ6eJvKX8CqNs8yL5jN4464CgpTYZ96of")
                print("push",push_service)
                result =push_service.notify_single_device(registration_id=reg_id,
                                                              message_title='Notification '+title,
                                                              message_body=message)
                
                return result