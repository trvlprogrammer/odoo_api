
from odoo import models, fields
import datetime
from datetime import date
from datetime import date, timedelta

class CrmActivityReport(models.Model):
    _inherit = 'crm.activity.report'
    
    
    def GetActivity(self,data):
        domain = []
        response = []
        if data.get("name"):
            domain.append(("name", "in", data.get("name")))

        if data.get("company_id"):
            if domain:
                domain.insert(0, '&')
            domain.append(("company_id", "in", data.get("company_id")))

        if data.get("mail_activity_type_id"):
            if domain:
                domain.insert(0, '&')
            domain.append(("mail_activity_type_id", "in", data.get("mail_activity_type_id")))

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
        
        if data.get("date_from"):
            if domain:
                domain.insert(0, '&')
            domain.append(("date", ">=", data.get("invoice_date_from")))

        if data.get("date_to"):
            if domain:
                domain.insert(0, '&')
            domain.append(("date", "<=", data.get("invoice_date_to")))

        if data.get("date"):
            today = date.today()
            if data.get("date") == "this_month":                
                first_day_of_month = today.replace(day=1)
                last_day_of_month = today.replace(day=1).replace(month=today.month + 1, day=1) - timedelta(days=1)
                if domain:
                    domain.insert(0, '&')
                domain.append(("date", ">=", first_day_of_month))
                domain.append(("date", "<=", last_day_of_month))

            elif data.get("date") == "this_year":
                first_day_of_year = today.replace(month=1, day=1)
                last_day_of_year = today.replace(month=12, day=31)
                if domain:
                    domain.insert(0, '&')
                domain.append(("date", ">=", first_day_of_year))
                domain.append(("date", "<=", last_day_of_year))

        if data.get("state"):
            if domain:
                domain.insert(0, '&')
            domain.append(("state", "in", data.get("state")))

        if domain:
            activities = self.env["crm.activity.report"].search(domain)
            for activity in activities:
                activity_data = {}

                for item in data.get("output_selector"):
                    item_split = item.split(".")
                    if hasattr(activity, item_split[0]):
                        if len(item_split) > 1:                                                 
                            if hasattr(eval("activity."+item_split[0]), item_split[1]):
                                activity_data[item] = getattr(eval("activity."+item_split[0]), item_split[1])
                        else :
                            if isinstance(getattr(activity, item_split[0]), datetime.datetime):
                                activity_data[item] = getattr(activity, item_split[0]).strftime('%Y-%m-%d %H:%M:%S')
                            elif isinstance(getattr(activity, item_split[0]), date):
                                activity_data[item] = getattr(activity, item_split[0]).strftime('%Y-%m-%d')
                            else :
                                activity_data[item] = getattr(activity, item_split[0])

                response.append(activity_data)
            
        return response