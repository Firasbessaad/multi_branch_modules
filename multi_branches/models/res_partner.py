# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class Partner(models.Model):
    _inherit = "res.partner"

    branch_id = fields.Many2one(
        "res.branch",
        string='Branch',
        default=lambda self: self.env.user.branch_id
    )
    company_id = fields.Many2one(
        default=lambda self: self.env.user.company_id
    )

    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id:
            branches = self.env.user.branch_ids.filtered(lambda m: m.company_id.id == self.company_id.id).ids
            self.branch_id = False
            if len(branches) > 0:
                self.branch_id = branches[0]
        else:
            return {'domain': {'branch_id': []}}
