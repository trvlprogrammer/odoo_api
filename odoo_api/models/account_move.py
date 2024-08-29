
from odoo import models, fields
import datetime
from datetime import date

class MyModel(models.Model):
    _inherit = 'account.move'
    
    
    def GetInvoice(self,data):
        # domain = [("move_type","=","out_invoice")]
        domain = []
        response = []
        # if data.get("name"):
        #     domain.append(("name","in", data.get("name")))

        # if data.get("company_id"):
        #     domain.append(("company_id","in", data.get("company_id")))

        # if data.get("move_type"):
        #     domain.append(("move_type","in",data.get("move_type")))

        if data.get("name"):
            domain.append(("name", "in", data.get("name")))

        if data.get("company_id"):
            if domain:
                domain.insert(0, '&')
            domain.append(("company_id", "in", data.get("company_id")))

        if data.get("move_type"):
            if domain:
                domain.insert(0, '&')
            domain.append(("move_type", "in", data.get("move_type")))

        if data.get("create_date_from"):
            if domain:
                domain.insert(0, '&')
            domain.append(("create_date", ">=", data.get("create_date_from")))

        if data.get("create_date_to"):
            if domain:
                domain.insert(0, '&')
            domain.append(("create_date", "<=", data.get("create_date_to")))
        
        if data.get("invoice_date_from"):
            if domain:
                domain.insert(0, '&')
            domain.append(("invoice_date", ">=", data.get("invoice_date_from")))

        if data.get("invoice_date_to"):
            if domain:
                domain.insert(0, '&')
            domain.append(("invoice_date", "<=", data.get("invoice_date_to")))

        if data.get("state"):
            if domain:
                domain.insert(0, '&')
            domain.append(("state", "in", data.get("state")))

        if domain:
            invoices = self.env["account.move"].search(domain)
            for invoice in invoices:
                invoice_data = {}

                for item in data.get("output_selector"):
                    item_split = item.split(".")
                    if hasattr(invoice, item_split[0]):
                        if len(item_split) > 1:                                                 
                            if hasattr(eval("invoice."+item_split[0]), item_split[1]):
                                invoice_data[item] = getattr(eval("invoice."+item_split[0]), item_split[1])
                        else :
                            if isinstance(getattr(invoice, item_split[0]), datetime.datetime):
                                invoice_data[item] = getattr(invoice, item_split[0]).strftime('%Y-%m-%d %H:%M:%S')
                            elif isinstance(getattr(invoice, item_split[0]), date):
                                invoice_data[item] = getattr(invoice, item_split[0]).strftime('%Y-%m-%d')
                            else :
                                invoice_data[item] = getattr(invoice, item_split[0])

                response.append(invoice_data)
            
        return response