# See LICENSE file for full copyright and licensing details.

from odoo.tests import common
import time


class TestEcole(common.TransactionCase):

    def setUp(self):
        super(TestEcole, self).setUp()
        self.eleve_eleve_obj = self.env['eleve.eleve']
        self.enseignant_obj = self.env['ecole.enseignant']
        self.parent_obj = self.env['ecole.parent']
        self.ecole_ecole_obj = self.env['ecole.ecole']
        self.ecole_standard_obj = self.env['ecole.standard']
        self.res_company_obj = self.env['res.company']
        self.assign_roll_obj = self.env['assign.roll.no']
        self.ecole_id = self.env.ref('ecole.demo_ecole_1')
        self.standard_medium = self.env.ref('ecole.demo_standard_medium_1')
        self.year = self.env.ref('ecole.demo_academic_year_2')
        self.currency_id = self.env.ref('base.INR')
        self.sch = self.env.ref('ecole.demo_ecole_1')
        self.country_id = self.env.ref('base.in')
        self.std = self.env.ref('ecole.demo_standard_standard_1')
        self.state_id = self.env.ref('base.state_in_gj')
        self.subject1 = self.env.ref('ecole.demo_subject_subject_1')
        self.subject2 = self.env.ref('ecole.demo_subject_subject_2')
        self.eleve_eleve = self.env.ref('ecole.demo_eleve_eleve_2')
        self.eleve_done = self.env.ref('ecole.demo_eleve_eleve_6')
        self.parent = self.env.ref('ecole.demo_eleve_parent_1')
        eleve_list = [self.eleve_done.id]
        self.eleve_eleve._compute_eleve_age()
        self.eleve_eleve.check_age()
        self.eleve_eleve.admission_done()
        self.eleve_eleve.set_alumni()
        self.parent.eleve_id = [(6, 0, eleve_list)]
        # Create annee academique
        self.academic_year_obj = self.env['academic.year']
        self.academic_year = self.academic_year_obj.\
            create({'sequence': 7,
                    'code': '2012',
                    'name': '2012 Year',
                    'date_start': time.strftime('01-01-2012'),
                    'date_stop': time.strftime('12-31-2012')
                    })
        self.academic_year._check_academic_year()
        self.academic_month_obj = self.env['academic.month']
        # Academic month created
        self.academic_month = self.academic_month_obj.\
            create({'name': 'May',
                    'code': 'may',
                    'date_start': time.strftime('05-01-2012'),
                    'date_stop': time.strftime('05-31-2012'),
                    'year_id': self.academic_year.id
                    })
        self.academic_month._check_duration()
        self.academic_month._check_year_limit()
        self.assign_roll_no = self.assign_roll_obj.\
            create({'standard_id': self.std.id,
                    'medium_id': self.standard_medium.id
                    })
        self.assign_roll_no.assign_rollno()

    def test_ecole(self):
        self.assertEqual(self.eleve_eleve.ecole_id,
                         self.eleve_eleve.standard_id.ecole_id)
