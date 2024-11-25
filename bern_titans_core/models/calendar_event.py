from odoo import api, fields, _, models
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)

class Meeting(models.Model):
    _inherit = "calendar.event"

    partner_answers = fields.One2many('partner.answer', 'calendar_event', string="Mitgliederantworten")
    attendees_count = fields.Integer(string="Teilnehmer", compute="_compute_attendees", store=True)
    group_ids = fields.Many2many('partner.group', relation='partner_group_calendar_event_rel',
                                 column1='calendar_event_id',
                                 column2='partner_group_id',
                                 string='Groups')

    @api.depends('partner_answers')
    def _compute_attendees(self):
        for record in self:
            record.attendees_count = len(record.partner_answers.filtered(lambda l: l.answer == 'yes'))

    @api.model
    def _get_google_synced_fields(self):
        fields = super(Meeting, self)._get_google_synced_fields()
        return fields.union({'colorId'})

    @api.model
    def _odoo_values(self, ge, default_reminders=()):
        values = super(Meeting, self)._odoo_values(ge, default_reminders)
        general_id = self.env.ref('google_multi_calendar.group_id_bern_titans').id
        calendar = self.env['partner.group'].search([('color_id', '=', ge.colorId)])
        if calendar:
            values['group_ids'] = [(5, 0, 0), (4, calendar.mapped('id')[0])]
        else:
            values['group_ids'] = [(5, 0, 0), (4, general_id)]
        #_logger.info(values)
        return values

class ResPartner(models.Model):
    _inherit = 'res.partner'

    answers = fields.One2many('partner.answer', 'calendar_event', string="Antworten")


class PartnerAnswer(models.Model):
    _name = 'partner.answer'
    _description = 'Spielerantwort'

    name = fields.Char(string='Bezeichnung')
    partner_id = fields.Many2one('res.partner', string='Mitglied')
    calendar_event = fields.Many2one('calendar.event', string="Event")
    answer = fields.Char(string='Antwort', default=None)

    def do_participate(self):
        return self.write({'answer': 'yes'})

    def do_decline(self):
        return self.write({'answer': 'no'})

    def do_unknown(self):
        return self.write({'answer': None})

    def write(self, values):
        val = super(PartnerAnswer, self).write(values)
        for record in self:
            record.sudo().calendar_event._compute_attendees()
        return val
