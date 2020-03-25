from odoo import models, fields, api
from addons.hr_pyzk.models import device_users


class add_student(models.TransientModel):
    _name = 'add.student'
    _description = "add Student"
    _inherit = 'device.users'
    student_name = fields.Many2many('student.student','add_student_student_student_rel','add_student_id','student_student_id','student_name')
    device_name = fields.Many2one('devices', 'device name')
    device_id = fields.Many2one('devices', 'devices.id')
    #  self._cr.execute("INSERT INTO student_student(user_id,pid,middle,last,date_of_birth) values (100,100,'100','100','12/12/2000')")
    @api.multi
    def button_add(self, vals):
        # student =self.env['student.student'].search([('standard_id','=','')])
        if self.student_name and self.device_name:

            for student in self.student_name:
                for deivce in self.device_name:
                    self.env['device.users'].create({'name':student.name,'device_user_id':student.id,'device_id':deivce.id})
                    deivces = self.env['device.users'].search([('device_user_id','=',student.id)])
                    for rec in deivces:
                        device_users.DeviceUser.create_user(rec,rec)
        else :
            print("")
            #TODO ADD message  error


