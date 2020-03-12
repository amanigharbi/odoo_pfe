from odoo import models, fields, api
from addons.hr_pyzk.controllers import controller as c
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
        """
                Function uses to get attendances
                """
        ip_address = self.device_id.ip_address
        port = self.device_id.port
        device_password = self.device_id.device_password
        user_id = str(self.device_user_id)

        with c.ConnectToDevice(ip_address, port, device_password) as conn:

            device_users = conn.get_users()
            device_user_ids = [int(x.user_id) for x in device_users]
            if self.device_user_id not in device_user_ids:
                conn.set_user(uid=self.device_user_id, name=self.name, privilege=const.USER_DEFAULT, user_id=user_id)
                self.device_uid = self.device_user_id
                return {
                    "type": "ir.actions.act_window",
                    "res_model": "device.users",
                    "views": [[False, "form"]],
                    "res_id": self.id,
                    "target": "main",
                    "context": {'show_message1': True},
                }

            else:
                return {
                    "type": "ir.actions.act_window",
                    "res_model": "device.users",
                    "views": [[False, "form"]],
                    "res_id": self.id,
                    "target": "main",
                    "context": {'show_message2': True},
                }