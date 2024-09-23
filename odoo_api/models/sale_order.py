
from odoo import models, fields
import datetime
from datetime import date
from datetime import date, timedelta

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    
    def GetOrder(self,data):
        domain = []
        response = []
        if data.get("name"):
            domain.append(("name", "in", data.get("name")))

        if data.get("company_id"):
            if domain:
                domain.insert(0, '&')
            domain.append(("company_id", "in", data.get("company_id")))        

        if data.get("create_date_from"):
            if domain:
                domain.insert(0, '&')
            domain.append(("create_date", ">=", data.get("create_date_from")))

        if data.get("create_date_to"):
            if domain:
                domain.insert(0, '&')
            domain.append(("create_date", "<=", data.get("create_date_to")))

        if data.get("update_from"):
            if domain:
                domain.insert(0, '&')
            domain.append(("write_date", ">=", data.get("update_from")))

        if data.get("update_to"):
            if domain:
                domain.insert(0, '&')
            domain.append(("write_date", "<=", data.get("update_to")))
        
        if data.get("order_date_from"):
            if domain:
                domain.insert(0, '&')
            domain.append(("date_order", ">=", data.get("order_date_from")))

        if data.get("order_date_to"):
            if domain:
                domain.insert(0, '&')
            domain.append(("date_order", "<=", data.get("order_date_to")))

        if data.get("order_date"):
            today = date.today()
            if data.get("order_date") == "this_month":                
                first_day_of_month = today.replace(day=1)
                last_day_of_month = today.replace(day=1).replace(month=today.month + 1, day=1) - timedelta(days=1)
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_order", ">=", first_day_of_month))
                domain.append(("date_order", "<=", last_day_of_month))

            elif data.get("order_date") == "this_year":
                first_day_of_year = today.replace(month=1, day=1)
                last_day_of_year = today.replace(month=12, day=31)
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_order", ">=", first_day_of_year))
                domain.append(("date_order", "<=", last_day_of_year))

        if data.get("state"):
            if domain:
                domain.insert(0, '&')
            domain.append(("state", "in", data.get("state")))

        if domain:
            orders = self.env["sale.order"].search(domain)
            for order in orders:
                order_data = {}

                for item in data.get("output_selector"):
                    item_split = item.split(".")
                    if hasattr(order, item_split[0]):
                        if len(item_split) > 1:                                                 
                            if hasattr(eval("order."+item_split[0]), item_split[1]):
                                order_data[item] = getattr(eval("order."+item_split[0]), item_split[1])
                        else :
                            if isinstance(getattr(order, item_split[0]), datetime.datetime):
                                order_data[item] = getattr(order, item_split[0]).strftime('%Y-%m-%d %H:%M:%S')
                            elif isinstance(getattr(order, item_split[0]), date):
                                order_data[item] = getattr(order, item_split[0]).strftime('%Y-%m-%d')
                            else :
                                order_data[item] = getattr(order, item_split[0])

                response.append(order_data)
            
        return response