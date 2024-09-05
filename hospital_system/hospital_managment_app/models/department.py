from odoo import models, fields, api

class Department(models.Model):
    _name = 'hms.department'

    name = fields.Char()
    capacity = fields.Integer()
    is_opened = fields.Boolean()
    patients = fields.Char()

    patient_ids = fields.One2many('hms.patient','department_id',string='Patients')