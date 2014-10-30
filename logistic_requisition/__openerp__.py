# -*- coding: utf-8 -*-
#
#
#    Author: Joël Grand-Guillaume, Jacques-Etienne Baudoux, Guewen Baconnier
#    Copyright 2013-2014 Camptocamp SA
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
#

{"name": "Logistic Requisition",
 "version": "1.0",
 "author": "Camptocamp",
 "license": "AGPL-3",
 "category": "Purchase Management",
 'complexity': "normal",
 "images": [],
 "website": "http://www.camptocamp.com",
 "depends": ["sale_sourced_by_line",
             "stock_dropshipping",
             "purchase",
             "purchase_requisition_bid_selection",
             "mail",
             "logistic_order",
             "transport_information",
             "purchase_requisition_transport_document",
             ],
 "demo": ['data/logistic_requisition_demo.xml'],
 "data": ["wizard/logistic_line_create_requisition_view.xml",
          "wizard/assign_line_view.xml",
          "wizard/cost_estimate_view.xml",
          "wizard/logistic_requisition_cancel_view.xml",
          "security/logistic_requisition.xml",
          "security/ir.model.access.csv",
          "data/logistic_requisition_data.xml",
          "data/logistic_requisition_sequence.xml",
          "view/logistic_requisition.xml",
          "view/sale_order.xml",
          "view/cancel_reason.xml",
          "view/purchase_order.xml",
          "view/report_logistic_requisition.xml",
          "logistic_requisition_report.xml",
          "data/logistic.requisition.cancel.reason.csv",
          ],
 "test": ['test/line_assigned.yml',
          'test/requisition_create_cost_estimate.yml',
          'test/requisition_sourcing_with_tender.yml',
          'test/requisition_cancel_reason.yml',
          # XXX port report to Qweb
          # 'test/logistic_requisition_report_test.yml',
          # XXX to remove or replace as there are no more relation on sol
          # 'test/test_picking_by_location_address.yml',
          ],
 'installable': True,
 'auto_install': False,
 }
