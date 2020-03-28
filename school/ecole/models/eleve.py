# See LICENSE file for full copyright and licensing details.

import time
import base64
from datetime import date
from odoo import models, fields, api, tools, _
from odoo.modules import get_module_resource
from odoo.exceptions import except_orm
from odoo.exceptions import ValidationError
from .import ecole

# from lxml import etree
# added import statement in try-except because when server runs on
# windows operating system issue arise because this library is not in Windows.
try:
    from odoo.tools import image_colorize, image_resize_image_big
except:
    image_colorize = False
    image_resize_image_big = False


class eleveeleve(models.Model):
    ''' Defining a eleve information '''
    _name = 'eleve.eleve'
    _table = "eleve_eleve"
    _description = 'eleve Information'

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False,
                access_rights_uid=None):
        '''Method to get eleve of parent having group enseignant'''
        enseignant_group = self.env.user.has_group('ecole.group_ecole_enseignant')
        parent_grp = self.env.user.has_group('ecole.group_ecole_parent')
        login_user = self.env['res.users'].browse(self._uid)
        name = self._context.get('eleve_id')
        if name and enseignant_group and parent_grp:
            parent_login_stud = self.env['ecole.parent'
                                         ].search([('partner_id', '=',
                                                  login_user.partner_id.id)
                                                   ])
            childrens = parent_login_stud.eleve_id
            args.append(('id', 'in', childrens.ids))
        return super(eleveeleve, self)._search(
            args=args, offset=offset, limit=limit, order=order, count=count,
            access_rights_uid=access_rights_uid)

    @api.depends('date_of_birth')
    def _compute_eleve_age(self):
        '''Method to calculate eleve age'''
        current_dt = date.today()
        for rec in self:
            if rec.date_of_birth:
                start = rec.date_of_birth
                age_calc = ((current_dt - start).days / 365)
                # Age should be greater than 0
                if age_calc > 0.0:
                    rec.age = age_calc

    @api.constrains('date_of_birth')
    def check_age(self):
        '''Method to check age should be greater than 5'''
        current_dt = date.today()
        if self.date_of_birth:
            start = self.date_of_birth
            age_calc = ((current_dt - start).days / 365)
            # Check if age less than 5 years
            if age_calc < 5:
                raise ValidationError(_('''Age Eleve obligatoirement supérieur à 5ans!'''))

    @api.model
    def create(self, vals):
        '''Method to create user when eleve is created'''
        if vals.get('pid', _('New')) == _('New'):
            vals['pid'] = self.env['ir.sequence'
                                   ].next_by_code('eleve.eleve'
                                                  ) or _('New')
        if vals.get('pid', False):
            vals['login'] = vals['pid']
            vals['password'] = vals['pid']
        else:
            raise except_orm(_('Erreur!'),
                             _('''PID non valide
                                 donc record ne sera pas enregistrer.'''))
        if vals.get('company_id', False):
            company_vals = {'company_ids': [(4, vals.get('company_id'))]}
            vals.update(company_vals)
        if vals.get('email'):
            ecole.emailvalidation(vals.get('email'))
        res = super(eleveeleve, self).create(vals)
        enseignant = self.env['ecole.enseignant']
        for data in res.parent_id:
            enseignant_rec = enseignant.search([('stu_parent_id',
                                           '=', data.id)])
            for record in enseignant_rec:
                record.write({'eleve_id': [(4, res.id, None)]})
        # Assign group to eleve based on condition
        emp_grp = self.env.ref('base.group_user')
        if res.state == 'draft':
            admission_group = self.env.ref('ecole.group_is_admission')
            new_grp_list = [admission_group.id, emp_grp.id]
            res.user_id.write({'groups_id': [(6, 0, new_grp_list)]})
        elif res.state == 'done':
            done_eleve = self.env.ref('ecole.group_ecole_eleve')
            group_list = [done_eleve.id, emp_grp.id]
            res.user_id.write({'groups_id': [(6, 0, group_list)]})
        return res

    @api.multi
    def write(self, vals):
        enseignant = self.env['ecole.enseignant']
        if vals.get('parent_id'):
            for parent in vals.get('parent_id')[0][2]:
                enseignant_rec = enseignant.search([('stu_parent_id',
                                               '=', parent)])
                for data in enseignant_rec:
                    data.write({'eleve_id': [(4, self.id)]})
        return super(eleveeleve, self).write(vals)

    @api.model
    def _default_image(self):
        '''Method to get default Image'''
        image_path = get_module_resource('hr', 'static/src/img',
                                         'default_image.png')
        return tools.image_resize_image_big(base64.b64encode(open(image_path,
                                                                  'rb').read()
                                                             ))

    @api.depends('state')
    def _compute_enseignant_user(self):
        for rec in self:
            if rec.state == 'done':
                enseignant = self.env.user.has_group("ecole.group_ecole_enseignant"
                                                  )
                if enseignant:
                    rec.teachr_user_grp = True

    @api.model
    def check_current_year(self):
        '''Method to get default value of logged in eleve'''
        res = self.env['academic.year'].search([('current', '=',
                                                 True)])
        if not res:
            raise ValidationError(_('''There is no current annee academique
                                    defined!Please contact to Administator!'''
                                    ))
        return res.id

    family_con_ids = fields.One2many('eleve.family.contact',
                                     'family_contact_id',
                                     'Family Contact Detail',
                                     states={'done': [('readonly', True)]})
    user_id = fields.Many2one('res.users', 'User ID', ondelete="cascade",
                              required=True, delegate=True)
    eleve_name = fields.Char('Nom Elève', related='user_id.name',
                               store=True, readonly=True)
    pid = fields.Char('ID Elève', required=True,
                      default=lambda self: _('New'),
                      help='Personal IDentification Number')
    reg_code = fields.Char('Code Registration',
                           help='eleve Registration Code')
    eleve_code = fields.Char('Code Elève')
    contact_phone = fields.Char('Numéro Téléphone.')
    contact_mobile = fields.Char('Numéro Portable')
    roll_no = fields.Integer('Numéro Roll.', readonly=True)
    photo = fields.Binary('Photo', default=_default_image)
    year = fields.Many2one('academic.year', 'Année Académique', readonly=True,
                           default=check_current_year)
    cast_id = fields.Many2one('eleve.cast', 'Réligion/Caste')
    relation = fields.Many2one('eleve.relation.master', 'Relation')

    admission_date = fields.Date('Date Admission ', default=date.today())
    middle = fields.Char('Deuxième Nom', required=True,
                         states={'done': [('readonly', True)]})
    last = fields.Char('Surname', required=True,
                       states={'done': [('readonly', True)]})
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],
                              'Sexe', states={'done': [('readonly', True)]})
    date_of_birth = fields.Date('Date De Naissance', required=True,
                                states={'done': [('readonly', True)]})
    mother_tongue = fields.Many2one('mother.toungue', "Langue Maternelle")
    age = fields.Integer(compute='_compute_eleve_age', string='Age',
                         readonly=True)
    maritual_status = fields.Selection([('célibataire', 'célibataire'),
                                        ('Marié', 'Marié')],
                                       'Marital Status',
                                       states={'done': [('readonly', True)]})
    reference_ids = fields.One2many('eleve.reference', 'reference_id',
                                    'Réferences',
                                    states={'done': [('readonly', True)]})
    previous_ecole_ids = fields.One2many('eleve.previous.ecole',
                                          'previous_ecole_id',
                                          'Détail École précédente',
                                          states={'done': [('readonly',
                                                            True)]})
    doctor = fields.Char('Doctor Name', states={'done': [('readonly', True)]})
    designation = fields.Char('Désignation')
    doctor_phone = fields.Char('Numéro Contact.')
    blood_group = fields.Char('Groupe Sanguin')
    height = fields.Float('Hauteur', help="Hieght in C.M")
    weight = fields.Float('Largeur', help="Weight in K.G")
    eye = fields.Boolean('Yeux')
    ear = fields.Boolean('Oreilles')
    nose_throat = fields.Boolean('Nez et gorge')
    respiratory = fields.Boolean('Respiratoire')
    cardiovascular = fields.Boolean('Cardiovasculaire')
    neurological = fields.Boolean('Neurologique')
    muskoskeletal = fields.Boolean('Appareil locomoteur')
    dermatological = fields.Boolean('Dermatologique')
    blood_pressure = fields.Boolean('Pression artérielle')
    remark = fields.Text('Remark', states={'done': [('readonly', True)]})
    ecole_id = fields.Many2one('ecole.ecole', 'Ecole',
                                states={'done': [('readonly', True)]})
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('terminate', 'Terminate'),
                              ('cancel', 'Cancel'),
                              ('alumni', 'Alumni')],
                             'Status', readonly=True, default="draft")
    history_ids = fields.One2many('eleve.history', 'eleve_id', 'Historique')
    descplines_ids = fields.One2many('eleve.desciplines', 'eleve_id', 'Desciplines')
    statistiques_ids = fields.One2many('eleve.statistiques', 'eleve_id', 'Statistiques')
    certificate_ids = fields.One2many('eleve.certificate', 'eleve_id',
                                      'Certificat')
    eleve_discipline_line = fields.One2many('eleve.descipline',
                                              'eleve_id', 'Descipline')
    document = fields.One2many('eleve.document', 'doc_id', 'Documents')
    description = fields.One2many('eleve.description', 'des_id',
                                  'Déscription')
    award_list = fields.One2many('eleve.award', 'award_list_id',
                                 'Liste des prix')
    stu_name = fields.Char('Prénom', related='user_id.name',
                           readonly=True)
    Acadamic_year = fields.Char('Année', related='year.name',
                                help='annee academique', readonly=True)
    division_id = fields.Many2one('standard.division', 'Division')
    medium_id = fields.Many2one('standard.medium', 'Medium')
    standard_id = fields.Many2one('ecole.standard', 'Classe')
    parent_id = fields.Many2many('ecole.parent', 'eleves_parents_rel',
                                 'eleve_id',
                                 'eleves_parent_id', 'Parent(s)',
                                 states={'done': [('readonly', True)]})
    terminate_reason = fields.Text('Raison')
    active = fields.Boolean(default=True)
    teachr_user_grp = fields.Boolean("Groupe Enseignant",
                                     compute="_compute_enseignant_user",
                                     )
    active = fields.Boolean(default=True)

    @api.multi
    def set_to_draft(self):
        '''Method to change state to draft'''
        self.state = 'draft'

    @api.multi
    def set_alumni(self):
        '''Method to change state to alumni'''
        eleve_user = self.env['res.users']
        for rec in self:
            rec.state = 'alumni'
            rec.standard_id._compute_total_eleve()
            user = eleve_user.search([('id', '=',
                                         rec.user_id.id)])
            rec.active = False
            if user:
                user.active = False

    @api.multi
    def set_done(self):
        '''Method to change state to done'''
        self.state = 'done'

    @api.multi
    def admission_draft(self):
        '''Set the state to draft'''
        self.state = 'draft'

    @api.multi
    def set_terminate(self):
        self.state = 'terminate'

    @api.multi
    def cancel_admission(self):
        self.state = 'cancel'

    @api.multi
    def admission_done(self):
        '''Method to confirm admission'''
        ecole_standard_obj = self.env['ecole.standard']
        ir_sequence = self.env['ir.sequence']
        eleve_group = self.env.ref('ecole.group_ecole_eleve')
        emp_group = self.env.ref('base.group_user')
        for rec in self:
            if not rec.standard_id:
                raise ValidationError(_('''SVP Séléctionnez Classe!'''))
            if rec.standard_id.remaining_seats <= 0:
                raise ValidationError(_('Seats of class %s are full'
                                        ) % rec.standard_id.standard_id.name)
            domain = [('ecole_id', '=', rec.ecole_id.id)]
            # Checks the standard if not defined raise error
            if not ecole_standard_obj.search(domain):
                raise except_orm(_('Avertissement'),
                                 _('''Standard Non trouvé dans
                                     ecole'''))
            # Assign group to eleve
            rec.user_id.write({'groups_id': [(6, 0, [emp_group.id,
                                                     eleve_group.id])]})
            # Assign roll no to eleve
            number = 1
            for rec_std in rec.search(domain):
                rec_std.roll_no = number
                number += 1
            # Assign registration code to eleve
            reg_code = ir_sequence.next_by_code('eleve.registration')
            registation_code = (str(rec.ecole_id.state_id.name) + str('/') +
                                str(rec.ecole_id.city) + str('/') +
                                str(rec.ecole_id.name) + str('/') +
                                str(reg_code))
            stu_code = ir_sequence.next_by_code('eleve.code')
            eleve_code = (str(rec.ecole_id.code) + str('/') +
                            str(rec.year.code) + str('/') +
                            str(stu_code))
            rec.write({'state': 'done',
                       'admission_date': time.strftime('%Y-%m-%d'),
                       'eleve_code': eleve_code,
                       'reg_code': registation_code})
        return True
class eleveDesciplines(models.Model):
    _name = 'eleve.desciplines'
    _description = "eleve Disciplines"

    subject_id = fields.Many2one('subject.subject', 'Nom Matière')
    device_datetime = fields.Datetime(string='Heure Machine')
    status=fields.Char("status")
    eleve_id = fields.Many2one('eleve.eleve', 'Elève')

    class StudentStatistique(models.Model):
        _name = 'eleve.statistiques'
        _description = "eleve statistiques"

        Abscence = fields.Integer("Statistique sur l'abscence")
        avertissement = fields.Integer("Statistique sur l'avertissement")
        Exclu = fields.Integer("Statistique sur l'Exclu")
        eleve_id = fields.Many2one('eleve.eleve', 'Elève')