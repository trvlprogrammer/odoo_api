from odoo import http
from odoo.http import request, Response
import json
import logging

_logger = logging.getLogger(__name__)

class MyApiController(http.Controller): 

    @http.route('/api', type='http', auth='api_key', methods=['POST'], csrf=False)
    def odoo_api(self, **kwargs):
        try:

            header = request.httprequest.environ
            # data = request.get_json_data()
            json_data = request.httprequest.get_data(as_text=True)
            data = json.loads(json_data)
            response_data = []
            if data.get("Filter"):
                if header.get("HTTP_ODOO_ACTION") == "GetInvoice" or data.get("ODOO_ACTION")=="GetInvoice":
                    models = request.env['account.move']
                    if hasattr(models, 'GetInvoice'):
                        response_data = getattr(models, 'GetInvoice')(data.get("Filter"))
                elif header.get("HTTP_ODOO_ACTION") == "GetOrder" or data.get("ODOO_ACTION")=="GetOrder":
                    models = request.env['sale.order']
                    if hasattr(models, 'GetOrder'):
                        response_data = getattr(models, 'GetOrder')(data.get("Filter"))
                elif header.get("HTTP_ODOO_ACTION") == "GetDeliveryOrder" or data.get("ODOO_ACTION")=="GetDeliveryOrder":
                    models = request.env['stock.picking']
                    if hasattr(models, 'GetDeliveryOrder'):
                        response_data = getattr(models, 'GetDeliveryOrder')(data.get("Filter"))
                elif header.get("HTTP_ODOO_ACTION") == "GetActivity" or data.get("ODOO_ACTION")=="GetActivity":
                    models = request.env['crm.activity.report']
                    if hasattr(models, 'GetActivity'):
                        response_data = getattr(models, 'GetActivity')(data.get("Filter"))
                else :
                    data["header"] = header
                    response_data = data
            else :
                data["header"] = header
                response_data = data

            return Response(
                json.dumps({
                    'status': 'Success',
                    'item': response_data,
                    'version' : '1.0'
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
                    'version' : '1.0'
                }),
                content_type='application/json',
                status=500
            )
