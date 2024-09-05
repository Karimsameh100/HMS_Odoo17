from pkg_resources import require

from odoo import fields, models,api
from odoo.exceptions import ValidationError


class Patient(models.Model):
    _name = "hms.patient"

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    birth_date = fields.Date()
    history = fields.Html(string="History")
    cr_ratio = fields.Float()
    blood_type = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
    ])
    pcr = fields.Boolean(string="PCR")
    image = fields.Binary()
    address = fields.Text()
    age = fields.Integer(compute='_compute_age', store=True)
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], default='undetermined')

    department_id = fields.Many2one('hms.department', string='Department', domain="[('is_opened', '=', True)]")
    doctor_id = fields.Many2one('hms.doctor', string='Doctor')
    department_capacity = fields.Integer(related='department_id.capacity', string='Department Capacity')
    history_ids = fields.One2many('hms.patient.history', 'patient_id')

    @api.multi
    def print_report(self):
        return self.env.ref('hms.report_patient').report_action(self)


    @api.depends('birth_date')
    def _compute_age(self):
        for patient in self:
            if patient.birth_date:
                age = (fields.Date.today() - patient.birth_date).days // 365
                patient.age = age

    @api.depends('pcr')
    def _compute_cr_ratio_required(self):
        for record in self:
            if record.pcr:
                record.cr_ratio_required = True
            else:
                record.cr_ratio_required = False

    cr_ratio_required = fields.Boolean(compute='_compute_cr_ratio_required', store=True)

    @api.onchange('pcr')
    def _onchange_pcr(self):
        if self.pcr:
            if not self.cr_ratio:
                raise ValidationError("CR ratio is required when PCR is checked")

    @api.onchange('birth_date')
    def _onchange_birth_date(self):
        if self.birth_date:
            age = (fields.Date.today() - self.birth_date).days // 365
            if age < 30:
                self.pcr = True
                history_record = self.env['hms.patient.history'].sudo().create({
                    'patient_id': self.id,
                    'description': 'PCR automatically checked due to age less than 30',
                })
                # Return the newly created recordset
                return {'value': {'pcr': True, 'history': [(6, 0, [history_record.id])]}}
            if age < 50:
                self.history = False
                return {'value': {'history': False}}

    @api.constrains('department_id')
    def _check_department_is_opened(self):
        for patient in self:
            if patient.department_id and not patient.department_id.is_opened:
                raise ValidationError("Cannot assign patient to a closed department")

class PatientHistory(models.Model):
    _name = "hms.patient.history"
    _description = "History"

    created_by=fields.Char(string="Created by")
    data=fields.Date(string="Date")
    description=fields.Text(string="Description")

    patient_id=fields.Many2one('hms.patient')


