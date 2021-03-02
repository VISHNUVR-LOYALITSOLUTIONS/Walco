# -*- coding: utf-8 -*-
# from odoo import http


# class StockDate(http.Controller):
#     @http.route('/stock_date/stock_date/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_date/stock_date/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_date.listing', {
#             'root': '/stock_date/stock_date',
#             'objects': http.request.env['stock_date.stock_date'].search([]),
#         })

#     @http.route('/stock_date/stock_date/objects/<model("stock_date.stock_date"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_date.object', {
#             'object': obj
#         })
