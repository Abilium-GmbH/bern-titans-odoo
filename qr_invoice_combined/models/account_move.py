# -*- coding: utf-8 -*-
from odoo import models
from odoo.tools import pdf
from base64 import b64encode
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_print_merged_qr_report(self):
        self.ensure_one()
        pdfs = []

        inv_print_name = self._get_report_base_filename()
        inv_pdf = self.env.ref('account.account_invoices')._render_qweb_pdf(self.ids)[0]
        pdfs.append(inv_pdf)

        self.partner_bank_id = self.env.company.partner_id.bank_ids[0]

        if self.move_type == 'out_invoice' \
            and self.partner_bank_id \
            and self.partner_bank_id._eligible_for_qr_code('ch_qr', self.partner_id, self.currency_id):
            qr_pdf = self.env.ref('l10n_ch.l10n_ch_qr_report')._render_qweb_pdf(self.ids)[0]
            pdfs.append(qr_pdf)
            _logger.info("added qr pdf")

        merged_pdf = pdf.merge_pdf(pdfs)

        pdf_attachment = self.env['ir.attachment'].create({
            'name': inv_print_name + '.pdf',
            'datas': b64encode(merged_pdf),
            'type': 'binary',
            'res_model': 'account.move',
            'res_id': self.id
        })

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % pdf_attachment.id,
            'target': 'self',
        }
