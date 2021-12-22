# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Warehouse(models.Model):
    _inherit = 'stock.warehouse'

    branch_id = fields.Many2one("res.branch", string='Branch', default=lambda self: self.env.user.branch_id)

    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id:
            return {'domain': {'branch_id': [('company_id', '=', self.company_id.id)]}}

        else:
            return {'domain': {'branch_id': []}}

    @api.model
    def create(self, vals):
        if self._context.get('is_branch'):
            return False
        warehouse = super(Warehouse, self).create(vals)
        if warehouse:
            warehouse.lot_stock_id.write({'branch_id': vals.get('branch_id')})
            warehouse.view_location_id.write({'branch_id': vals.get('branch_id')})
            warehouse.wh_input_stock_loc_id.write({'branch_id': vals.get('branch_id')})
            warehouse.wh_qc_stock_loc_id.write({'branch_id': vals.get('branch_id')})
            warehouse.wh_output_stock_loc_id.write({'branch_id': vals.get('branch_id')})
            warehouse.wh_pack_stock_loc_id.write({'branch_id': vals.get('branch_id')})
        return warehouse

    @api.model
    def name_search(self, name, args, operator='ilike', limit=100):
        if self._context.get('branch_id', False):
            branch_id = self._context.get('branch_id', False)
            warehouses = self.env['stock.warehouse'].search([('branch_id', '=', branch_id)])
            if len(warehouses) > 0:
                args.append(('id', 'in', warehouses.ids))
            else:
                args.append(('id', '=', []))
        return super(Warehouse, self).name_search(name, args=args, operator=operator, limit=limit)


class StockLocation(models.Model):
    _inherit = 'stock.location'

    branch_id = fields.Many2one("res.branch", string='Branch', default=lambda self: self.env.user.branch_id)

    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id:
            branches = self.env.user.branch_ids.filtered(lambda m: m.company_id.id == self.company_id.id).ids
            return {'domain': {'branch_id': [('id', 'in', branches)]}}
        else:
            return {'domain': {'branch_id': []}}

    @api.onchange('branch_id')
    def _onchange_branch_id(self):
        if self.location_id:
            if self.branch_id.id != self.location_id.branch_id.id and self.location_id.name != 'Virtual Locations':
                raise ValidationError(
                    _("Configuration Error \n You must select same branch on a location as a warehouse configuration"))


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    branch_id = fields.Many2one("res.branch", string='Branch',
                                default=lambda self: self.env.user.branch_id, index=True,
                                states={'done': [('readonly', True)], 'cancel': [('readonly', True)]})

    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id:
            branches = self.env.user.branch_ids.filtered(lambda m: m.company_id.id == self.company_id.id).ids
            self.branch_id = False
            if len(branches) > 0:
                self.branch_id = branches[0]
        else:
            return {'domain': {'branch_id': []}}


class StockMove(models.Model):
    _inherit = 'stock.move'

    branch_id = fields.Many2one("res.branch", string='Branch', default=lambda self: self.env.user.branch_id)

    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id:
            branches = self.env.user.branch_ids.filtered(lambda m: m.company_id.id == self.company_id.id).ids
            self.branch_id = False
            if len(branches) > 0:
                self.branch_id = branches[0]
        else:
            return {'domain': {'branch_id': []}}

    def _create_account_move_line(self, credit_account_id, debit_account_id, journal_id, qty, description, svl_id, cost):
        self.ensure_one()
        AccountMove = self.env['account.move'].with_context(default_journal_id=journal_id)

        move_lines = self._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id, description)
        if move_lines:
            date = self._context.get('force_period_date', fields.Date.context_today(self))
            new_account_move = AccountMove.sudo().create({
                'journal_id': journal_id,
                'line_ids': move_lines,
                'date': date,
                'ref': description,
                'stock_move_id': self.id,
                'stock_valuation_layer_ids': [(6, None, [svl_id])],
                'type': 'entry',
                'branch_id': self.branch_id.id,
            })
            new_account_move.post()

    def _generate_valuation_lines_data(self, partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, description):
        res = super(StockMove, self)._generate_valuation_lines_data(partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, description)
        res['debit_line_vals'].update({'branch_id': self.picking_id.branch_id.id})
        res['credit_line_vals'].update({'branch_id': self.picking_id.branch_id.id})
        if 'price_diff_line_vals' in res:
            res['price_diff_line_vals'].update({'branch_id': self.picking_id.branch_id.id})
        return res


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    branch_id = fields.Many2one(related='location_id.branch_id', store=True, readonly=True, string='Branch')

class StockRule(models.Model):
    """ A rule describe what a procurement should do; produce, buy, move, ... """
    _inherit = 'stock.rule'

    branch_id = fields.Many2one("res.branch", string='Branch', related='warehouse_id.branch_id')
