

from odoo import models, fields, api
from addons.hr_pyzk.models import device_users
from odoo.exceptions import except_orm
import datetime
import os
import functools
import operator
from schools.school.models.parent import history_notification

class school_attendance_device(models.TransientModel):
    _name = 'school.attendance.device'
    _description = "School Attendance"
    _inherit = 'device.users'
    student_name = fields.Many2many('student.student', 'school_attendance_device_student_rel', 'school_attendance_device_id',
                                    'student_student_id', 'Name student')
    device_name = fields.Many2one('devices', 'Device Name')
    device_id = fields.Many2one('devices', 'devices.id')

    @api.multi
    def ticket(self, name, last, status, classe, time,date, subject):
        f = open("billet", "w")

        name = functools.reduce(operator.add, ("          ", name, " ", last, "\n"))
        # status = functools.reduce(operator.add, ("  Status: ", status, "\n"))
        classe = functools.reduce(operator.add, ("  Class: ", classe, "\n"))
        subject = functools.reduce(operator.add, ("  Subject: ", subject, "\n"))
        datetime = functools.reduce(operator.add, ("  DateTime  : ", date," ",time, "\n"))

        f.write("___________________________________\n")
        f.write("          Ticket " + status + "          \n\n")
        f.write(name + "          \n")
        f.write(classe)
        f.write(datetime)
        f.write(subject)
        f.write("___________________________________")
        #f.close()

        os.system('lpr billet')


        

    @api.multi
    def button_add(self, vals):
        # student =self.env['student.student'].search([('standard_id','=','')])
        if self.student_name and self.device_name:

            for student in self.student_name:
                for deivce in self.device_name:
                    self.env['device.users'].create(
                        {'name': student.name, 'device_user_id': student.id, 'device_id': deivce.id})
                    deivces = self.env['device.users'].search([('device_user_id', '=', student.id)])
                    for rec in deivces:
                        device_users.DeviceUser.create_user(rec, rec)
        else:
            raise except_orm(('Warning'), ('''Select student/device please!!!'''))

    # action planifié du pointage d'élève
    def test_attendance_student(self):
        # le jour d'aujourd'hui
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

                    # for x in device_attendances:
                    student_id = x.device_user_id.device_user_id

                    last_date = datetime.datetime.strptime(str(x.device_datetime), '%Y-%m-%d %H:%M:%S')
                    current_time = last_date.strftime("%H.%M")
                    current_t = float(current_time) + 1.0
                    current_time=round((current_t),2)
                    current_date=last_date.strftime("%Y-%m-%d")

                    # les informations d'élève ou son id est le meme du table device_attendance
                    student_object = self.env['student.student'].search([('id', '=', student_id)])

                    standard = student_object.standard_id.id
                    standard_name = student_object.standard_id.name
                    school = student_object.school_id.id
                    name = student_object.student_name
                    last = student_object.last
                    # les informations relatives au parent de l'élève pointé
                    parent_object = self.env['school.parent'].search([('student_id', '=', student_id)])
                    parent = parent_object.id
                    name_parent=parent_object.name
                    reg_object = self.env['parent.registration'].search([('parent_id', '=', parent)])



                    # l'emploie du temps relative au classe et école de l'élève pointé
                    timetable_object = self.env['time.table'].search(
                        [('school_id', '=', school), ('standard_id', '=', standard)])
                    timetable = timetable_object.id

                    # extraire les informations nécessaires relatives au l'emploie du temps et le jour du pointage
                    timetable_objet_line = self.env['time.table.line'].search(
                        [('table_id', '=', timetable), ('week_day', '=', local_day)])

                    # initialiser les variables
                    start_time = 0
                    subject_id = 0
                    numberlate = 0
                    subject_name = ''
                    late_mn = 0

                    for rec in timetable_objet_line:
                        # if (current_time >= rec.start_time and current_time - rec.start_time <= 1 and current_time - rec.start_time >= 0):

                        # les informations de l'emploie nécessaires
                        start_time = rec.start_time
                        subject_id = rec.subject_id.id
                        subject_name = rec.subject_id.name

                    # extraire les attributs du table settings.descipline
                    search = self.env['settings.descipline'].search([])
                    late = search.max_late

                    settings_nb_avertissement = search.number_avertissement
                    settings_nb_exclu = search.number_exclu
                    settings_discipline_selected=search.status_discipline


                        # tester si l'élève pointé est retard
                    if (current_time - start_time <= late):
                        status = "Late"
                        # le retard de l'élève
                        late_mn = round((current_time - start_time), 2)
                        # impression de billet
                        self.ticket(name, last, status, standard_name, str(current_time), str(current_date),
                                    subject_name)

                        # notification pour l'admin
                        message = (
                                'A Student Is Pointed: \n' + name + ' Is Late In ' + subject_name + ' With ' + str(
                            late_mn) + 'Minutes !')
                        self.env.user.notify_info(message)
                        numberlate = numberlate + 1

                        # notification pour le parent
                        message_notif = ('Votre Enfant ' + name + ' Est Retard DE : ' + str(
                            late_mn) + 'Min, Dans La Matière ' + subject_name + ' Prévu à ' + str(start_time))
                    else:
                        status = "Absent"

                        # notification pour l'admin
                        message = ('A Student Is Pointed: \n' + name + ' is Absent In ' + subject_name + '!')

                        self.env.user.notify_info(message)

                        # notification pour le parent
                        message_notif = (
                                'Votre Enfant ' + name + ' Est Absent(e) Dans La Matière ' + subject_name + ' Prévu à ' + str(
                            start_time))

                    # création de la discipline de l'élève necessaire
                    self.env['student.desciplines'].create(
                        {'subject_id': subject_id, 'device_datetime': last_date, 'status': status,
                         'student_id': student_id})

                                        # création de la notification pour le parent avec le discipline nécessaire
                    self.env['history.notification'].create(
                        {'student_id': student_id, 'title': status, 'message': message_notif,
                         'status_message': 'In Progress', 'parent_id': parent})
                    titre = (name + " Est : " + status)
                    if reg_object:
                        for reg in reg_object:
                            reg_id = reg.reg_id
                            history_notification.get_notif(titre, message_notif, reg_id)
                    else:
                        message = ('Demandez au parent '+name_parent+' d '+' installer l '+' application pour recevoir ses notifications !')
                        self.env.user.notify_danger(message)


                    # conter le nombre totales des retard
                    nombreTotaleRetard = self.env['student.desciplines'].search_count(
                        [('status', '=', 'Late'), ('student_id.id', '=', student_id)])

                    # conter le nombre totales des abcences
                    nombreTotaleAbsence = self.env['student.desciplines'].search_count(
                        [('status', '=', 'Absent'), ('student_id.id', '=', student_id)])

                    # extraire le nombre des avertissements
                    nombreTotaleAvert = self.env['student.sanctions'].search(
                        [('sanction', '=', 'avertissement') and ('student_id.id', '=', student_id)])

                    # extraire le nombre des exclus
                    nombreTotaleExclu = self.env['student.sanctions'].search(
                        [('sanction', '=', 'exclu') and ('student_id.id', '=', student_id)])

                    for nbAvert in nombreTotaleAvert:
                        # supprimer la ligne du table

                        nbAvert.unlink()
                    if settings_discipline_selected=="Late":
                        # calculer le nombre des avertissements totales
                        numberAver = int(nombreTotaleRetard / settings_nb_avertissement)

                    else:
                        numberAver = int(nombreTotaleAbsence / settings_nb_avertissement)

                    sanction = "avertissement"

                    # creer la ligne avertissement dans la table
                    self.env['student.sanctions'].create(
                        {'sanction': sanction, 'number': numberAver, 'student_id': student_id})

                    for nb in nombreTotaleExclu:
                        # supprimer la ligne de la table
                        nb.unlink()


                    # calculer le nombre totale des avertissements
                    numberExclu = int(numberAver / settings_nb_exclu)
                    sanction = "exclu"

                    # creer la ligne exclu dans la table
                    self.env['student.sanctions'].create(
                        {'sanction': sanction, 'number': numberExclu, 'student_id': student_id})
                break
        else:
            # notification pour l'admin
            self.env.user.notify_info(message='None Pointed Student')



    def count_discipline_absent(self, id, date_actuelle):
        count = 0

        discipline_student = self.env['student.desciplines'].search([
            ('student_id', '=', id)])
        for c in discipline_student:
            device = c.device_datetime
            date = device.strftime("%Y-%m-%d")

            if date_actuelle == date:
                count = count + 1
        return count

    # action planifié d'absence des élèves
    def attendance_student_daily(self):

        # le jour d'aujourd'hui
        date_actuelle = datetime.date.today().strftime("%Y-%m-%d")
        student_object = self.env['student.student'].search([])
        for i in student_object:
            id = i.id
            name = i.student_name

            if self.count_discipline_absent(id, date_actuelle) == 0:
                self.env['absence.daily'].create(
                    {'date': date_actuelle, 'status': 'Absent For Day',
                     'student_id': id})

                # les informations relatives au parent de l'élève
                parent_object = self.env['school.parent'].search([('student_id', '=', id)])
                parent = parent_object.id
                # création de la notification pour le parent avec l'absence nécessaire
                message_notif = ('Votre Enfant ' + name + ' Est Absent(e) Le ' + date_actuelle)
                self.env['history.notification'].create(
                    {'student_id': id, 'title': "Absence D'Une Journée", 'message': message_notif,
                     'status_message': 'In Progress', 'parent_id': parent})

