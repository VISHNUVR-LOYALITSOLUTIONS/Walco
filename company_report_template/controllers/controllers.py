# -*- coding: utf-8 -*-
import base64
from collections import OrderedDict
import datetime

from odoo import http
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.tools.translate import _
from odoo.addons.portal.controllers.portal import pager as portal_pager, CustomerPortal, get_records_pager
from odoo.addons.web.controllers.main import Binary



class CustomerPortal(CustomerPortal):

    # @http.route(['/my/orders/<int:order_id>/accept'], type='json', auth="public", website=True)
    # def portal_quote_accept(self, order_id, access_token=None, name=None, signature=None):
    #     values = super(CustomerPortal, self).portal_quote_accept(order_id, access_token, name, signature)
    #     return values
    @http.route(['/my/orders/<int:order_id>'], type='http', auth="public", website=True)
    def portal_order_page(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw):
        values = super(CustomerPortal, self).portal_order_page(order_id, report_type, access_token, message, download)
        try:
            order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            if order_sudo.company_id:
                if order_sudo.company_id.sale_reports == 'walcotech':
                    pdf = 'sale_order_print.walcotech_sale_order_print'
                elif order_sudo.company_id.sale_reports == 'walco':
                    pdf = 'sale_order_print.walco_sale_order_print'
                elif order_sudo.company_id.sale_reports == 'texerv':
                    pdf = 'sale_order_print.texerv_sale_order_print'
                elif order_sudo.company_id.sale_reports == 'odoo_standard':
                    pdf = 'sale.action_report_saleorder'
                return self._show_report(model=order_sudo, report_type=report_type, report_ref=pdf, download=download)
        return values
