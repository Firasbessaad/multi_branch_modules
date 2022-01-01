from odoo import api, fields, models, _


class AicskTurn(models.Model):
    _name = "aicsk.trun"
    _description = "Aicsk Turn"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    visitor_id = fields.Many2one(
        string='Visitor',
        comodel_name='res.partner',
        ondelete='restrict',
    )
    
    def get_coming_turn(self):
       info = "%s" % self.env.user.partner_id.name
       return info