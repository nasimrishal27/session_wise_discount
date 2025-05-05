# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    """Extension of 'res.config.settings' for configuring delivery settings."""
    _inherit = 'res.config.settings'
    enable_session_wise_discount = fields.Boolean(string='Enable Session Wise Discount',
                                                  help='This field is used to enable setting session'
                                                       'wise discount in settings')
    session_wise_discount_amount = fields.Float(string='Discount Amount', help='Set the discount amount')

    @api.model
    def get_values(self):
        """Get the values from settings."""
        res = super(ResConfigSettings, self).get_values()
        icp_sudo = self.env['ir.config_parameter'].sudo()
        enable_session_wise_discount = icp_sudo.get_param('res.config.settings.enable_session_wise_discount')
        session_wise_discount_amount = icp_sudo.get_param('res.config.settings.session_wise_discount_amount')
        res.update(
            enable_session_wise_discount=enable_session_wise_discount,
            session_wise_discount_amount=session_wise_discount_amount if session_wise_discount_amount else 0,
        )
        return res

    def set_values(self):
        """Set the values. The new values are stored in the configuration parameters."""
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.enable_session_wise_discount', self.enable_session_wise_discount)
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.session_wise_discount_amount',
            self.session_wise_discount_amount)
        return res
