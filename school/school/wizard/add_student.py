
from odoo import models, fields, api
from addons.hr_pyzk.models import device_users
from odoo.exceptions import except_orm
import datetime


class add_student(models.TransientModel):
    _name = 'add.student'
    _description = "add student"
    _inherit = 'device.users'
    student_name = fields.Many2many('student.student','add_student_student_student_rel','add_student_id','student_student_id','Name student')
    device_name = fields.Many2one('devices', 'Device Name')
    device_id = fields.Many2one('devices', 'devices.id')
    #  self._cr.execute("INSERT INTO student_student(user_id,pid,middle,last,date_de_naissance) values (100,100,'100','100','12/12/2000')")
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
            raise except_orm(('Warning'),('''Select student/device please!!!'''))

# action planifié du pointage d'élève
    def test_attendance_student(self):
        local_day = datetime.date.today().strftime("%A")

        device_user_object = self.env['device.users']
        device_attendances_object = self.env['device.attendances']
        odoo_users = device_user_object.search([])

        user_punches2 = []
        user_punches2.clear()
        all_attendance = []
        all_attendance.clear()
        user_clocks = []
        user_clocks.clear()
        attendance = []
        attendance.clear()

        for user in odoo_users:
            device_attendances = []
            device_attendances.clear()
            device_attendances = device_attendances_object.search(
                [('device_user_id', '=', user.id), ('attendance_state', '=', 0)])

            if len(device_attendances) != 0:
                user_punches = [[int(x.device_user_id), datetime.datetime.strptime(str(x.device_datetime),
                                                                                   '%Y-%m-%d %H:%M:%S'),
                                 x.device_punch] for x in device_attendances]
                user_punches2.extend(user_punches)
                all_attendance.extend(attendance)


                for x in device_attendances:
                    if x.attendance_state == 0:
                        x.attendance_state = 1

                #for x in device_attendances:
                    student_id = x.device_user_id.device_user_id
                    last_date = datetime.datetime.strptime(str(x.device_datetime), '%Y-%m-%d %H:%M:%S')
                    current_time = last_date.strftime("%H.%M")
                    current_time = float(current_time) + 1.0
                    student_object = self.env['student.student'].search([('student_name', '=', x.device_user_id.name)])
                    standard = student_object.standard_id
                    name = student_object.student_name
                    parent_object = self.env['school.parent'].search([('student_id', '=', student_id)])
                    parent = parent_object.id
                    print('parent ',parent)
                    timetable_object = self.env['time.table'].search([('standard_id', '=', standard.id)])
                    timetable = timetable_object.id
                    timetable_objet_line = self.env['time.table.line'].search(
                        [('table_id', '=', timetable) and ('week_day', '=', local_day)])

                    start_time = 0
                    subject_id = 0
                    numberlate = 0
                    subject_name=''


                    for rec in timetable_objet_line:
                        if (current_time >= rec.start_time and current_time - rec.start_time <= 1 and current_time - rec.start_time >= 0):
                            start_time = rec.start_time
                            subject_id = rec.subject_id.id
                            subject_name=rec.subject_id.name
                        #else:
                            #message = ('Aucune Matière dans ce temps! ')
                            #self.env.user.notify_danger(message)
                            #break
                    search = self.env['settings.descipline'].search([])
                    late = search.max_late
                    settings_nb_avertissement = search.number_avertissement
                    settings_nb_exclu = search.number_exclu

                    print('late', late)
                    if (current_time - start_time <= late):
                        status = "Late"
                        message = ('Student ', name, ' is Late! ')
                        self.env.user.notify_info(message)
                        numberlate = numberlate + 1
                        print(numberlate)

                        message_notif=('Your Children Is Late : '+str(late)+'Min, In Subject '+subject_name+' Planned at '+str(start_time))
                        print("notif: ",message_notif)
                    else:
                        status = "Absent"
                        message = ('Student ', name, ' is Absent! ')
                        self.env.user.notify_info(message)
                        message_notif=('Your Children Is Absent  In Subject '+subject_name+' Planned at '+str(start_time))

                        print("notif: ", message_notif)
                    status_message=('en cours')
                    self.env['student.desciplines'].create(
                        {'subject_id': subject_id, 'device_datetime': last_date, 'status': status,
                         'student_id': student_id})

                    self.env['history.notification'].create(
                        {'student_id': student_id, 'title': status, 'message': message_notif, 'status_message': status_message,'parent_id':parent})



                    var = self.env['student.desciplines'].search_count(
                        [('status', '=', 'Late'), ('student_id.id', '=', student_id)])
                    search = self.env['student.sanctions'].search(
                        [('sanction', '=', 'avertissement') and ('student_id.id', '=', student_id)])
                    print('var: ', var)
                    var2 = self.env['student.sanctions'].search(
                        [('sanction', '=', 'exclu') and ('student_id.id', '=', student_id)])

                    for v in search:
                        v.unlink()
                    numberAver = int(var / settings_nb_avertissement)
                    print('number aver: ', numberAver)

                    sanction = "avertissement"

                    self.env['student.sanctions'].create(
                        {'sanction': sanction, 'number': numberAver, 'student_id': student_id})

                    for v2 in var2:
                        v2.unlink()

                    numberExclu = int(numberAver / settings_nb_exclu)
                    sanction = "exclu"

                    self.env['student.sanctions'].create(
                        {'sanction': sanction, 'number': numberExclu, 'student_id': student_id})

                # res = "Succes"
                #self.env.user.notify_success(message='Traitement Descipline Terminé!')
                #print(res)
                break
        else:
            self.env.user.notify_info(message='None Pointed Student')
            res = "None Pointed Student"
            print(res)






