# See LICENSE file for full copyright and licensing details.

# import time
import re
import calendar
from datetime import datetime
from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import except_orm
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


EM = (r"[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$")


def emailvalidation(email):

    if email:
        EMAIL_REGEX = re.compile(EM)
        if not EMAIL_REGEX.match(email):
            raise ValidationError(_('''This seems not to be valid email.
            Please enter email in correct format!'''))
        else:
            return True


class scolaireannee(models.Model):
    ''' Defines an annee scolaire '''
    _name = "annee.scolaire"
    _description = "annee scolaire"
    _order = "sequence"

    sequence = fields.Integer('Sequence', required=True,
                              help="Sequence order you want to see this annee.")
    nom = fields.Char('nom', required=True, help='nom of annee scolaire')
    code = fields.Char('Code', required=True, help='Code of annee scolaire')
    debut_date = fields.Date('Debut Date', required=True,
                             help='debuting date of annee scolaire')
    fin_date = fields.Date('fin date', required=True,
                            help='Ending of annee scolaire')
    mois_ids = fields.One2many('mois.scolaire', 'annee_id', 'mois',
                                help="related mois scolaires")
    mention_id = fields.Many2one('mention.maitre', "Mention")
    courant = fields.Boolean('courant', help="Set Active courant annee")
    description = fields.Text('Description')

    @api.model
    def next_annee(self, sequence):
        '''This method assign sequence to annees'''
        annee_id = self.search([('sequence', '>', sequence)], order='id',
                              limit=1)
        if annee_id:
            return annee_id.id
        return False

    @api.multi
    def nom_get(self):
        '''Method to display nom and code'''
        return [(rec.id, ' [' + rec.code + ']' + rec.nom) for rec in self]

    @api.multi
    def generate_scolairemois(self):
        interval = 1
        mois_obj = self.env['mois.scolaire']
        for data in self:
            ds = data.debut_date
            while ds < data.fin_date:
                de = ds + relativedelta(mois=interval, days=-1)
                if de > data.fin_date:
                    de = data.fin_date
                mois_obj.create({
                    'nom': ds.strftime('%B'),
                    'code': ds.strftime('%m/%Y'),
                    'debut_date': ds.strftime('%Y-%m-%d'),
                    'fin_date': de.strftime('%Y-%m-%d'),
                    'annee_id': data.id,
                })
                ds = ds + relativedelta(mois=interval)
        return True

    @api.constrains('debut_date', 'fin_date')
    def _check_annee_scolaire(self):
        '''Method to check Debut Date should be greater than fin date
           also check that dates are not overlapped with existing scolaire
           annee'''
        new_debut_date = self.debut_date
        new_stop_date = self.fin_date
        delta = new_stop_date - new_debut_date
        if delta.days > 365 and not calendar.isleap(new_debut_date.annee):
            raise ValidationError(_('''Error! The duration of the annee scolaire
                                      is invalid.'''))
        if (self.fin_date and self.debut_date and
                self.fin_date < self.debut_date):
            raise ValidationError(_('''The Debut Date of the annee scolaire'
                                      should be less than fin date.'''))
        for old_ac in self.search([('id', 'not in', self.ids)]):
            # Check Debut Date should be less than stop date
            if (old_ac.debut_date <= self.debut_date <= old_ac.fin_date or
                    old_ac.debut_date <= self.fin_date <= old_ac.fin_date):
                raise ValidationError(_('''Error! You cannot define overlapping
                                          annee scolaires.'''))

    @api.constrains('courant')
    def verifier_annee_courant(self):
        check_annee = self.search([('courant', '=', True)])
        if len(check_annee.ids) >= 2:
            raise ValidationError(_('''Error! You cannot set two courant
            annee active!'''))


class scolairemois(models.Model):
    ''' Defining a mois of an annee scolaire '''
    _name = "mois.scolaire"
    _description = "mois scolaire"
    _order = "debut_date"

    nom = fields.Char('nom', required=True, help='nom of mois scolaire')
    code = fields.Char('Code', required=True, help='Code of mois scolaire')
    debut_date = fields.Date('debut of Period', required=True,
                             help='debuting of mois scolaire')
    fin_date = fields.Date('End of Period', required=True,
                            help='Ending of mois scolaire')
    annee_id = fields.Many2one('annee.scolaire', 'annee scolaire', required=True,
                              help="Related annee scolaire ")
    description = fields.Text('Description')

    _sql_constraints = [
        ('mois_unique', 'unique(debut_date, fin_date, annee_id)',
         'mois scolaire should be unique!'),
    ]

    @api.constrains('debut_date', 'fin_date')
    def _check_duration(self):
        '''Method to check duration of date'''
        if (self.fin_date and self.debut_date and
                self.fin_date < self.debut_date):
            raise ValidationError(_(''' La date de fin de période doit être supérieure
                                    que le début de la date Peroid!'''))

    @api.constrains('annee_id', 'debut_date', 'fin_date')
    def _check_annee_limit(self):
        '''Method to check annee limit'''
        if self.annee_id and self.debut_date and self.fin_date:
            if (self.annee_id.fin_date < self.fin_date or
                    self.annee_id.fin_date < self.debut_date or
                    self.annee_id.debut_date > self.debut_date or
                    self.annee_id.debut_date > self.fin_date):
                raise ValidationError(_('''Mois invalide! Quelques mois se chevauchent
                                    ou la période de date n'est pas dans la portée
                                    de l'annee scolaire!'''))

    @api.constrains('debut_date', 'fin_date')
    def check_mois(self):
        for old_mois in self.search([('id', 'not in', self.ids)]):
            # Check Debut Date should be less than stop date
            if old_mois.debut_date <= \
                    self.debut_date <= old_mois.fin_date \
                    or old_mois.debut_date <= \
                    self.fin_date <= old_mois.fin_date:
                    raise ValidationError(_('''Erreur! Vous ne pouvez pas définir
                    mois qui se chevauchent!'''))



class classeDivision(models.Model):
    ''' Defining a division(A, B, C) related to classe'''
    _name = "classe.division"
    _description = "classe Division"
    _order = "sequence"

    sequence = fields.Integer('Sequence', required=True)
    nom = fields.Char('nom', required=True)
    code = fields.Char('Code', required=True)
    description = fields.Text('Description')


class classeclasse(models.Model):
    ''' Defining classe Information '''
    _name = 'classe.classe'
    _description = 'Information Classe'
    _order = "sequence"

    sequence = fields.Integer('Sequence', required=True)
    nom = fields.Char('nom', required=True)
    code = fields.Char('Code', required=True)
    description = fields.Text('Description')

    @api.model
    def classe_suivant(self, sequence):
        '''This method check sequence of classe'''
        classe_ids = self.search([('sequence', '>', sequence)], order='id',
                                limit=1)
        if classe_ids:
            return classe_ids.id
        return False


class Ecoleclasse(models.Model):
    ''' Defining a classe related to ecole '''
    _name = 'ecole.classe'
    _description = 'Ecole classes'
    _rec_name = "classe_id"

    @api.depends('classe_id', 'ecole_id', 'division_id',
                 'ecole_id')
    def _compute_eleve(self):
        '''Compute eleve of terminé etat'''
        eleve_obj = self.env['eleve.eleve']
        for rec in self:
            rec.eleve_ids = eleve_obj.\
                search([('classe_id', '=', rec.id),
                        ('ecole_id', '=', rec.ecole_id.id),
                        ('division_id', '=', rec.division_id.id),
                        ('etat', '=', 'terminé')])

    @api.onchange('classe_id', 'division_id')
    def onchange_combine(self):
        self.nom = str(self.classe_id.nom
                        ) + '-' + str(self.division_id.nom)

    @api.depends('matiere_ids')
    def _compute_matiere(self):
        '''Method to compute matieres'''
        for rec in self:
            rec.total_no_matieres = len(rec.matiere_ids)

    @api.depends('eleve_ids')
    def _compute_total_eleve(self):
        for rec in self:
            rec.total_eleves = len(rec.eleve_ids)

    @api.depends("capacité", "total_eleves")
    def _compute_remain_seats(self):
        for rec in self:
            rec.remaining_seats = rec.capacité - rec.total_eleves

    ecole_id = fields.Many2one('ecole.ecole', 'Ecole', required=True)
    classe_id = fields.Many2one('classe.classe', 'Classe',
                                  required=True)
    division_id = fields.Many2one('classe.division', 'Division',
                                  required=True)
    matiere_ids = fields.Many2many('matiere.matiere', 'matiere_classes_rel',
                                   'matiere_id', 'classe_id', 'matiere')
    user_id = fields.Many2one('ecole.enseignant', 'Class enseignant')
    eleve_ids = fields.One2many('eleve.eleve', 'classe_id',
                                  'eleve dans classe',
                                  compute='_compute_eleve', store=True
                                  )
    couleur = fields.Integer('couleur Index')
    cmp_id = fields.Many2one('res.company', 'nom societe',
                             related='ecole_id.company_id', store=True)

    total_no_matieres = fields.Integer('Nombre total de matiere',
                                       compute="_compute_matiere")
    nom = fields.Char('nom')
    capacité = fields.Integer("Nombre total de sièges")
    total_eleves = fields.Integer("Total eleves",
                                    compute="_compute_total_eleve",
                                    store=True)
    sièges_restants = fields.Integer("Places libres",
                                     compute="_compute_remain_seats",
                                     store=True)
    salle_classe_id = fields.Many2one('salle.classe', 'Numéro salle')

    @api.constrains('classe_id', 'division_id')
    def check_classe_unique(self):
        classe_search = self.env['ecole.classe'
                                   ].search([('classe_id', '=',
                                              self.classe_id.id),
                                             ('division_id', '=',
                                              self.division_id.id),
                                             ('ecole_id', '=',
                                              self.ecole_id.id),
                                             ('id', 'not in', self.ids)])
        if classe_search:
            raise ValidationError(_('''La division et la classe doivent être uniques!'''
                                    ))

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.eleve_ids or rec.matiere_ids :
                raise ValidationError(_('''Vous ne pouvez pas supprimer cette classe
                car il fait référence à eleve ou matiere !'''))
        return super(Ecoleclasse, self).unlink()

    @api.constrains('capacité')
    def check_seats(self):
        if self.capacité <= 0:
            raise ValidationError(_('''Le nombre total de sièges doit être supérieur à
                0!'''))

    @api.multi
    def nom_get(self):
        '''Method to display classe and division'''
        return [(rec.id, rec.classe_id.nom + '[' + rec.division_id.nom +
                 ']') for rec in self]


class EcoleEcole(models.Model):
    ''' Defining Ecole Information '''
    _name = 'ecole.ecole'
    _description = 'Ecole Information'
    _rec_name = "com_name"

    @api.model
    def _lang_get(self):
        '''Method to get langue'''
        langues = self.env['res.lang'].search([])
        return [(langue.code, langue.nom) for langue in langues]

    company_id = fields.Many2one('res.company', 'Societe',
                                 ondelete="cascade",
                                 required=True,
                                 delegate=True)
    com_name = fields.Char('Ecole nom', related='company_id.nom',
                           store=True)
    code = fields.Char('Code', required=True)
    classes = fields.One2many('ecole.classe', 'ecole_id',
                                'Classes')
    lang = fields.Selection(_lang_get, 'langue',
                            help='''Si la langue sélectionnée est chargée dans le
                                système, tous les documents liés à ce partenaire
                                sera imprimé dans cette langue.
                                Sinon, ce sera l'anglais.''')

    @api.model
    def create(self, vals):
        res = super(EcoleEcole, self).create(vals)
        main_company = self.env.ref('base.main_company')
        res.company_id.parent_id = main_company.id
        return res


class matierematiere(models.Model):
    '''Defining a matiere '''
    _name = "matiere.matiere"
    _description = "matieres"

    nom = fields.Char('nom', required=True)
    code = fields.Char('Code', required=True)
    maximum_note = fields.Integer("Maximum notes")
    minimum_note = fields.Integer("Minimum notes")
    weightage = fields.Integer("WeightAge")
    enseignant_ids = fields.Many2many('ecole.enseignant', 'matiere_enseignant_rel',
                                   'matiere_id', 'enseignant_id', 'enseignants')
    classe_ids = fields.Many2many('classe.classe',
                                    string='Classes')
    classe_id = fields.Many2one('classe.classe', 'Class')
    is_practical = fields.Boolean('Is Practical',
                                  help='Check this if matiere is practical.')

    eleve_ids = fields.Many2many('eleve.eleve',
                                   'elective_matiere_eleve_rel',
                                   'matiere_id', 'eleve_id', 'eleves')


class languematernelle(models.Model):
    _name = 'langue.maternelle'
    _description = "langue maternelle"

    nom = fields.Char("langue maternelle")


class eleveAward(models.Model):
    _name = 'eleve.award'
    _description = "eleve Awards"

    award_list_id = fields.Many2one('eleve.eleve', 'eleve')
    nom = fields.Char('Award nom')
    description = fields.Char('Description')


class AttendanceType(models.Model):
    _name = "attendance.type"
    _description = "Ecole Type"

    nom = fields.Char('nom', required=True)
    code = fields.Char('Code', required=True)


class eleveDocument(models.Model):
    _name = 'eleve.document'
    _description = "eleve Document"
    _rec_name = "doc_type"

    doc_id = fields.Many2one('eleve.eleve', 'eleve')
    file_no = fields.Char('File No', readonly="1", default=lambda obj:
                          obj.env['ir.sequence'].
                          next_by_code('eleve.document'))
    submited_date = fields.Date('Submitted Date')
    doc_type = fields.Many2one('document.type', 'Type Document', required=True)
    file_name = fields.Char('File nom',)
    return_date = fields.Date('Return Date')
    new_datas = fields.Binary('Attachments')


class DocumentType(models.Model):
    ''' Defining a Document Type(SSC,Leaving)'''
    _name = "document.type"
    _description = "Document Type"
    _rec_name = "doc_type"
    _order = "seq_no"

    seq_no = fields.Char('Sequence', readonly=True,
                         default=lambda self: _('New'))
    doc_type = fields.Char('Type Document', required=True)

    @api.model
    def create(self, vals):
        if vals.get('seq_no', _('New')) == _('New'):
            vals['seq_no'] = self.env['ir.sequence'
                                      ].next_by_code('document.type'
                                                     ) or _('New')
        return super(DocumentType, self).create(vals)


class eleveDescription(models.Model):
    ''' Defining a eleve Description'''
    _name = 'eleve.description'
    _description = "eleve Description"

    des_id = fields.Many2one('eleve.eleve', 'eleve Ref.')
    nom = fields.Char('Nom')
    description = fields.Char('Description')


class eleveDescipline(models.Model):
    _name = 'eleve.descipline'
    _description = "eleve Discipline"

    eleve_id = fields.Many2one('eleve.eleve', 'eleve')
    enseignant_id = fields.Many2one('ecole.enseignant', 'enseignant')
    date = fields.Date('Date')
    classe_id = fields.Many2one('classe.classe', 'Classe')
    note = fields.Text('Note')
    action_taken = fields.Text('Action Taken')


class eleveHistory(models.Model):
    _name = "eleve.history"
    _description = "eleve History"

    eleve_id = fields.Many2one('eleve.eleve', 'eleve')
    annee_scolaire_id = fields.Many2one('annee.scolaire', 'Année Scolaire',
                                        )
    classe_id = fields.Many2one('ecole.classe', 'Classe')
    percentage = fields.Float("Pourcentage", readonly=True)
    result = fields.Char('Resultat', readonly=True)


class elevecertificat(models.Model):
    _name = "eleve.certificat"
    _description = "eleve certificat"

    eleve_id = fields.Many2one('eleve.eleve', 'Elève')
    description = fields.Char('Description')
    certi = fields.Binary('Certification', required=True)


class eleveReference(models.Model):
    ''' Defining a eleve reference information '''
    _name = "eleve.reference"
    _description = "eleve Reference"

    reference_id = fields.Many2one('eleve.eleve', 'eleve')
    nom = fields.Char('First nom', required=True)
    middle = fields.Char('Middle nom', required=True)
    nom_famille_eleve = fields.Char('Surnom', required=True)
    designation = fields.Char('Designation', required=True)
    telephone = fields.Char('telephone', required=True)
    sexe = fields.Selection([('male', 'Male'), ('female', 'Female')],
                              'sexe')


class eleveprecedentEcole(models.Model):
    ''' Defining a eleve precedent ecole information '''
    _name = "eleve.precedent.ecole"
    _description = "eleve precedent Ecole"

    precedent_ecole_id = fields.Many2one('eleve.eleve', 'Elève')
    nom = fields.Char('nom', required=True)
    numero_enseignant = fields.Char('Numéro de Registration.', required=True)
    date_admission = fields.Date('Date Admission')
    date_sortie = fields.Date('Date de sortie')
    course_id = fields.Many2one('classe.classe', 'Cours', required=True)
    ajouter_mat = fields.One2many('matiere.scolaire', 'ajouter_mat_id', 'Ajouter Matière')

    @api.constrains('date_admission', 'date_sortie')
    def check_date(self):
        curr_dt = datetime.now()
        new_dt = datetime.strftime(curr_dt,
                                   DEFAULT_SERVER_DATE_FORMAT)
        if self.date_admission >= new_dt or self.date_sortie >= new_dt:
            raise ValidationError(_('''Your admission date and exit date
            should be less than courant date in precedent ecole details!'''))
        if self.date_admission > self.date_sortie:
            raise ValidationError(_(''' Admission date should be less than
            exit date in precedent ecole!'''))


class scolairematiere(models.Model):
    ''' Defining a eleve precedent ecole information '''
    _name = "matiere.scolaire"
    _description = "eleve Ecole Precedent"

    ajouter_mat_id = fields.Many2one('eleve.precedent.ecole', 'Add matieres',
                                 invisible=True)
    nom = fields.Char('nom', required=True)
    maximum_note = fields.Integer("Maximum notes")
    minimum_note = fields.Integer("Minimum notes")


class eleveContactFamille(models.Model):
    ''' Defining a eleve emergency contact information '''
    _name = "eleve.contact.famille"
    _description = "eleve contact.famille"

    @api.depends('relation', 'nom_ele')
    def _compute_get_name(self):
        for rec in self:
            if rec.nom_ele:
                rec.nom_relative = rec.nom_ele.nom
            else:
                rec.nom_relative = rec.nom

    contact_famille_id = fields.Many2one('eleve.eleve', 'eleve Ref.')
    nom_rel = fields.Selection([('exist', 'lien elève existant'),
                                 ('new', 'Créer un nouveau nom relatif')],
                                'eleve en relation', help="Selectionner nom",
                                required=True)
    user_id = fields.Many2one('res.users', 'User ID', ondelete="cascade")
    nom_ele = fields.Many2one('eleve.eleve', 'eleve existant',
                               help="Selectionner eleve à partir de la liste existant")
    nom = fields.Char('Nom Relative')
    relation = fields.Many2one('eleve.relation.maitre', 'Relation',
                               required=True)
    telephone = fields.Char('Numèro Télephone', required=True)
    email = fields.Char('E-Mail')
    nom_relative = fields.Char(compute='_compute_get_name', string='Nom')


class eleveRelationmaitre(models.Model):
    ''' eleve Relation Information '''
    _name = "eleve.relation.maitre"
    _description = "eleve Relation maitre"

    nom = fields.Char('nom', required=True, help="Entrer nom du relation")
    seq_no = fields.Integer('Sequence')


class mentionmaitre(models.Model):
    _name = 'mention.maitre'
    _description = "mention maitre"

    nom = fields.Char('Mention', required=True)
    mention_ids = fields.One2many('mention.ligne', 'mention_id', 'Mention ligne')


class mentionLine(models.Model):
    _name = 'mention.ligne'
    _description = "mentions"
    _rec_name = 'mention'

    de_note = fields.Integer('De note', required=True,
                               help='La mention commencera à partir de ces marques.')
    jusqu_note = fields.Integer('Jusqu a note', required=True,
                             help='La mention se terminera par ces marques.')
    mention = fields.Char('Mention', required=True, help="mention")
    sequence = fields.Integer('Sequence', help="Ordre de séquence de la mention.")
    échouer = fields.Boolean('échouer', help='Si  échouer  le champ est défini sur True,\
                                  cela vous permettra de définir la mention comme échouer.')
    mention_id = fields.Many2one("mention.maitre", 'Mention Ref.')
    nom = fields.Char('nom')


class eleveNews(models.Model):
    _name = 'eleve.news'
    _description = 'eleve News'
    _rec_name = 'matiere'
    _order = 'date asc'

    matiere = fields.Char('Matière', required=True,
                          help='matiere of the news.')
    description = fields.Text('Description', help="Description")
    date = fields.Datetime('Date Expiration', help='Date expiration des nouvelles.')
    user_ids = fields.Many2many('res.users', 'user_news_rel', 'id', 'user_ids',
                                'User News',
                                help='nom à qui cette nouvelle est liée.')
    couleur = fields.Integer('Index des couleurs', default=0)

    @api.constrains("date")
    def checknews_dates(self):
        new_date = datetime.now()
        if self.date < new_date:
            raise ValidationError(_('''Configurer une date d'expiration supérieure à
            date actuelle!'''))

    @api.multi
    def news_update(self):
        '''Method to send email to eleve for news update'''
        emp_obj = self.env['hr.employee']
        obj_mail_server = self.env['ir.mail_server']
        user = self.env['res.users'].browse(self._context.get('uid'))
        # Check if out going mail configured
        mail_server_ids = obj_mail_server.search([])
        if not mail_server_ids:
            raise except_orm(_('Email Erreur'),
                             _('''Aucun serveur de messagerie sortant
                               spécifié!'''))
        mail_server_record = mail_server_ids[0]
        email_list = []
        # Check email is defined in eleve
        for news in self:
            if news.user_ids and news.date:
                email_list = [news_user.email for news_user in news.user_ids
                              if news_user.email]
                if not email_list:
                    raise except_orm(_('Configuration de la messagerie utilisateur!'),
                                     _("E-mail introuvable chez les utilisateurs!"))
            # Check email is defined in user created from employee
            else:
                for employee in emp_obj.search([]):
                    if employee.email_travail:
                        email_list.append(employee.email_travail)
                    elif employee.user_id and employee.user_id.email:
                        email_list.append(employee.user_id.email)
                if not email_list:
                    raise except_orm(_('Email Configuration!'),
                                     _("Email not defined!"))
            news_date = news.date
            # Add company nom while sending email
            company = user.company_id.nom or ''
            body = """Salut, <br/> <br/>
                    Ceci est une mise à jour de <b>% s </b> publiée sur% s <br/>
                    <br/>% s <br/> <br/>
                    Je vous remercie.""" % (company,
                                     news_date.strftime('%d-%m-%Y %H:%M:%S'),
                                     news.description or '')
            smtp_user = mail_server_record.smtp_user or False
            # Check if mail of outgoing server configured
            if not smtp_user:
                raise except_orm(_('Configuration e-mail'),
                                 _("Veuillez configurer le serveur de courrier sortant!"))
            notification = 'Notification de mise à jour des nouvelles.'
            # Configure email
            message = obj_mail_server.build_email(email_from=smtp_user,
                                                  email_to=email_list,
                                                  matiere=notification,
                                                  body=body,
                                                  body_alternative=body,
                                                  reply_to=smtp_user,
                                                  subtype='html')
            # Send Email configured above with help of send mail method
            obj_mail_server.send_email(message=message,
                                       mail_server_id=mail_server_ids[0].id)
        return True


class eleverappel(models.Model):
    _name = 'eleve.rappel'
    _description = "eleve.rappel"

    @api.model
    def check_user(self):
        '''Method to get default value of logged in eleve'''
        return self.env['eleve.eleve'].search([('user_id', '=',
                                                    self._uid)]).id

    ele_id = fields.Many2one('eleve.eleve', 'nom eleve', required=True,
                             default=check_user)
    nom = fields.Char('Titre')
    date = fields.Date('Date')
    description = fields.Text('Description')
    couleur = fields.Integer('couleur Index', default=0)


class eleveCaste(models.Model):
    _name = "eleve.caste"
    _description = "eleve.caste"

    nom = fields.Char("Nom", required=True)


class SalleClasse(models.Model):
    _name = "salle.classe"
    _description = "Salle Classe"

    nom = fields.Char("nom")
    number = fields.Char("Numéro salle")


class Report(models.Model):
    _inherit = "ir.actions.report"

    @api.multi
    def render_template(self, template, values=None):
        eleve_id = self.env['eleve.eleve'].\
            browse(self._context.get('eleve_id', False))
        if eleve_id and eleve_id.etat == 'Brouillon':
            raise ValidationError(_('''You cannot print report for
                eleve in unconfirm etat!'''))
        return super(Report, self).render_template(template, values)
