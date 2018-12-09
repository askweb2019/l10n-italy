# -*- coding: utf-8 -*-
#
# Copyright 2014    - Davide Corio <davide.corio@abstract.it>
# Copyright 2018-19 - Odoo Italia Associazione <https://www.odoo-italia.org>
# Copyright 2018-19 - SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
#
from odoo import api, fields, models
import odoo.addons.decimal_precision as dp

RELATED_DOCUMENT_TYPES = {
    'order': 'DatiOrdineAcquisto',
    'contract': 'DatiContratto',
    'agreement': 'DatiConvenzione',
    'reception': 'DatiRicezione',
    'invoice': 'DatiFattureCollegate',
}
# TODO: Use module for classification
EU_COUNTRIES = ['AT', 'BE', 'BG', 'CY', 'HR', 'DK', 'EE',
                'FI', 'FR', 'DE', 'GR', 'IE', 'IT', 'LV',
                'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'GB',
                'CZ', 'RO', 'SK', 'SI', 'ES', 'SE', 'HU']


class FatturapaFormat(models.Model):
    # _position = ['1.1.3']
    _name = "fatturapa.format"
    _description = 'E-invoice Format'

    name = fields.Char('Description', size=128)
    code = fields.Char('Code', size=5)

#  used in fatturaPa import
class FatturapaPaymentData(models.Model):
    # _position = ['2.4.2.2']
    _name = "fatturapa.payment.data"
    _description = 'E-invoice Payment Data'

    #  2.4.1
    payment_terms = fields.Many2one(
        'fatturapa.payment_term', string="Electronic Invoice Payment Method")
    #  2.4.2
    payment_methods = fields.One2many(
        'fatturapa.payment.detail', 'payment_data_id',
        'Payments Details')
    invoice_id = fields.Many2one(
        'account.invoice', 'Related Invoice',
        ondelete='cascade', index=True)


class FatturapaPaymentDetail(models.Model):
    # _position = ['2.4.2']
    _name = "fatturapa.payment.detail"
    recipient = fields.Char('Recipient', size=200)
    fatturapa_pm_id = fields.Many2one(
        'fatturapa.payment_method', string="Electronic Invoice Payment Method"
    )
    payment_term_start = fields.Date('Payment Term Start')
    payment_days = fields.Integer('Payment Term Days')
    payment_due_date = fields.Date('Payment Due Date')
    payment_amount = fields.Float('Payment Amount')
    post_office_code = fields.Char('Post Office Code', size=20)
    recepit_name = fields.Char("Recepit Partner Firstname")
    recepit_surname = fields.Char("Recepit Partner Lastname")
    recepit_cf = fields.Char("Recepit Partner Fiscalnumber")
    recepit_title = fields.Char("Recepit Partner Title")
    payment_bank_name = fields.Char("Bank Name")
    payment_bank_iban = fields.Char("IBAN")
    payment_bank_abi = fields.Char("ABI")
    payment_bank_cab = fields.Char("CAB")
    payment_bank_bic = fields.Char("BIC")
    payment_bank = fields.Many2one(
        'res.partner.bank', string="Payment Bank")
    prepayment_discount = fields.Float('Prepayment Discount')
    max_payment_date = fields.Date('Maximum Date for Payment')
    penalty_amount = fields.Float('Amount of Penalty')
    penalty_date = fields.Date('Effective Date of Penalty')
    payment_code = fields.Char('Payment Code')
    account_move_line_id = fields.Many2one(
        'account.move.line', string="Payment Line")
    payment_data_id = fields.Many2one(
        'fatturapa.payment.data', 'Related Payments Data',
        ondelete='cascade', index=True)


class FatturapaFiscalPosition(models.Model):
    # _position = ['2.1.1.7.7', '2.2.1.14']
    _name = "fatturapa.fiscal_position"
    _description = 'Electronic Invoice Fiscal Position'

    name = fields.Char('Description', size=128)
    code = fields.Char('Code', size=4)


class WelfareFundType(models.Model):
    # _position = ['2.1.1.7.1']
    _name = "welfare.fund.type"
    _description = 'Welfare Fund Type'

    name = fields.Char('Name')
    description = fields.Char('Description')


class WelfareFundDataLine(models.Model):
    # _position = ['2.1.1.7']
    _name = "welfare.fund.data.line"
    _description = 'E-invoice Welfare Fund Data'

    name = fields.Many2one(
        'welfare.fund.type', string="Welfare Fund Type")
    tax_nature_id = fields.Many2one('italy.ade.tax.nature',
                                    string="No taxable nature")
    welfare_rate_tax = fields.Float('Welfare Tax Rate')
    welfare_amount_tax = fields.Float('Welfare Tax Amount')
    welfare_taxable = fields.Float('Welfare Taxable')
    welfare_Iva_tax = fields.Float('VAT Tax Rate')
    subjected_withholding = fields.Char(
        'Subjected to Withholding', size=2)
    pa_line_code = fields.Char('PA Code for this Record', size=20)
    invoice_id = fields.Many2one(
        'account.invoice', 'Related Invoice',
        ondelete='cascade', index=True
    )


class DiscountRisePrice(models.Model):
    # _position = ['2.1.1.8', '2.2.1.10']
    _name = "discount.rise.price"
    _description = 'E-invoice Discount Supplement Data'

    name = fields.Selection(
        [('SC', 'Discount'), ('MG', 'Supplement')], 'Type')
    percentage = fields.Float('Percentage')
    amount = fields.Float('Amount', digits=dp.get_precision('Discount'))
    invoice_line_id = fields.Many2one(
        'account.invoice.line', 'Related Invoice',
        ondelete='cascade', index=True
    )
    invoice_id = fields.Many2one(
        'account.invoice', 'Related Invoice',
        ondelete='cascade', index=True
    )


class FatturapaRelatedDocumentType(models.Model):
    # _position = ['2.1.2', '2.2.3', '2.1.4', '2.1.5', '2.1.6']
    _name = 'fatturapa.related_document_type'
    _description = 'E-invoice Related Document Type'

    type = fields.Selection(
        [
            ('order', 'Order'),
            ('contract', 'Contract'),
            ('agreement', 'Agreement'),
            ('reception', 'Reception'),
            ('invoice', 'Related Invoice')
        ],
        'Document Type', required=True
    )
    name = fields.Char('Document ID', size=20, required=True)
    lineRef = fields.Integer('Line Ref.')
    invoice_line_id = fields.Many2one(
        'account.invoice.line', 'Related Invoice Line',
        ondelete='cascade', index=True)
    invoice_id = fields.Many2one(
        'account.invoice', 'Related Invoice',
        ondelete='cascade', index=True)
    date = fields.Date('Date')
    numitem = fields.Char('Item Num.', size=20)
    code = fields.Char('Order Agreement Code', size=100)
    cig = fields.Char('CIG Code', size=15)
    cup = fields.Char('CUP Code', size=15)

    @api.model
    def create(self, vals):
        if vals.get('invoice_line_id'):
            line_obj = self.env['account.invoice.line']
            line = line_obj.browse(vals['invoice_line_id'])
            vals['lineRef'] = line.sequence
        return super(FatturapaRelatedDocumentType,
                     self).create(vals)


class FaturapaActivityProgress(models.Model):
    # _position = ['2.1.7']
    _name = "faturapa.activity.progress"

    fatturapa_activity_progress = fields.Integer('Activity Progress')
    invoice_id = fields.Many2one(
        'account.invoice', 'Related Invoice',
        ondelete='cascade', index=True)


class FatturaAttachments(models.Model):
    # _position = ['2.5']
    _name = "fatturapa.attachments"
    _description = "E-invoice attachments"
    _inherits = {'ir.attachment': 'ir_attachment_id'}

    ir_attachment_id = fields.Many2one(
        'ir.attachment', 'Attachment', required=True, ondelete="cascade")
    compression = fields.Char('Compression', size=10)
    format = fields.Char('Format', size=10)
    invoice_id = fields.Many2one(
        'account.invoice', 'Related Invoice',
        ondelete='cascade', index=True)


class FatturapaRelatedDdt(models.Model):
    # _position = ['2.1.2', '2.2.3', '2.1.4', '2.1.5', '2.1.6']
    _name = 'fatturapa.related_ddt'
    _description = 'E-invoice Related DDT'

    name = fields.Char('Document ID', size=20, required=True)
    date = fields.Date('Date')
    lineRef = fields.Integer('Line Ref.')
    invoice_line_id = fields.Many2one(
        'account.invoice.line', 'Related Invoice Line',
        ondelete='cascade', index=True)
    invoice_id = fields.Many2one(
        'account.invoice', 'Related Invoice',
        ondelete='cascade', index=True)

    @api.model
    def create(self, vals):
        if vals.get('invoice_line_id'):
            line_obj = self.env['account.invoice.line']
            line = line_obj.browse(vals['invoice_line_id'])
            vals['lineRef'] = line.sequence
        return super(FatturapaRelatedDdt,
                     self).create(vals)


class AccountInvoiceLine(models.Model):
    # _position = ['2.2.1']
    _inherit = "account.invoice.line"

    related_documents = fields.One2many(
        'fatturapa.related_document_type', 'invoice_line_id',
        'Related Documents Type', copy=False
    )
    ftpa_related_ddts = fields.One2many(
        'fatturapa.related_ddt', 'invoice_line_id',
        'Related DdT', copy=False
    )
    admin_ref = fields.Char('Administration ref.', size=20, copy=False)
    discount_rise_price_ids = fields.One2many(
        'discount.rise.price', 'invoice_line_id',
        'Discount or Supplement Details', copy=False
    )
    ftpa_line_number = fields.Integer("Line Number", readonly=True, copy=False)


class FaturapaSummaryData(models.Model):
    # _position = ['2.2.2']
    _name = "faturapa.summary.data"
    tax_rate = fields.Float('Tax Rate')
    non_taxable_nature = fields.Many2one(
        'italy.ade.tax.nature',
        string="No taxable nature")
    incidental_charges = fields.Float('Incidental Charges')
    rounding = fields.Float('Rounding')
    amount_untaxed = fields.Float('Amount Untaxed')
    amount_tax = fields.Float('Amount Tax')
    payability = fields.Selection([
        ('I', 'Immediate payability'),
        ('D', 'Deferred payability'),
        ('S', 'Split payment'),
    ], string="VAT payability")
    law_reference = fields.Char(
        'Law reference', size=128)
    invoice_id = fields.Many2one(
        'account.invoice', 'Related Invoice',
        ondelete='cascade', index=True)


class AccountInvoice(models.Model):
    # _position = ['2.1', '2.2', '2.3', '2.4', '2.5']
    _inherit = "account.invoice"
    protocol_number = fields.Char('Protocol Number', size=64, copy=False)
    # 1.2 -- partner_id
    # 1.3
    tax_representative_id = fields.Many2one(
        'res.partner', string="Tax Representative")
    #  1.4 company_id
    #  1.5
    intermediary = fields.Many2one(
        'res.partner', string="Intermediary")
    #  1.6
    sender = fields.Selection(
        [('CC', 'Assignee / Partner'),
         ('TZ', 'Third Person')], 'Sender')
    # 2.1.1.1 FIXME doc_type
    invoice_type_id = fields.Many2one(
        'italy.ade.invoice.type', string="Document Type",)
    #  2.1.1.5
    #  2.1.1.5.1
    ftpa_withholding_type = fields.Selection(
        [('RT01', 'Natural Person'),
         ('RT02', 'Legal Person')],
        'Withholding Type'
    )
    #  2.1.1.5.2 withholding_amount in module
    #  2.1.1.5.3
    ftpa_withholding_rate = fields.Float('Withholding rate')
    #  2.1.1.5.4
    ftpa_withholding_payment_reason = fields.Char(
        'Withholding reason', size=2)
    #  2.1.1.6
    virtual_stamp = fields.Boolean('Virtual Stamp', default=False, copy=False)
    stamp_amount = fields.Float('Stamp Amount', copy=False)
    #  2.1.1.7
    welfare_fund_ids = fields.One2many(
        'welfare.fund.data.line', 'invoice_id',
        'Welfare Fund', copy=False
    )
    #  2.1.2 - 2.1.6
    related_documents = fields.One2many(
        'fatturapa.related_document_type', 'invoice_id',
        'Related Documents', copy=False
    )
    #  2.1.7
    activity_progress_ids = fields.One2many(
        'faturapa.activity.progress', 'invoice_id',
        'Phase of Activity Progress', copy=False
    )
    #  2.1.8
    ftpa_related_ddts = fields.One2many(
        'fatturapa.related_ddt', 'invoice_id',
        'Related DdT', copy=False
    )
    #  2.1.9
    carrier_id = fields.Many2one(
        'res.partner', string="Carrier", copy=False)
    transport_vehicle = fields.Char('Vehicle', size=80, copy=False)
    transport_reason = fields.Char('Reason', size=80, copy=False)
    number_items = fields.Integer('Number of Items', copy=False)
    description = fields.Char('Description', size=100, copy=False)
    unit_weight = fields.Char('Weight Unit', size=10, copy=False)
    gross_weight = fields.Float('Gross Weight', copy=False)
    net_weight = fields.Float('Net Weight', copy=False)
    pickup_datetime = fields.Datetime('Pick up', copy=False)
    transport_date = fields.Date('Transport Date', copy=False)
    delivery_address = fields.Text('Delivery Address', copy=False)
    delivery_datetime = fields.Datetime('Delivery Date Time', copy=False)
    ftpa_incoterms = fields.Char(string="Incoterms", copy=False)
    #  2.1.10
    related_invoice_code = fields.Char('Related Invoice Code', copy=False)
    related_invoice_date = fields.Date('Related Invoice Date', copy=False)
    #  2.2.1 invoice lines
    #  2.2.2
    fatturapa_summary_ids = fields.One2many(
        'faturapa.summary.data', 'invoice_id',
        'Electronic Invoice Summary Data', copy=False
    )
    #  2.3
    vehicle_registration = fields.Date('Vehicle Registration', copy=False)
    total_travel = fields.Char('Travel in hours or Km', size=15, copy=False)
    #  2.4
    fatturapa_payments = fields.One2many(
        'fatturapa.payment.data', 'invoice_id',
        'Electronic Invoice Payment Data', copy=False
    )
    #  2.5
    fatturapa_doc_attachments = fields.One2many(
        'fatturapa.attachments', 'invoice_id',
        'Electronic Invoice Attachments', copy=False
    )
    # 1.2.3
    efatt_stabile_organizzazione_indirizzo = fields.Char(
        string="Organization Address",
        help="The fields must be entered only when the seller/provider is "
             "non-resident, with a stable organization in Italy. Address of "
             "the stable organization in Italy (street name, square, etc.)",
        readonly=True, copy=False)
    efatt_stabile_organizzazione_civico = fields.Char(
        string="Organization Street Number",
        help="Street number of the address (no need to specify if already "
             "present in the address field)",
        readonly=True, copy=False)
    efatt_stabile_organizzazione_cap = fields.Char(
        string="Organization ZIP",
        help="ZIP Code",
        readonly=True, copy=False)
    efatt_stabile_organizzazione_comune = fields.Char(
        string="Organization Municipality",
        help="Municipality or city to which the Stable Organization refers",
        readonly=True, copy=False)
    efatt_stabile_organizzazione_provincia = fields.Char(
        string="Organization Province",
        help="Acronym of the Province to which the municipality indicated "
             "in the information element 1.2.3.4 <Comune> belongs. "
             "Must be filled if the information element 1.2.3.6 <Nazione> is "
             "equal to IT",
        readonly=True, copy=False)
    efatt_stabile_organizzazione_nazione = fields.Char(
        string="Organization Country",
        help="Country code according to the ISO 3166-1 alpha-2 code standard",
        readonly=True, copy=False)
    # 2.1.1.10
    efatt_rounding = fields.Float(
        "Rounding", readonly=True,
        help="Possible total amount rounding on the document (negative sign "
             "allowed)", copy=False
    )
    art73 = fields.Boolean(
        'Art. 73', readonly=True,
        help="Indicates whether the document has been issued according to "
             "methods and terms laid down in a ministerial decree under the "
             "terms of Article 73 of Italian Presidential Decree 633/72 (this "
             "enables the seller/provider to issue in the same year several "
             "documents with same number)", copy=False)

    @api.model
    def default_get(self, fields):
        res = super(AccountInvoice, self).default_get(fields)
        if 'type' in res:
            einv_type_model = self.env['italy.ade.invoice.type']
            ids = einv_type_model.search(
                [('scope', 'like', res['type'])], order='code')
            if ids:
                res.update({'invoice_type_id': ids[0].id})
        return res

    @api.one
    def set_default_einvoice_type(self):
        if not self.invoice_type_id:
            einv_type_model = self.env['italy.ade.invoice.type']
            scope = 'XX%'
            if self.partner.country_id:
                if self.partner.country_id.code == 'IT':
                    scope = 'IT%'
                elif self.partner.country_id.code in EU_COUNTRIES:
                    scope = 'EU%'
            if self.amount >= 0:
                scope += self.type
            else:
                scope += self.type[0].upper() + self.type[1:]
            ids = einv_type_model.search(
                [('scope', 'like', scope)], order='code')
            if ids:
                return ids[0].id
        return False
