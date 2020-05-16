# See LICENSE file for full copyright and licensing details.
import self as self
import time
import base64
from datetime import date
from odoo import models, fields, api, tools, _
from odoo.modules import get_module_resource
from odoo.exceptions import except_orm
from odoo.exceptions import ValidationError
from .import ecole

# from lxml import etree
# added import etatment in try-except because when server runs on
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
    _description = 'Information eleve'

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False,
                access_rights_uid=None):
        '''Method to get eleve of parent having group enseignant'''
        groupe_enseignant = self.env.user.has_group('ecole.group_ecole_enseignant')
        parent_grp = self.env.user.has_group('ecole.group_ecole_parent')
        login_user = self.env['res.users'].browse(self._uid)
        nom = self._context.get('eleve_id')
        if nom and groupe_enseignant and parent_grp:
            parent_login_stud = self.env['ecole.parent'
                                         ].search([('partner_id', '=',
                                                  login_user.partner_id.id)
                                                   ])
            enfants = parent_login_stud.eleve_id
            args.append(('id', 'in', enfants.ids))
        return super(eleveeleve, self)._search(
            args=args, offset=offset, limit=limit, order=order, count=count,
            access_rights_uid=access_rights_uid)

    @api.depends('date_de_naissance')
    def _compute_eleve_age(self):
        '''Method to calculate eleve age'''
        courant_dt = date.today()
        for rec in self:
            if rec.date_de_naissance:
                debut = rec.date_de_naissance
                age_calc = ((courant_dt - debut).days / 365)
                # Age should be greater than 0
                if age_calc > 0.0:
                    rec.age = age_calc

    @api.constrains('date_de_naissance')
    def verifier_age(self):
        '''Method to check age should be greater than 5'''
        courant_dt = date.today()
        if self.date_de_naissance:
            debut = self.date_de_naissance
            age_calc = ((courant_dt - debut).days / 365)
            # Check if age less than 5 annees
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
        if res.etat == 'Brouillon':
            groupe_admission = self.env.ref('ecole.group_is_admission')
            nouveau_grp_liste = [groupe_admission.id, emp_grp.id]
            res.user_id.write({'groups_id': [(6, 0, nouveau_grp_liste)]})
        elif res.etat == 'terminé':
            terminé_eleve = self.env.ref('ecole.group_ecole_eleve')
            groupe_liste = [terminé_eleve.id, emp_grp.id]
            res.user_id.write({'groups_id': [(6, 0, groupe_liste)]})
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

    @api.depends('etat')
    def _compute_enseignant_user(self):
        for rec in self:
            if rec.etat == 'terminé':
                enseignant = self.env.user.has_group("ecole.group_ecole_enseignant"
                                                  )
                if enseignant:
                    rec.enseignant_grp = True

    @api.model
    def verifier_annee_courant(self):
        '''Method to get default value of logged in eleve'''
        res = self.env['annee.scolaire'].search([('courant', '=',
                                                 True)])
        if not res:
            raise ValidationError(_('''Il n'y a pas de courant scolaire scolaire
                                    Veuillez contacter l'administrateur!'''
                                    ))
        return res.id

    famille_con_ids = fields.One2many('eleve.contact.famille',
                                     'contact.famille_id',
                                     'contact famille Detaile',
                                     etats={'terminé': [('readonly', True)]})
    user_id = fields.Many2one('res.users', 'User ID', ondelete="cascade",
                              required=True, delegate=True)
    nom_eleve = fields.Char('Nom Elève', related='user_id.nom',
                               store=True, readonly=True)
    pid = fields.Char('ID Elève', required=True,
                      default=lambda self: _('New'),
                      help='Personal IDentification Number')
    reg_code = fields.Char('Code Registration',
                           help='eleve Registration Code')
    eleve_code = fields.Char('Code Elève')
    contact_telephone = fields.Char('Numéro Téléphone.')
    contact_portable = fields.Char('Numéro Portable')

    photo = fields.Binary('Photo', default=_default_image)
    annee = fields.Many2one('annee.scolaire', 'Année Scolaire', readonly=True,
                           default=verifier_annee_courant)
    caste_id = fields.Many2one('eleve.caste', 'Réligion/Caste')
    relation = fields.Many2one('eleve.relation.maitre', 'Relation')

    date_admission = fields.Date('Date Admission ', default=date.today())
    nom_famille_eleve = fields.Char('Nom Famille', required=True,
                       etats={'terminé': [('readonly', True)]})
    sexe = fields.Selection([('Homme', 'Homme'), ('Femme', 'Femme')],
                              'Sexe', etats={'terminé': [('readonly', True)]})
    date_de_naissance = fields.Date('Date De Naissance', required=True,
                                etats={'terminé': [('readonly', True)]})
    langue_maternelle = fields.Many2one('langue.maternelle', "Langue Maternelle")
    age = fields.Integer(compute='_compute_eleve_age', string='Age',
                         readonly=True)
    etat_civil = fields.Selection([('célibataire', 'célibataire'),
                                        ('Marié', 'Marié')],
                                       'Etat Civil',
                                       etats={'terminé': [('readonly', True)]})
    precedent_ecole_ids = fields.One2many('eleve.precedent.ecole',
                                          'precedent_ecole_id',
                                          'Détail École précédente',
                                          etats={'terminé': [('readonly',
                                                            True)]})
    medecin = fields.Char('Nom Médecin', etats={'terminé': [('readonly', True)]})
    designation = fields.Char('Désignation')
    medecin_telephone = fields.Char('Numéro Contact.')
    groupe_sanguin = fields.Char('Groupe Sanguin')
    hauteur = fields.Float('Hauteur', help="Hauteur dans C.M")
    largeur = fields.Float('Largeur', help="Largeur dans K.G")
    yeux = fields.Boolean('Yeux')
    oreille = fields.Boolean('Oreilles')
    nez_gorge = fields.Boolean('Nez et gorge')
    respiratoire = fields.Boolean('Respiratoire')
    cardiovasculaire = fields.Boolean('Cardiovasculaire')
    neurologique = fields.Boolean('Neurologique')
    dermatologique = fields.Boolean('Dermatologique')
    pression_arterielle = fields.Boolean('Pression artérielle')
    ecole_id = fields.Many2one('ecole.ecole', 'Ecole',
                                etats={'terminé': [('readonly', True)]})
    etat = fields.Selection([('Brouillon', 'Brouillon'),
                              ('terminé', 'terminé'),
                              ('mettre_fin', 'mettre_fin'),
                              ('annuler', 'annuler'),
                              ('ancien', 'ancien')],
                             'Status', readonly=True, default="Brouillon")
    descplines_ids = fields.One2many('eleve.desciplines', 'eleve_id', 'Desciplines')
    sanctions_ids = fields.One2many('eleve.sanctions', 'eleve_id', 'Sanctions')

    certificat_ids = fields.One2many('eleve.certificat', 'eleve_id',
                                      'Certification')
    document = fields.One2many('eleve.document', 'doc_id', 'Documents')
    description = fields.One2many('eleve.description', 'des_id',
                                  'Déscription')
    nom_ele = fields.Char('Prénom', related='user_id.nom',
                           readonly=True)
    annee_scolaire = fields.Char('Année', related='annee.nom',
                                help='annee scolaire', readonly=True)
    division_id = fields.Many2one('classe.division', 'Division')
    classe_id = fields.Many2one('ecole.classe', 'Classe')
    parent_id = fields.Many2many('ecole.parent', 'eleves_parents_rel',
                                 'eleve_id',
                                 'eleves_parent_id', 'Parent(s)',
                                 etats={'terminé': [('readonly', True)]})
    mettre_fin_raison = fields.Text('Raison')
    active = fields.Boolean(default=True)
    enseignant_grp = fields.Boolean("Groupe Enseignant",
                                     compute="_compute_enseignant_user",
                                     )
    active = fields.Boolean(default=True)

    @api.multi
    def set_to_Brouillon(self):
        '''Method to change etat to Brouillon'''
        self.etat = 'Brouillon'

    @api.multi
    def set_ancien(self):
        '''Method to change etat to ancien'''
        eleve_user = self.env['res.users']
        for rec in self:
            rec.etat = 'ancien'
            rec.classe_id._compute_total_eleve()
            user = eleve_user.search([('id', '=',
                                         rec.user_id.id)])
            rec.active = False
            if user:
                user.active = False

    @api.multi
    def set_terminé(self):
        '''Method to change etat to terminé'''
        self.etat = 'terminé'

    @api.multi
    def admission_Brouillon(self):
        '''Set the etat to Brouillon'''
        self.etat = 'Brouillon'

    @api.multi
    def set_mettre_fin(self):
        self.etat = 'mettre_fin'

    @api.multi
    def annuler_admission(self):
        self.etat = 'annuler'

    @api.multi
    def admission_terminé(self):
        '''Method to confirm admission'''
        ecole_classe_obj = self.env['ecole.classe']
        ir_sequence = self.env['ir.sequence']
        eleve_group = self.env.ref('ecole.group_ecole_eleve')
        emp_group = self.env.ref('base.group_user')
        for rec in self:
            if not rec.classe_id:
                raise ValidationError(_('''SVP Séléctionnez Classe!'''))
            if rec.classe_id.sièges_restants <= 0:
                raise ValidationError(_('Les classe% s sont pleins'
                                        ) % rec.classe_id.classe_id.nom)
            domain = [('ecole_id', '=', rec.ecole_id.id)]
            # Checks the classe if not defined raise error
            if not ecole_classe_obj.search(domain):
                raise except_orm(_('Avertissement'),
                                 _('''Classe Non trouvé dans
                                     ecole'''))
            # Assign group to eleve
            rec.user_id.write({'groups_id': [(6, 0, [emp_group.id,
                                                     eleve_group.id])]})
            # Assign registration code to eleve
            reg_code = ir_sequence.next_by_code('eleve.registration')
            registation_code = (str(rec.ecole_id.etat_id.nom) + str('/') +
                                str(rec.ecole_id.ville) + str('/') +
                                str(rec.ecole_id.nom) + str('/') +
                                str(reg_code))
            stu_code = ir_sequence.next_by_code('eleve.code')
            eleve_code = (str(rec.ecole_id.code) + str('/') +
                            str(rec.annee.code) + str('/') +
                            str(stu_code))
            rec.write({'etat': 'terminé',
                       'date_admission': time.strftime('%Y-%m-%d'),
                       'eleve_code': eleve_code,
                       'reg_code': registation_code})
        return True
class eleveDesciplines(models.Model):
    _name = 'eleve.desciplines'
    _description = "eleve Disciplines"

    matiere_id = fields.Many2one('matiere.matiere', 'Nom Matière')
    device_datetime = fields.Datetime(string='Heure Machine')
    status=fields.Char("status")
    eleve_id = fields.Many2one('eleve.eleve', 'Elève')

class eleveSanctions(models.Model):
    _name ='eleve.sanctions'
    _description = "eleve Sanctions"
    sanction = fields.Char("santion")
    nombre=fields.Integer("nombre")
    eleve_id = fields.Many2one('eleve.eleve', 'Elève')
