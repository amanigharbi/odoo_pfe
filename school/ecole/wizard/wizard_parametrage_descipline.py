from odoo import models, fields, api



class parametrage_descipline(models.TransientModel):
    _name = 'parametrage.descipline'
    _description = "parametrage descipline"

    nombre_avertissement=fields.Integer('Nombre des absences pour avoir un avertissement :')
    nombre_exclu=fields.Integer('Nombre avertissement pour avoir un exclu :')

    max_retard=fields.Float("Maximum retard pour un élève")

    def enregistrer_parametrage(self):
        if self.env['parametrage.descipline'].search_count([]) > 0:
            search = self.env['parametrage.descipline'].search([])

            data = {
                'ids': self.ids,

                'model': self._name,
                'form': self.read()[0]
                }
            #print('data',data['form'])
            nouveau_nb_avert=data['form']['nombre_avertissement']
            nouveau_nb_exclu=data['form']['nombre_exclu']
            nouveau_max_retard=data['form']['max_retard']
            print('n',nouveau_nb_avert)
            for a in search:
                a.unlink()
            #search.nombre_avertissemets=nouveau_nb_avert
            #search.nombre_exclus=nouveau_nb_exclu
            #search.max_retard=nouveau_max_retard


        self.env['parametrage.descipline'].create({'nombre_avertissement':nouveau_nb_avert,
                    'nombre_exclu': nouveau_nb_exclu,
                    'max_retard':nouveau_max_retard                                   })


            #vals={'nombre_avertissemets':nouveau_nb_avert,
                          #'nombre_exclus':nouveau_nb_exclu,
                           #'max_retard':nouveau_max_retard}

            #print ('valeur', vals)
            #search.update(vals)
            #print('update', search.update(vals))
               # nb_avert.update(nouveau_nb_avert)
                #nb_exclu.update(nouveau_nb_exclu)
                #m_retard.update(nouveau_max_retard)
                    #print("hi",a.update(vals))
        #return True