from odoo import models,api

class ReportPatient(models.AbstractModel):
    _name = 'hms.report_patient'
    _description = 'Patient Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        patients = self.env['hms.patient'].browse(docids)
        return {
            'docs': patients,
        }