from odoo import api, models, _


class StatDescipline(models.AbstractModel):
    _name = 'report.ecole.report_stat_descipline'
    _description = 'Statistique descipline'
    @api.model
    def _get_report_values(self, docids, data=None):
        if data['form']['classe_id']:
            appointments = self.env['ecole.classe'].search([('id', '=', data['form']['classe_id'][0])])

            print('appointments ',appointments)
        else:
            appointments = self.env['ecole.classe'].search([])
            print('appointments2 ', appointments)
            appointment_list = []
            for app in appointments:
                 vals = {
                     'nom': app.nom,
                     #'notes': app.notes,
                     #'appointment_date': app.appointment_date
                 }
                 appointment_list.append(vals)
            print('appointment_list ', appointment_list)
        return {
            'doc_model': 'ecole.classe',
            'appointments': appointments,
        }