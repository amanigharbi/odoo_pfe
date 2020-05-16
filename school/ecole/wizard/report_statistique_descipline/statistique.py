from odoo import models, fields, api
from datetime import datetime




class statistique_eleve(models.TransientModel):
    _name = 'statistique.eleve'
    _description = "statistique eleve"
    classe_id = fields.Many2many('ecole.classe','classe_stat_rel','classe_id','stat_id','Classe')
    #academic_year = fields.Many2one('academic.year', 'academic_year.nom')
    date_id=fields.Selection([('Jour', 'Jour'),
                                 ('Semaine', 'Semaine'),
                                 ('Mois', 'Mois'),
                                 ('Annee', 'Annee'),
                                 ]
                             )

    @api.multi
    def print_report(self):
       data = {
           'ids': self.ids,
           'model': self._name,
           'form': self.read()[0]

       }
       return self.env.ref('ecole.report_statistique').report_action(self, data=data)

    class ReportStatistique(models.AbstractModel):

        _name = 'report.ecole.report_stat_descipline'

        def nbjoursmois(self, m, a):
            """Donne le nombre de jours du mois m de l'année a"""
            nj = (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)[m]
            if m == 2 and ((a % 4 == 0 and a % 100 != 0) or a % 400 == 0):  # m=février et a=bissextile?
                return nj + 1
            return nj

        def get_nombreDate(self, date):

            # print('date time',datetime.datetime.now().strptime('%Y-%m-%d'))
            print('date', datetime.now().year)
            mois = datetime.now().month
            annee = datetime.now().year

            print("resultat ", self.nbjoursmois(mois, annee))
            nb=0
            if date == "Jour":
                nb = nb + 1
            if date == "Semaine":
                nb = nb + 6
            if date == "Mois":
                nb = nb + 24
            if date == "Annee":
                nb = nb + 360
            return nb
        @api.multi
        def get_NombreDesipline(self,id,status):
            count=0
            stat = (self.env['eleve.desciplines'].search_count(
                [('status', '=', status), ('id', '=', id)]) > 0)
            if stat:
                count = count + 1
            return count

        @api.multi
        def get_NombreSanction(self, id, sanction):
            count=0
            sanc = self.env['eleve.sanctions'].search(
                [('sanction', '=', sanction), ('id', '=', id)])
            count = sanc.nombre + count
            return count
        @api.multi
        def calcul_pourcentage(self,nb,total,id):
            nbreeleve = self.env['eleve.eleve'].search_count([('classe_id', '=', id)])
            nb_prescence=nb*nbreeleve
            pourcentage=round(((total /nb_prescence) *100),2)
            return pourcentage


        @api.model
        def _get_report_values(self, docids, data=None):
           # classe_id = data['form']['classe_id'][1]
            classe = data['form'].get('classe_id')
            docs = []
            for a in classe:
                #date from form
                date = data['form']['date_id']
                #appel du methode qui retourne le nombre de date
                nb=self.get_nombreDate(date)

                #donnée de classe selectionnée
                classe = self.env['ecole.classe'].search([('id', '=', a)])

                countAbsent = 0
                countRetard = 0
                countAver=0
                countExclu=0
                for rec in classe:
                    nom = rec.nom
                    id = rec.id
                    #info et nombre d'eleve de classe sélectionnée
                    eleve = self.env['eleve.eleve'].search([('classe_id', '=', id)])

                    for ele in eleve:
                        descipline = ele.descplines_ids
                        sanction =ele.sanctions_ids

                        for rec2 in descipline:
                            countAbsent=self.get_NombreDesipline(rec2.id,'Absent')+countAbsent
                            countRetard = self.get_NombreDesipline(rec2.id,'Retard')+countRetard
                        totalAbsence = countAbsent
                        totalRetard = countRetard


                        pourcentageAbsence = self.calcul_pourcentage(nb,totalAbsence,id)
                        pourcentageRetard = self.calcul_pourcentage(nb,totalRetard,id)




                        for sanc in sanction:
                            countAver=self.get_NombreSanction(sanc.id, 'avertissement')+countAver
                            countExclu=self.get_NombreSanction(sanc.id, 'exclu')+countExclu

                        totalAver = countAver
                        totalExclu= countExclu
                        pourcentageAvert = self.calcul_pourcentage(nb,totalAver,id)
                        pourcentageExclu = self.calcul_pourcentage(nb,totalExclu,id)

                    docs.append({
                        'nom': nom,
                        'pourcentageAbsent': pourcentageAbsence,
                        'pourcentageRetard': pourcentageRetard,
                        'pourcentageAvert': pourcentageAvert,
                        'pourcentageExclu': pourcentageExclu,
                        'par': date })

            return {
                 'doc_ids': data['ids'],
                 'doc_model': data['model'],
                 'docs': docs,
                        }

