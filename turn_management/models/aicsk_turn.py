from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Visit(models.Model):
    _name = "aicsk.visit"

    aicsk_visitor_id = fields.Many2one(
        comodel_name='res.partner',
        string='Visitor')

    aicsk_type = fields.Selection(
        string='Visit Type',
        selection=[('registration', 'Registration'),
                   ('other', 'Other'), ]
    )

    aicsk_turn = fields.Char(default = lambda self : self.env['ir.sequence'].next_by_code('aicsk.visit'))