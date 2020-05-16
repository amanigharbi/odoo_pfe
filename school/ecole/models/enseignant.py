# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class Ecoleenseignant(models.Model):
    ''' Defining a enseignant information '''
    _name = 'ecole.enseignant'
    _description = 'enseignant Information'

    employee_id = fields.Many2one('hr.employee', 'Employee ID',
                                  ondelete="cascade",
                                  delegate=True, required=True)
    classe_id = fields.Many2one('ecole.classe',
                                  "Responsable de la classe  Scolaire",
                                  help="classe for which the enseignant\
                                  responsible for.")
    stand_id = fields.Many2one('classe.classe', "Course",
                               related="classe_id.classe_id", store=True)
    matiere_id = fields.Many2many('matiere.matiere', 'matiere_enseignant_rel',
                                  'enseignant_id', 'matiere_id',
                                  'Cours')
    ecole_id = fields.Many2one('ecole.ecole', "Ecole",
                                related="classe_id.ecole_id", store=True)
    categorie_ids = fields.Many2many('hr.employee.category',
                                    'employee_category_rel', 'emp_id',
                                    'category_id', 'Tags')
    department_id = fields.Many2one('hr.department', 'Department')
    est_parent = fields.Boolean('Est Directeur')
    stu_parent_id = fields.Many2one('ecole.parent', 'Related Parent')
    eleve_id = fields.Many2many('eleve.eleve',
                                  'eleves_enseignants_parent_rel',
                                  'enseignant_id', 'eleve_id',
                                  'Children')
    numero_telephone = fields.Char("Numéro Télételephone")

    @api.onchange('est_parent')
    def _onchange_isparent(self):
        if self.est_parent:
            self.stu_parent_id = False
            self.eleve_id = [(6, 0, [])]

    @api.onchange('stu_parent_id')
    def _onchangeeleve_parent(self):
        stud_list = []
        if self.stu_parent_id and self.stu_parent_id.eleve_id:
            for eleve in self.stu_parent_id.eleve_id:
                stud_list.append(eleve.id)
            self.eleve_id = [(6, 0, stud_list)]

    @api.model
    def create(self, vals):
        enseignant_id = super(Ecoleenseignant, self).create(vals)
        user_obj = self.env['res.users']
        user_vals = {'nom': enseignant_id.nom,
                     'login': enseignant_id.email_travail,
                     'email': enseignant_id.email_travail,
                     }
        ctx_vals = {'enseignant_create': True,
                    'ecole_id': enseignant_id.ecole_id.company_id.id}
        user_id = user_obj.with_context(ctx_vals).create(user_vals)
        enseignant_id.employee_id.write({'user_id': user_id.id})
        if vals.get('est_parent'):
            self.parent_crt(enseignant_id)
        return enseignant_id

    @api.multi
    def parent_crt(self, manager_id):
        stu_parent = []
        if manager_id.stu_parent_id:
            stu_parent = manager_id.stu_parent_id
        if not stu_parent:
            emp_user = manager_id.employee_id
            eleves = [stu.id for stu in manager_id.eleve_id]
            parent_vals = {'nom': manager_id.nom,
                           'email': emp_user.email_travail,
                           'parent_create_mng': 'parent',
                           'user_ids': [(6, 0, [emp_user.user_id.id])],
                           'partner_id': emp_user.user_id.partner_id.id,
                           'eleve_id': [(6, 0, eleves)]}
            stu_parent = self.env['ecole.parent'].create(parent_vals)
            manager_id.write({'stu_parent_id': stu_parent.id})
        user = stu_parent.user_ids
        user_rec = user[0]
        parent_grp_id = self.env.ref('ecole.group_ecole_parent')
        groups = parent_grp_id
        if user_rec.groups_id:
            groups = user_rec.groups_id
            groups += parent_grp_id
        group_ids = [group.id for group in groups]
        user_rec.write({'groups_id': [(6, 0, group_ids)]})

    @api.multi
    def write(self, vals):
        if vals.get('est_parent'):
            self.parent_crt(self)
        if vals.get('eleve_id'):
            self.stu_parent_id.write({'eleve_id': vals.get('eleve_id')})
        if not vals.get('est_parent'):
            user_rec = self.employee_id.user_id
            ir_obj = self.env['ir.model.data']
            parent_grp_id = ir_obj.get_object('ecole', 'group_ecole_parent')
            groups = parent_grp_id
            if user_rec.groups_id:
                groups = user_rec.groups_id
                groups -= parent_grp_id
            group_ids = [group.id for group in groups]
            user_rec.write({'groups_id': [(6, 0, group_ids)]})
        return super(Ecoleenseignant, self).write(vals)

    @api.onchange('address_id')
    def onchange_address_id(self):
        self.telephone_travail = False
        self.telephone_portable = False
        if self.address_id:
            self.telephone_travail = self.address_id.telephone,
            self.telephone_portable = self.address_id.mobile

    @api.onchange('department_id')
    def onchange_department_id(self):
        if self.department_id:
            self.parent_id = (self.department_id and
                              self.department_id.manager_id and
                              self.department_id.manager_id.id) or False

    @api.onchange('user_id')
    def onchange_user(self):
        if self.user_id:
            self.nom = self.nom or self.user_id.nom
            self.email_travail = self.user_id.email
            self.image = self.image or self.user_id.image

    @api.onchange('ecole_id')
    def onchange_ecole(self):
        self.address_id = False
        self.telephone_portable = False
        self.lieu_travail = False
        self.email_travail = False
        self.telephone_travail = False
        if self.ecole_id:
            self.address_id = self.ecole_id.company_id.partner_id.id
            self.telephone_portable = self.ecole_id.company_id.partner_id.mobile
            self.lieu_travail = self.ecole_id.company_id.partner_id.ville
            self.email_travail = self.ecole_id.company_id.partner_id.email
            telephone = self.ecole_id.company_id.partner_id.telephone
            self.telephone_travail = telephone
            self.numero_telephone = telephone
            telephone = self.ecole_id.company_id.partner_id.telephone