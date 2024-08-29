from odoo import http
from odoo.http import request, Response
import json
import logging

_logger = logging.getLogger(__name__)

class MyApiController(http.Controller):  # Make sure "Controller" is spelled correctly

    @http.route('/api', type='http', auth='public', methods=['POST'], csrf=False)
    def odoo_api(self, **kwargs):
        try:

            header = request.httprequest.headers.environ
            data = request.get_json_data()
            
            if data.get("Filter"):
                if header.get("HTTP_ODOO_ACTION") == "GetInvoice":
                    models = request.env['account.move'].sudo()
                    if hasattr(models, 'GetInvoice'):
                        response_data = getattr(models, 'GetInvoice')(data.get("Filter"))

            return Response(
                json.dumps({
                    'status': 'Success',
                    'item': response_data,
                }),
                content_type='application/json',
                status=200
            )
        except Exception as e:
            _logger.exception("Error in API: %s", e)
            return Response(
                json.dumps({
                    'status': 'Error',
                    'message': str(e),
                }),
                content_type='application/json',
                status=500
            )
