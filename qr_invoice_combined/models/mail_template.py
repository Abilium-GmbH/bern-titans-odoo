# -*- coding: utf-8 -*-
from odoo import models
from odoo.tools import pdf
from base64 import b64decode, b64encode
import logging

_logger = logging.getLogger(__name__)


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    def generate_email(self, res_ids, fields):
        result = super().generate_email(res_ids, fields)

        _logger.info("in qr combined")

        if self.model != 'account.move':
            return result

        multi_mode = True
        if isinstance(res_ids, int):
            res_ids = [res_ids]
            multi_mode = False

        if self.model == 'account.move':
            _logger.info("in qr combined 2")
            for record in self.env[self.model].browse(res_ids):
                record_dict = multi_mode and result[record.id] or result
                attachments_list = record_dict.get('attachments', [])

                record.partner_bank_id = self.env.company.partner_id.bank_ids[0]

                _logger.info("%s %s %s" % (record.move_type, record.partner_bank_id, record.partner_bank_id._eligible_for_qr_code('ch_qr', record.partner_id, record.currency_id)))
                if record.move_type == 'out_invoice' \
                        and record.partner_bank_id \
                        and record.partner_bank_id._eligible_for_qr_code('ch_qr', record.partner_id, record.currency_id):
                    qr_pdf = self.env.ref('l10n_ch.l10n_ch_qr_report')._render_qweb_pdf(record.ids)[0]
                    qr_pdf = b64encode(qr_pdf)
                    attachments_list.append(('qr-invoice.pdf', qr_pdf))
                    _logger.info("adding qr pdf")
                    # pdf_attachment = self.env['ir.attachment'].create({
                    #     'name': 'qrinvoice' + '.pdf',
                    #     'datas': b64encode(qr_pdf),
                    #     'type': 'binary',
                    #     'res_model': 'account.move',
                    #     'res_id': record.id
                    # })
                _logger.info(list(map(lambda l: l[0], attachments_list)))
                if len(attachments_list) > 2:
                    attachments_list = attachments_list[:-1]
                if len(attachments_list) > 0:
                    merged_pdf = pdf.merge_pdf([b64decode(_pdf) for name, _pdf in attachments_list])
                    record_dict['attachments'] = [(attachments_list[0][0], b64encode(merged_pdf))]

        return result
    #
    # def generate_email(self, res_ids, fields):
    #     res = super().generate_email(res_ids, fields)
    #
    #     multi_mode = True
    #     if isinstance(res_ids, int):
    #         res_ids = [res_ids]
    #         multi_mode = False
    #
    #     if self.model not in ['account.move', 'account.payment']:
    #         return res
    #
    #     records = self.env[self.model].browse(res_ids)
    #     for record in records:
    #         record_data = (res[record.id] if multi_mode else res)
    #         for doc in record.edi_document_ids:
    #             record_data.setdefault('attachments', [])
    #             attachments = self._get_edi_attachments(doc)
    #             record_data['attachment_ids'] += attachments.get('attachment_ids', [])
    #             record_data['attachments'] += attachments.get('attachments', [])
    #
    #     return res