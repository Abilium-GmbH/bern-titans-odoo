from odoo import api, fields, _, models
from datetime import timedelta, date

class ResPartner(models.Model):
    _inherit = 'res.partner'

    birthday = fields.Datetime(string='Geburtstag')
    gender = fields.Selection([('male', 'männlich'),
                               ('female', 'weiblich'),
                               ('divers', 'divers')], string="Geschlecht")
    adult = fields.Boolean(string='volljährig', default=True, compute='_compute_adult', store=True)

    member_status = fields.Selection([('active', 'Aktivmitglied'),
                                      ('passive', 'Passivmitglied')], string="Mitgliedstatus")
    position = fields.Selection([('attack', 'Attack'),
                                 ('middie', 'Middie'),
                                 ('goalie', 'Goalie'),
                                 ('middie_d', 'Middie D'),
                                 ('middie_a', 'Middie A'),
                                 ('defense', 'Defense'),
                                 ('d_coach', 'D-Coach')], string="Position")
    trikot_num = fields.Integer(string='Trikotnummer')
    trikot_name = fields.Char(string='Trikotname')
    licenced = fields.Boolean(string='Lizenziert', default=False)

    entry_date = fields.Datetime(string='Eintritt')
    exit_date = fields.Datetime(string='Austritt')
    ref_licence = fields.Many2one('ref.licence', string="Schirilizenz")
    scout = fields.Many2one('res.partner', string='Scout')
    scouted_by = fields.One2many('res.partner', 'scout')
    infoletter = fields.Char(string='Infoletter')
    nationality = fields.Many2one('res.country', string="Nationalität")

    partner_group_ids = fields.Many2many(
        'partner.group',
        relation='res_partner_group_rel',
        column1='res_partner_id',
        column2='partner_group_id',
        string='Gruppen'
    )

    @api.depends('birthday')
    def _compute_adult(self):
        for record in self:
            if record.birthday:
                today = date.today()
                age = today.year - record.birthday.year - ((today.month, today.day) < (record.birthday.month, record.birthday.day))
                if age >= 18:
                    record.adult = True
            record.adult = False


class RefLicence(models.Model):
    _name = 'ref.licence'
    _description = 'Schirilizenz'

    name = fields.Char(string='Bezeichnung')
    partner_ids = fields.One2many('res.partner', 'ref_licence', string='Mitglieder')


class PartnerGroup(models.Model):
    _name = 'partner.group'
    _description = 'Team groups'

    name = fields.Char(string='Gruppenname')
    color_id = fields.Char(string="Google Color Id", store=True)
    color_name = fields.Char(string="Google Color Name", store=True)
    partner_id_count = fields.Integer(compute='_compute_partner_id_count')

    def _compute_partner_id_count(self):
        for record in self:
            record.partner_id_count = len(record.partner_ids)

    partner_ids = fields.Many2many(
        'res.partner',
        relation='res_partner_group_rel',
        string='Mitglieder'
    )
    calendar_events = fields.Many2many('calendar.event', relation='partner_group_calendar_event_rel', string="Events")
