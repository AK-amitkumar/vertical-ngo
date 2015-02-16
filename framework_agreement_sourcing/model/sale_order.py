# -*- coding: utf-8 -*-
##############################################################################
#
#    Authors: Nicolas Bessi, Yannick Vaucher
#    Copyright 2013-2015 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, api, exceptions, _, netsvc
from openerp.osv import orm


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_accepted(self):
        """ On acceptation of Cost Estimate, we generate PO
        for all line sourced by a framework agreement

        Framework agreement currency is selected this way:

        - Currency matching with Cost Estimate currency.
        - Or first currency found on framework agreement.

        """
        res = super(SaleOrder, self).action_accepted()
        fa_so_lines = self.mapped('order_line').filtered(
            lambda rec: (rec.sourcing_method == 'fw_agreement' and
                         not rec.sourced_by))
        for line in fa_so_lines:
            source = line.lr_source_id
            # If no po has been generated yet
            if not source.purchase_line_id:
                line._make_source_fa_purchase_order()
            line.sourced_by = source.purchase_line_id
        return res


class sale_order_line(orm.Model):

    """Pass agreement PO into state confirmed when SO is confirmed"""

    _inherit = "sale.order.line"

    @api.multi
    def _make_source_fa_purchase_order(self):
        source = self.lr_source_id
        pricelist = self.order_id.pricelist_id
        order_currency = pricelist.currency_id
        fa_currencies = (source
                         .framework_agreement_id
                         .framework_agreement_pricelist_ids
                         .mapped('currency_id'))
        if not fa_currencies:
            raise exceptions.Warning(
                _('No currency found for Framework agreement %s')
                % source.framework_agreement_id)
        if order_currency not in fa_currencies:
            currency = fa_currencies[0]

            pricelist = self.env['product.pricelist'].search(
                [('currency_id', '=', currency.id),
                 ('type', '=', 'purchase')],
                limit=1)

        source.make_purchase_order(pricelist)

    def button_confirm(self, cr, uid, ids, context=None):
        """Override confirmation of request of quotation to support LTA

        Related PO generated by agreement source line will be passed to state
        draft_po.

        """
        POL = self.pool['purchase.order.line']
        LRL = self.pool['logistic.requisition.line']
        wf_service = netsvc.LocalService("workflow")

        def source_valid(source):
            if source and source.sourcing_method == 'fw_agreement':
                return True
            return False

        result = super(sale_order_line, self).button_confirm(cr, uid, ids,
                                                             context=context)

        order_lines = self.browse(cr, uid, ids, context=context)

        so_ids = list(set((l.order_id.id for l in order_lines)))

        lrl_ids = LRL.search(cr, uid, [
            ('cost_estimate_id', 'in', so_ids)
        ], context=context)

        sources = []

        for lrl in LRL.browse(cr, uid, lrl_ids, context=context):
            for lrs in lrl.source_ids:
                sources.append(lrs)

        source_ids = [source.id for source in sources if source_valid(source)]

        po_line_ids = POL.search(cr, uid, [
            ('lr_source_line_id', 'in', source_ids)
        ], context=context)

        po_lines = POL.browse(cr, uid, po_line_ids, context=context)

        po_ids = list(set((l.order_id.id for l in po_lines)))

        for po_id in po_ids:
            wf_service.trg_validate(uid, 'purchase.order', po_id,
                                    'draft_po', cr)
        return result
