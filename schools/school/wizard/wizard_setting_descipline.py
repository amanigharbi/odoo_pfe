from odoo import models, fields, api



class parametrage_descipline(models.TransientModel):
    _name = 'settings.descipline'
    _description = "settings descipline"

    number_avertissement=fields.Integer('Number of lates to get avertissement :')
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

            print('n',new_nb_avert)
            for a in search:
                a.unlink()



        self.env['settings.descipline'].create({'number_avertissement':new_nb_avert,
                    'number_exclu': new_nb_exclu,
                    'max_late':new_max_late,
                     })


