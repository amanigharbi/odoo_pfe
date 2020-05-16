from odoo import models, fields, api
from addons.hr_pyzk.models import device_users
from odoo.exceptions import except_orm
import datetime


class add_eleve(models.TransientModel):
    _name = 'add.eleve'
    _description = "add eleve"
    _inherit = 'device.users'
    nom_eleve = fields.Many2many('eleve.eleve','add_eleve_eleve_eleve_rel','add_eleve_id','eleve_eleve_id','Nom Elève')
    device_name = fields.Many2one('devices', 'Nom Machine')
    device_id = fields.Many2one('devices', 'devices.id')
    #  self._cr.execute("INSERT INTO eleve_eleve(user_id,pid,middle,last,date_de_naissance) values (100,100,'100','100','12/12/2000')")
    @api.multi
    def button_add(self, vals):
        # eleve =self.env['eleve.eleve'].search([('classe_id','=','')])
        if self.nom_eleve and self.device_name:

            for eleve in self.nom_eleve:
                for deivce in self.device_name:
                    self.env['device.users'].create({'name':eleve.nom,'device_user_id':eleve.id,'device_id':deivce.id})
                    deivces = self.env['device.users'].search([('device_user_id','=',eleve.id)])
                    for rec in deivces:
                        device_users.DeviceUser.create_user(rec,rec)
        else :
            raise except_orm(('Warning'),('''Séléctionnez elève/machine SVP!!!'''))

# action planifié du pointage d'élève
    def test_Pointage_Eleve(self):
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
                    courant_time = last_date.strftime("%H.%M")
                    courant_time = float(courant_time) + 1.0
                    student_object = self.env['eleve.eleve'].search([('nom_eleve', '=', x.device_user_id.nom)])
                    classe = student_object.classe_id
                    nom = student_object.nom_eleve
                    parent_object = self.env['ecole.parent'].search([('eleve_id', '=', student_id)])
                    parent = parent_object.id
                    print('parent ',parent)
                    emploie_object = self.env['emploie.emploie'].search([('classe_id', '=', classe.id)])
                    emploie = emploie_object.id
                    emploie_objet_ligne = self.env['emploie.emploie.details'].search(
                        [('table_id', '=', emploie) and ('jour_semaine', '=', local_day)])

                    heure_debut = 0
                    matiere_id = 0
                    nombreRetard = 0
                    matiere_nom=''


                    for rec in emploie_objet_ligne:
                        if (courant_time >= rec.heure_debut and courant_time - rec.heure_debut <= 1 and courant_time - rec.heure_debut >= 0):
                            heure_debut = rec.heure_debut
                            matiere_id = rec.matiere_id.id
                            matiere_nom=rec.matiere_id.nom
                        #else:
                            #message = ('Aucune Matière dans ce temps! ')
                            #self.env.user.notify_danger(message)
                            #break
                    search = self.env['parametrage.descipline'].search([])
                    retard = search.max_retard
                    parametrage_nb_avertissement = search.nombre_avertissement
                    parametrage_nb_exclu = search.nombre_exclu

                    print('retard', retard)
                    if (courant_time - heure_debut <= retard):
                        status = "Retard"
                        message = ('Elève ', nom, ' est Retard! ')
                        self.env.user.notify_info(message)
                        nombreRetard = nombreRetard + 1
                        print(nombreRetard)

                        message_notif=('Votre Enfant Est Retard De '+str(retard)+' Dans La Matière '+matiere_nom+' Prévu à '+str(heure_debut))
                        print("notif: ",message_notif)
                    else:
                        status = "Absent"
                        message = ('Elève ', nom, ' est Absent! ')
                        self.env.user.notify_info(message)
                        message_notif=('Votre Enfant Est Absent Dans La Matière '+matiere_nom+' Prévu à '+str(heure_debut))
                        print("notif: ", message_notif)
                    self.env['eleve.desciplines'].create(
                        {'matiere_id': matiere_id, 'device_datetime': last_date, 'status': status,
                         'eleve_id': student_id})

                    self.env['historique.notification'].create(
                        {'eleve_id': student_id, 'title': status, 'message': message_notif, 'etat_message': True,'parent_id':parent})



                    var = self.env['eleve.desciplines'].search_count(
                        [('status', '=', 'Retard'), ('eleve_id.id', '=', student_id)])
                    search = self.env['eleve.sanctions'].search(
                        [('sanction', '=', 'avertissement') and ('eleve_id.id', '=', student_id)])
                    print('var: ', var)
                    var2 = self.env['eleve.sanctions'].search(
                        [('sanction', '=', 'exclu') and ('eleve_id.id', '=', student_id)])

                    for v in search:
                        v.unlink()
                    nombreAver = int(var / parametrage_nb_avertissement)
                    print('nombre aver: ', nombreAver)

                    sanction = "avertissement"

                    self.env['eleve.sanctions'].create(
                        {'sanction': sanction, 'nombre': nombreAver, 'eleve_id': student_id})

                    for v2 in var2:
                        v2.unlink()

                    nombreExclu = int(nombreAver / parametrage_nb_exclu)
                    sanction = "exclu"

                    self.env['eleve.sanctions'].create(
                        {'sanction': sanction, 'nombre': nombreExclu, 'eleve_id': student_id})

                # res = "Succes"
                #self.env.user.notify_success(message='Traitement Descipline Terminé!')
                #print(res)
                break
        else:
            self.env.user.notify_info(message='Aucun(e) Elève Pointé')
            res = "Aucun(e) Elève Pointé"
            print(res)






