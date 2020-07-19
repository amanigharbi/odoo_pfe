from odoo import models, fields, api, exceptions, _
from addons.hr_pyzk.controllers import controller as c
from zk import ZK, const

class DeviceUser(models.Model):
    _name = 'device.users'
    _description = 'device user information'
    _order = "device_user_id"

    device_user_id = fields.Integer('Device User ID')
    device_uid = fields.Integer('Device UID') # uid in the device. Important to delete user in the future
    name = fields.Char('Device User Name')
    last_name = fields.Char('Device User Last Name')
    classe = fields.Char('Device User Class')
    device_id = fields.Many2one('devices', 'Fingerprint Device')
    fingers=fields.Integer('Finger',default=0)

    _sql_constraints = [
        ('device_user_id_uniq', 'unique (device_user_id)',
         'It is not possible to create more than one user '
         'with the same device_user_id'),
    ]
#crete user into device
    @api.multi
    def create_user(self, device):
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


    #method to chek if student has finger (return number fingerprint)
    @api.multi
    def get_numberFinger(self, uid):
        count = 0
        ip_address = self.device_id.ip_address
        port = self.device_id.port
        device_password = self.device_id.device_password
        with c.ConnectToDevice(ip_address, port, device_password) as conn:
            template = conn.get_templates()
            if template:
                for t in template:
                    id = t.uid
                    if id == uid:
                        count = count + 1

        return count
    @api.multi
    def check_nb_fingerprint(self, device):
        """
                              Function uses to get number of fingerprint of each user
                """
        ip_address = self.device_id.ip_address
        port = self.device_id.port
        device_password = self.device_id.device_password

        if self.device_id.id is False:
            raise exceptions.Warning("Fingerprint device is not selected")
        with c.ConnectToDevice(ip_address, port, device_password) as conn:

            uid=self.device_user_id
            var_finger=self.get_numberFinger(uid)
            self.fingers = var_finger
            try:
                conn.set_user(uid=self.device_user_id, name=self.name,privilege=const.USER_DEFAULT,
                              user_id=str(self.device_user_id))


            except Exception as e:
                raise exceptions.Warning("User does not exist in the device")







