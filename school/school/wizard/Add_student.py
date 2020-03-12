from odoo import models, fields, api
from addons.hr_pyzk.models import device_users


class Add_student(models.TransientModel):
    _name = 'add.student'
    _description = 'Add student'

    student_name = fields.Many2many('student.student','student_name',string='student_name')
    device_id = fields.Many2one('devices', 'Fingerprint Device')
    #id = fields.Many2many('student.student')

    @api.multi
    def add_button(self, vals):
        # student =self.env['student.student'].search([('standard_id','=','')])
        if self.student_name and self.device_id:
         for student in self.student_name:
           for device in self.device_id:
                self.env['device.users'].create({'name': student.name, 'device_user_id': student.id,'device_id': device.id})
                # print(rec.student_name)
        else:
            print("")
            # TODO ADD message  error

        #device_users.create_user(self,device)

   # def add_button(self,vals):
    #  student=self.env['student.student'].search([])
     # for res in student:
      #    self.env['device.users'].create({'name':res.student_name,'device_user_id':res.id})
       #   print(res.student_name)