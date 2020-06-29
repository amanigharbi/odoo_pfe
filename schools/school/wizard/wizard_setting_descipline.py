from odoo import models, fields, api



class parametrage_descipline(models.TransientModel):
    _name = 'settings.descipline'
    _description = "settings descipline"

    status_discipline=fields.Selection([('Absent','Absent'),('Late','Late')],'Choice Discipline')
    number_avertissement=fields.Integer('Number of discipline choiced to get avertissement :')
    number_exclu=fields.Integer('Number of avertissement to get exclu :')

    max_late=fields.Float("Maximum late for a student")


    def save_settings(self):
        if self.env['settings.descipline'].search_count([]) > 0:
            search = self.env['settings.descipline'].search([])

            data = {
                'ids': self.ids,
                'model': self._name,
                'form': self.read()[0]
                }

            new_nb_avert=data['form']['number_avertissement']
            new_nb_exclu=data['form']['number_exclu']
            new_max_late=data['form']['max_late']
            new_status_discipline = data['form']['status_discipline']

            for a in search:
                a.unlink()
            self.env['settings.descipline'].create({'number_avertissement':new_nb_avert,
                    'number_exclu': new_nb_exclu,
                    'max_late':new_max_late,'status_discipline':new_status_discipline,
                     })


