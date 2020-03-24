from odoo import models, fields, api
from addons.hr_pyzk.models import device_users


class add_eleve(models.TransientModel):
    _name = 'add.eleve'
    _description = "add eleve"
    _inherit = 'device.users'
    eleve_name = fields.Many2many('eleve.eleve','add_eleve_eleve_eleve_rel','add_eleve_id','eleve_eleve_id','eleve_name')
    device_name = fields.Many2one('devices', 'device name')
    device_id = fields.Many2one('devices', 'devices.id')
    #  self._cr.execute("INSERT INTO eleve_eleve(user_id,pid,middle,last,date_of_birth) values (100,100,'100','100','12/12/2000')")
    @api.multi
    def button_add(self, vals):
        # eleve =self.env['eleve.eleve'].search([('standard_id','=','')])
        if self.eleve_name and self.device_name:

            for eleve in self.eleve_name:
                for deivce in self.device_name:
                    self.env['device.users'].create({'name':eleve.name,'device_user_id':eleve.id,'device_id':deivce.id})
                    deivces = self.env['device.users'].search([('device_user_id','=',eleve.id)])
                    for rec in deivces:
                        device_users.cc.create_user(rec,rec)
        else :
            print("")
            #TODO ADD message  error


