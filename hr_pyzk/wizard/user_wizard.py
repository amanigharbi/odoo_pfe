# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

#from datetime import datetime
from odoo import models, fields, api, exceptions, _
import datetime
import pytz
from addons.hr_pyzk.controllers import controller as c



class UserWizard(models.TransientModel):
    _name = 'user.wizard'
    _description = 'user wizard information'
    def import_users(self): # Import User for fur Import user Wizard
        device_object = self.env['devices']
        devices = device_object.search([('state', '=', 0)])
        users_object = self.env['device.users']
        odoo_users = users_object.search([])
        odoo_users_id = [user.device_user_id for user in odoo_users]
        unique_data = c.DeviceUsers.get_users(devices)

        for user in unique_data:
            if int(user.user_id) not in odoo_users_id:
                users_object.create({
                    'device_user_id': int(user.user_id),
                    'device_uid': user.uid,
                    'name': user.name,
                })


    def import_attendance(self): # Import Attendance Wizard
        all_attendances = []
        all_attendances.clear()
        all_clocks = []
        all_clocks.clear()
        device_user_object = self.env['device.users']
        device_users = device_user_object.search([])
        attendance_object = self.env['device.attendances']
        devices_object = self.env['devices']
        devices = devices_object.search([('state', '=', 0)])
        # user_tz = self.env.user.tz
        # local = pytz.timezone(user_tz)
        # local_time = datetime.datetime.now()
        # difference = (pytz.timezone('UTC').localize(local_time) - local.localize(local_time))
        for device in devices:
            attendances = c.DeviceUsers.get_attendance(device)
            latest_rec = attendance_object.search([('device_id', '=', device.id)], limit=1)
            if latest_rec:
                latest_datetime = str(latest_rec.device_datetime)
                latest_datetime = datetime.datetime.strptime(latest_datetime, '%Y-%m-%d %H:%M:%S')
                latest_datetime = latest_datetime + datetime.timedelta(hours=device.difference)

                all_attendances = [[y.id, x[1].astimezone(pytz.utc), x[2], x[3]]
                                   for x in attendances for y in device_users if
                                   int(x[0]) == y.device_user_id and x[2] <= 1 and x[1] > latest_datetime]
            else:

                all_attendances = [[y.id, x[1].astimezone(pytz.utc), x[2], x[3]]
                                   for x in attendances for y in device_users if
                                   int(x[0]) == y.device_user_id and x[2] <= 1]
            all_clocks.extend((all_attendances))

        for a in all_clocks:
            attendance_object.create({
                'device_user_id': int(a[0]),
                'device_datetime': a[1]+ datetime.timedelta(hours=device.difference),
                'device_punch': a[2],
                #'repeat': a[4],
                'attendance_state': 0,
                'device_id': a[3],
            })

    def employee_attendance(self): # combining employee attendances
        device_user_object  = self.env['device.users']
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
        #clock = []
        #clock.clear()

        for user in odoo_users:
            device_attendances = []
            device_attendances.clear()
            device_attendances = device_attendances_object.search(
                [('device_user_id', '=', user.id), ('attendance_state', '=', 0)])

            if len(device_attendances)!=0:
                user_punches = [[int(x.device_user_id),datetime.datetime.strptime(str(x.device_datetime),
                                                                                  '%Y-%m-%d %H:%M:%S'),
                                 x.device_punch] for x in device_attendances]
                user_punches.sort()
                attendance = c.DeviceUsers.outputresult(user_punches)
                user_punches2.extend(user_punches)
                all_attendance.extend(attendance)
                #user_clocks.extend(clock)

                for record in device_attendances:
                    if record.attendance_state == 0:
                        record.attendance_state = 1
        return all_attendance

    @api.multi
    def combine_attendance(self):
        combined_attendances_object= self.env['combined.attendances']
        valid_attendances = []
        valid_attendances.clear()
        valid_attendances = self.employee_attendance()
        for attendance in valid_attendances:
            combined_attendances_object.create({
                'device_user_id': int(attendance[0]),
                'device_date': attendance[1].date(),
                'device_clockin': attendance[1],
                'device_clockout': attendance[2],
            })

    def transfer_attendance(self):
        combined_attendance_object = self.env['combined.attendances']
        hr_attendance_object = self.env['hr.attendance']
        all_data = combined_attendance_object.search([('state', '=', 'Not Transferred'), ('employee_id', '!=', False)])

        for attendance in all_data:
            # if attendance.employee_id:
            hr_attendance_object.create({
                'employee_id': attendance.employee_id.id,
                'check_in': attendance.device_clockin,
                'check_out': attendance.device_clockout,
            })

            attendance.state = 'Transferred'

    def test_attendances(self):
        """
        user_tz = self.env.user.tz
        local = pytz.timezone(user_tz)
        local_time = datetime.datetime.now()
        x = local_time.strftime("%H:%M:%S")
        difference = (pytz.timezone('UTC').localize(local_time) - local.localize(local_time))
        time = local_time+difference


        attendance_object = self.env['device.attendances']
        student_object = self.env['student.student'].search([('id','=',49)])
        classe =student_object.standard_id
        print(classe)
        emploie_object = self.env['time.table'].search([('standard_id', '=',classe.id)])
        emploie = emploie_object.id
        emploie_line_object = self.env['time.table.line'].search([('table_id', '=', emploie)])
        for rec in emploie_line_object:
            print(emploie,',',rec.table_id)



        user_object = self.env['device.users']
        devices_object = self.env['devices']
        devices = devices_object.search([('state', '=', 0)])
        for device in devices:
            latest_rec = attendance_object.search([('device_id', '=', device.id)])
            check = attendance_object.search([('device_user_id','=',0)])
            for rec in latest_rec:
                if rec:
                    latest_datetime = str(rec.device_datetime)
                    latest_datetime = datetime.datetime.strptime(latest_datetime, '%Y-%m-%d %H:%M:%S')+difference
                    time=latest_datetime.strftime("%H:%M:%S")
                    print(time)

"""
        user_tz = self.env.user.tz
        local = pytz.timezone(user_tz)
        local_time = datetime.datetime.now()
        difference = (pytz.timezone('UTC').localize(local_time) - local.localize(local_time))
        local_day = datetime.date.today().strftime("%A")
        print(local_day)
        device_user_object  = self.env['device.users']
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
        #clock = []
        #clock.clear()

        for user in odoo_users:
            device_attendances = []
            device_attendances.clear()
            device_attendances = device_attendances_object.search(
                [('device_user_id', '=', user.id), ('attendance_state', '=', 0)])

            if len(device_attendances)!=0:
                user_punches = [[int(x.device_user_id),datetime.datetime.strptime(str(x.device_datetime),
                                                                                  '%Y-%m-%d %H:%M:%S'),
                                 x.device_punch] for x in device_attendances]

                print("info last attendance",)
                user_punches2.extend(user_punches)
                all_attendance.extend(attendance)
                #user_clocks.extend(clock)

                for record in device_attendances:
                    if record.attendance_state == 0:
                        record.attendance_state = 1


                for x in device_attendances:
                    student_id=x.device_user_id.device_user_id
                    last_date = datetime.datetime.strptime(str(x.device_datetime), '%Y-%m-%d %H:%M:%S')
                    current_time = last_date.strftime("%H.%M")
                    current_time=float(current_time)+1.0
                    student_object = self.env['student.student'].search([('student_name','=',x.device_user_id.name)])
                    classe =student_object.standard_id
                    print("id classe",classe.id)
                    emploie_object = self.env['time.table'].search([('standard_id', '=',classe.id)])
                    emploie = emploie_object.id
                    emploie_line_object = self.env['time.table.line'].search([('table_id', '=', emploie) and ('week_day','=',local_day)])
                    for rec in emploie_line_object:
                        start_time =rec.start_time
                        print("id emploie",emploie,',',"table id",rec.table_id.id,", day",rec.week_day,start_time)
                        subject_id=rec.subject_id.id
                        subject_object = self.env['subject.subject'].search([('id', '=', rec.subject_id.id)])
                        for sub in subject_object:
                            if(current_time-start_time<=0.15):
                                status="Retard"
                            else:
                                status ="Absent"
                self.env['student.desciplines'].create({'subject_id':subject_id, 'device_datetime': last_date, 'status': status, 'student_id': student_id })

