from odoo import http

class ReportController(http.Controller):
    @http.route('/web/report/hms.patient/<int:patient_id>', type='http', auth='user')
    def print_report(self, patient_id):
        report = self.env.ref('hms.report_patient')
        return report.render_qweb_pdf([patient_id])