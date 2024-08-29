
from odoo import models, fields
import datetime

class MyModel(models.Model):
    _inherit = 'account.move'
    
    
    def GetInvoice(self,data):
        domain = []
        response = []
        if data.get("name"):
            domain.append(("name","in", data.get("name")))

        if data.get("company_id"):
            domain.append(("company_id","in", data.get("company_id")))

        if domain:
            invoices = self.env["account.move"].search(domain)
            for invoice in invoices:
                invoice_data = {}

                for item in data.get("OutputSelector"):
                    item_split = item.split(".")
                    if hasattr(invoice, item_split[0]):
                        if len(item_split) > 1:                                                 
                            if hasattr(eval("invoice."+item_split[0]), item_split[1]):
                                invoice_data[item] = getattr(eval("invoice."+item_split[0]), item_split[1])
                        else :
                            if isinstance(getattr(invoice, item_split[0]), datetime.datetime):
                                invoice_data[item] = getattr(invoice, item_split[0]).strftime('%Y-%m-%d %H:%M:%S')
                            else :
                                invoice_data[item] = getattr(invoice, item_split[0])

                response.append(invoice_data)
            
        return response