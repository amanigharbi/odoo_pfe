# -*- coding: utf-8 -*-
##############################################################################

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
    def test_search_attendance(self,times,attendances):
        all_attendances = []
        all_attendances.clear()
        all_clocks = []
        all_clocks.clear()
        device_user_object = self.env['device.users']
        device_users = device_user_object.search([])
        attendance_object = self.env['device.attendances']
        all_attendances = [[y.id, x[1].astimezone(pytz.utc), x[2], x[3]]
                           for x in attendances for y in device_users if
                           int(x[0]) == y.device_user_id]

        all_clocks.extend(all_attendances)

        for cl in all_clocks:
            attendance_object.create({
                'device_user_id': cl[0],
                'device_datetime': times,
                'device_punch': cl[2],
                'attendance_state': 0,
                'device_id': cl[3],
            })
    def test_attendance_odoo(self,a,time_attendance_device):
        all_attendances = []
        all_attendances.clear()
        all_clocks = []
        all_clocks.clear()
        device_user_object = self.env['device.users']
        device_users = device_user_object.search([])
        attendance_object = self.env['device.attendances']



        all_attendances = [[y.id, a[1].astimezone(pytz.utc), a[2], a[3]]
                           for y in device_users if
                           int(a[0]) == y.device_user_id]

        all_clocks.extend((all_attendances))
        print("nooo", all_clocks)

        for all in all_clocks:
            attendance_object.create({
                'device_user_id': int(all[0]),
                'device_datetime': time_attendance_device,
                'device_punch': all[2],
                'attendance_state': 0,
                'device_id': all[3],
            })
    def get_time(self,a):
        time_attendance_device = a[1] + datetime.timedelta(hours=-1)
        return time_attendance_device
    def import_attendance(self): # Import Attendance Wizard
        attendance_object = self.env['device.attendances']
        devices_object = self.env['devices']
        devices = devices_object.search([('state', '=', 0)])

        for device in devices:
            attendances = c.DeviceUsers.get_attendance(device)

            for a in attendances:
                attendance_odoo_search = attendance_object.search([])
                #methode pour obtenir l'heure
                times = self.get_time(a)

                attendance_odoo = attendance_object.search_count([
                    ('device_id', '=', device.id),('device_user_id.device_user_id', '=', a[0]),
                    ('device_datetime', '=', times)])

                #s'il n'existe pas un attendance comme celui çi dans la pointage ,il va l'ajouter
                if attendance_odoo == 0:
                    self.test_attendance_odoo(a,times)

                elif not attendance_odoo_search:
                    # chercher s'il n'y a aucune attendance dans device_attendance
                    self.test_search_attendance(times, attendances)






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



