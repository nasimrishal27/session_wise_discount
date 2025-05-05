from odoo import http
from odoo.http import request

class POSSessionController(http.Controller):

    @http.route('/pos/update_session_discount_limit', type='json', auth='user')
    def update_session_discount_limit(self, session_id, used_discount):
        session = request.env['pos.session'].browse(session_id)
        if session and session.session_discount_limit is not None:
            session.session_discount_limit -= used_discount
        return {'remaining_limit': session.session_discount_limit}
