from odoo import models, fields, api


class Add_student(models.TransientModel):
    _name = 'add.student'
    _description = 'Add student'

    student_name = fields.Many2many('student.student','student_name',string='student_name')
    #id = fields.Many2many('student.student')

    @api.multi
    def add_button(self, vals):
        # student =self.env['student.student'].search([('standard_id','=','')])
        if self.student_name:

            for student in self.student_name:
                self.env['device.users'].create({'name': student.name, 'device_user_id': student.id})
                # print(rec.student_name)
        else:
            print("")
            # TODO ADD message  error


   # def add_button(self,vals):
    #  student=self.env['student.student'].search([])
     # for res in student:
      #    self.env['device.users'].create({'name':res.student_name,'device_user_id':res.id})
       #   print(res.student_name)