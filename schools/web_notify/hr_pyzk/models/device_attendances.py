from datetime import datetime

from odoo import models, fields, api, exceptions, _


class DeviceAttendances(models.Model):
    _name = "device.attendances"
    _description = "Device Attendances"
    _order = "device_datetime desc"




    device_user_id = fields.Many2one('device.users','Name')
    device_datetime = fields.Datetime(string="Device Datetime")
    device_punch = fields.Selection([(0, 'Check In'), (1, 'Check Out')], string='Device Punch')
    attendance_state = fields.Selection([(0, 'Not Logged'), (1, 'Logged')], string='Status', default = 0)
    device_id = fields.Many2one('devices', 'fingerprint Device')


