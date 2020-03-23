from odoo import models, fields, api
from addons.hr_pyzk.models import device_users
from zk import ZK, const


class add_users(models.TransientModel):
    _name = 'add.users'
    _description = "add users"
    _order = "device_user_id"


    device_user_id = fields.Integer('Device User ID')
    # device_user_id = fields.Many2one('devices.users','device_users.device_user_id')
    device_uid = fields.Integer('Device UID') # uid in the device. Important to delete user in the future
    name = fields.Char('Device User Name')
    # name = fields.Many2one('devices.users', 'device_users.name')
    employee_id = fields.Many2one('hr.employee', 'Related employee')
    device_id = fields.Many2one('devices', 'devices.id')

    @api.multi
    def button_add(self, device):
        deivces = self.env['device.users'].search([])
        print(deivces)
        for rec in deivces:
            device_users.DeviceUser.create_user(rec,rec)