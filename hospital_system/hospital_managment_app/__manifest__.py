{
    'name': 'Hospital System',
    'summary': 'HMS is an hospital managment system',
    'description': 'this system manage patient doctos and department',
    'author': 'Karim Sameh',
    'category': 'Productivity',
    'version': '17.0.0.1.0',
    'depends': [
        'base'
    ],
    'application': True,

    "data":[
        "security/ir.model.access.csv",
        'views/base_menus.xml',
        'views/patient_view.xml',
        'views/doctor_view.xml',
        'views/department_view.xml',
        'report/report_patient.xml'
    ]
}