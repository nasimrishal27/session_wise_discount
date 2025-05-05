from odoo import models, fields, api

class PosSession(models.Model):
    _inherit = 'pos.session'

    session_discount_limit = fields.Float(
        string="Session Discount Limit",
        compute="_compute_discount_limit",
        store=True
    )

    @api.depends('config_id')
    def _compute_discount_limit(self):
        param = self.env['ir.config_parameter'].sudo()
        enabled = param.get_param('res.config.settings.enable_session_wise_discount', 'False') == 'True'
        amount = float(param.get_param('res.config.settings.session_wise_discount_amount', '0'))
        for session in self:
            session.session_discount_limit = amount if enabled else 0.0

    @api.model
    def _load_pos_data_fields(self, config_id):
        params = super()._load_pos_data_fields(config_id)
        params += ['session_discount_limit']
        return params