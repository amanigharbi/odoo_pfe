# See LICENSE file for full copyright and licensing details.

{
    'name': 'Ecole',
    'version': '12.0.1.0.0',
    'author': 'Ameni & Soumaya',
    'summary':'Ce module a été ecrit durant la période du notre projet fin Etudes',
    'category': 'Ecole',
    'license': "AGPL-3",
    'complexity': 'easy',
    'Summary': 'module pour gestion ecole',
    'depends': ['hr', 'crm', 'account'],
    'data': ['security/ecole_security.xml',
             'security/ir.model.access.csv',
             'wizard/mettre_fin_raison_view.xml',
             'wizard/wiz_send_email_view.xml',
             'views/eleve_view.xml',
             'views/ecole_view.xml',
             'views/enseignant_view.xml',
             'views/parent_view.xml',
             #'views/historique_notification_view.xml',


             'wizard/move_standards_view.xml',

             'wizard/statistic_view.xml',
             'views/rapport_view.xml',
             'views/carte_identite.xml',
             'views/template_view.xml',
             'views/emploie_view.xml',
             'views/emploie.xml',

             'wizard/report_statistique_descipline/statistic_view.xml',
             'wizard/report_statistique_descipline/stat_descipline.xml',
             'wizard/report_statistique_descipline/report_stat.xml',

             'data/TestPointageElève.xml'
             ],
    'installable': True,
    'application': True
}
