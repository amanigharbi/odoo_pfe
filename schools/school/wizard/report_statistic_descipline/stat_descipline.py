from odoo import api, models, _


class StatDescipline(models.AbstractModel):
    _name = 'report.school.report_stat_descipline'
    _description = 'Statistic descipline'
    @api.model
    def _get_report_values(self, docids, data=None):
        if data['form']['standard_id']:
            appointments = self.env['school.standard'].search([('id', '=', data['form']['standard_id'][0])])

            print('appointments ',appointments)
        else:
            appointments = self.env['school.standard'].search([])
            print('appointments2 ', appointments)
            appointment_list = []
            for app in appointments:
                 vals = {
                     'name': app.name,
                     #'notes': app.notes,
                     #'appointment_date': app.appointment_date
                 }
                 appointment_list.append(vals)
            print('appointment_list ', appointment_list)
        return {
            'doc_model': 'school.standard',
            'appointments': appointments,
        }