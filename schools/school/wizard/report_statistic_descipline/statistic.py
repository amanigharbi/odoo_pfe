from odoo import models, fields, api
from datetime import datetime


class statistic_student(models.TransientModel):
    _name = 'statistic.student'
    _description = "statistic student"

    standard_id = fields.Many2many('school.standard', 'standard_stat_rel', 'standard_id', 'stat_id', 'Class')
    choix = fields.Selection(
        [('Subject', 'Subject'), ('Day', 'Day'), ('Academic Year', 'Academic Year')],'Statistic By :')

    academic_year = fields.Many2one('academic.year', 'academic_year.name')


    date_id = fields.Selection([
        ('Week', 'Week'),
        ('Month', 'Month'),
        ('Year', 'Year'),
    ]
    )

    @api.multi
    def print_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'choix': self.choix,
            'form': self.read()[0]

        }
        return self.env.ref('school.report_statistic').report_action(self, data=data)

    class Reportstatistic(models.AbstractModel):

        _name = 'report.school.report_stat_descipline'

        def nbjoursMonth(self, m, a):
            """Donne le number de jours du Month m de l'année a"""
            nj = (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)[m]
            if m == 2 and ((a % 4 == 0 and a % 100 != 0) or a % 400 == 0):  # m=février et a=bissextile?
                return nj + 1
            return nj

        def get_numberDate(self, date):
            Month = datetime.now().month
            Year = datetime.now().year
            nb = 0
            if date == "Week":
                nb = nb + 6
            if date == "Month":
                nb = nb + 24
            if date == "Year":
                nb = nb + 360
            return nb

        @api.multi
        def get_numberDesipline(self, id, status):
            count = 0
            stat = (self.env['student.desciplines'].search_count(
                [('status', '=', status), ('id', '=', id)]) > 0)
            if stat:
                count = count + 1
            return count

        @api.multi
        def get_numberDailyAbs(self, id):
            count = 0
            stat = (self.env['student.daily.disciplines'].search_count(
                [('id', '=', id)]) > 0)
            if stat:
                count = count + 1
            return count

        @api.multi
        def get_numberSanction(self, id, sanction):
            count = 0
            sanc = self.env['student.sanctions'].search(
                [('sanction', '=', sanction), ('id', '=', id)])
            count = sanc.number + count
            return count

        @api.multi
        def calcul_percentage(self, nb, total, id):
            nbrestudent = self.env['student.student'].search_count([('standard_id', '=', id)])
            nb_prescence = nb * nbrestudent
            percentage = round(((total / nb_prescence) * 100), 2)
            return percentage

        @api.multi
        def calcul_percentage_year(self, nb, total, id):
            nbrestudent = self.env['student.student'].search_count([('year', '=', id)])
            nb_prescence = nb * nbrestudent
            percentage = round(((total / nb_prescence) * 100), 2)
            return percentage

        @api.model
        def _get_report_values(self, docids, data=None):
            #academic_year= data['form']['academic_year'][0]

            docs = []

            docs_day = []
            doc_academic_year = []
            standard = data['form'].get('standard_id')
            academic_year = data['form'].get('academic_year')

            if academic_year:
                nb = 360
                # info of academic year selected
                year = self.env['academic.year'].search([('id', '=', academic_year[0])])
                countAbsentAY = 0
                countlateAY = 0
                countDayAbsAY = 0
                countAverAY = 0
                countExcluAY = 0
                for y in year:
                    name_year = y.name
                    id_year = y.id
                    # info et number of student academic year selected
                    student_AY = self.env['student.student'].search([('year','=',id_year)])
                    for ele in student_AY:
                        desciplineAY = ele.descplines_ids
                        sanctionAY = ele.sanctions_ids
                        daily_absAY = ele.daily_discplines_ids
                        for rec2 in desciplineAY:
                            countAbsentAY = self.get_numberDesipline(rec2.id, 'Absent') + countAbsentAY
                            countlateAY = self.get_numberDesipline(rec2.id, 'Late') + countlateAY

                        totalAbsenceAY = countAbsentAY

                        totallateAY = countlateAY

                        percentageAbsence_y = self.calcul_percentage_year(nb, totalAbsenceAY, id_year)
                        percentagelate_y = self.calcul_percentage_year(nb, totallateAY, id_year)

                        for sanc in sanctionAY:
                            countAverAY = self.get_numberSanction(sanc.id, 'avertissement') + countAverAY
                            countExcluAY = self.get_numberSanction(sanc.id, 'exclu') + countExcluAY

                        totalAverAY = countAverAY
                        totalExcluAY = countExcluAY
                        percentageAvert_y = self.calcul_percentage_year(nb, totalAverAY, id_year)
                        percentageExclu_y = self.calcul_percentage_year(nb, totalExcluAY, id_year)

                        for day_abs in daily_absAY:
                            countDayAbsAY = self.get_numberDailyAbs(day_abs.id) + countDayAbsAY
                        totalDayAbsAY = countDayAbsAY

                        percentageDayAbs_y = self.calcul_percentage_year(nb, totalDayAbsAY, id_year)

                    doc_academic_year.append({
                        'name_year': name_year,
                        'percentageAbsentAY': percentageAbsence_y,
                        'percentageDailyAbsAY': percentageDayAbs_y,
                        'percentagelateAY': percentagelate_y,
                        'percentageAvertAY': percentageAvert_y,
                        'percentageExcluAY': percentageExclu_y,
                        'percentageDailyAbsAY': percentageDayAbs_y})
            if standard:
                for a in standard:
                    # date from form
                    date = data['form']['date_id']
                    # call of function which return le number of date
                    nb = self.get_numberDate(date)

                    # info of standard selected
                    standard = self.env['school.standard'].search([('id', '=', a)])
                    #count_standard =self.env['school.standard'].search_count([('id', '=', a)])



                    countAbsent = 0
                    countlate = 0
                    countDayAbs = 0
                    countAver = 0
                    countExclu = 0

                    for rec in standard:
                        name = rec.name
                        id = rec.id
                        # info et number of student standard selected
                        student = self.env['student.student'].search([('standard_id', '=', id)])

                        for ele in student:
                            descipline = ele.descplines_ids
                            sanction = ele.sanctions_ids
                            daily_abs = ele.daily_discplines_ids

                            for rec2 in descipline:
                                countAbsent = self.get_numberDesipline(rec2.id, 'Absent') + countAbsent
                                countlate = self.get_numberDesipline(rec2.id, 'Late') + countlate

                            totalAbsence = countAbsent
                            totallate = countlate

                            percentageAbsence = self.calcul_percentage(nb, totalAbsence, id)

                            percentagelate = self.calcul_percentage(nb, totallate, id)

                            for sanc in sanction:
                                countAver = self.get_numberSanction(sanc.id, 'avertissement') + countAver
                                countExclu = self.get_numberSanction(sanc.id, 'exclu') + countExclu

                            totalAver = countAver
                            totalExclu = countExclu
                            percentageAvert = self.calcul_percentage(nb, totalAver, id)

                            percentageExclu = self.calcul_percentage(nb, totalExclu, id)



                            for day_abs in daily_abs:
                                countDayAbs = self.get_numberDailyAbs(day_abs.id) + countDayAbs
                            totalDayAbs = countDayAbs

                            percentageDayAbs = self.calcul_percentage(nb, totalDayAbs, id)



                        docs.append({
                            'name': name,
                            'percentageAbsent': percentageAbsence,
                            'percentagelate': percentagelate,
                            'percentageAvert': percentageAvert,
                            'percentageExclu': percentageExclu,
                            'by': date
                            #'count_standard':count_standard
                             })
                        docs_day.append({
                            'name': name,
                            'percentageDailyAbs': percentageDayAbs,
                            'by': date})

            return {
                'doc_ids': data['ids'],
                'doc_model': data['model'],
                'docs': docs,
                'docs_day': docs_day,
                'doc_academic_year':doc_academic_year,

            }
