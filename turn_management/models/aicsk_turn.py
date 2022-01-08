from odoo import api, fields, models, _


class AicskTurn(models.Model):
    _name = "aicsk.turn"
    _description = "Aicsk Turn"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    visitor_id = fields.Many2one(
        string='Visitor',
        comodel_name='res.partner',
        ondelete='restrict',
    )

    @api.model
    def get_coming_turn(self):
       info = "%s test" % self.env.user.partner_id.name
       # this function will render the visitor depending on the user and the state of the visit.fg

       return info