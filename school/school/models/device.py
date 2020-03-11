# See LICENSE file for full copyright and licensing details.

import time
import base64

from odoo import models, fields, api, tools, _


class DeviceUser(models.Model):
    ''' Defining a student information '''
    _name = 'device.device'
    _table = "device_users"
    _description = 'Device Information'


    @api.model
    def create(self, vals):
        res = super(DeviceUser, self).create(vals)
        return res

