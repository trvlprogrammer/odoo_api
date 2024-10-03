
from odoo import models, fields
import datetime
from datetime import date
from datetime import date, timedelta

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    
    def GetDeliveryOrder(self,data):
        domain = []
        response = []
        if data.get("name"):
            domain.append(("name", "in", data.get("name")))

        if data.get("company_id"):
            if domain:
                domain.insert(0, '&')
            domain.append(("company_id", "in", data.get("company_id")))

        if data.get("picking_type_id"):
            if domain:
                domain.insert(0, '&')
            domain.append(("picking_type_id", "in", data.get("picking_type_id")))

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
        
        if data.get("scheduled_date_from"):
            if domain:
                domain.insert(0, '&')
            domain.append(("scheduled_date", ">=", data.get("scheduled_date_from")))

        if data.get("scheduled_date_to"):
            if domain:
                domain.insert(0, '&')
            domain.append(("scheduled_date", "<=", data.get("scheduled_date_to")))

        if data.get("scheduled_date"):
            today = date.today()
            if data.get("scheduled_date") == "this_month":                
                first_day_of_month = today.replace(day=1)
                last_day_of_month = today.replace(day=1).replace(month=today.month + 1, day=1) - timedelta(days=1)
                if domain:
                    domain.insert(0, '&')
                domain.append(("scheduled_date", ">=", first_day_of_month))
                domain.append(("scheduled_date", "<=", last_day_of_month))

            elif data.get("scheduled_date") == "this_year":
                first_day_of_year = today.replace(month=1, day=1)
                last_day_of_year = today.replace(month=12, day=31)
                if domain:
                    domain.insert(0, '&')
                domain.append(("scheduled_date", ">=", first_day_of_year))
                domain.append(("scheduled_date", "<=", last_day_of_year))

            # Handle "last_year"
            elif data.get("scheduled_date") == "last_year":
                last_year = today.year - 1
                first_day_of_last_year = today.replace(year=last_year, month=1, day=1)
                last_day_of_last_year = today.replace(year=last_year, month=12, day=31)
                if domain:
                    domain.insert(0, '&')
                domain.append(("scheduled_date", ">=", first_day_of_last_year))
                domain.append(("scheduled_date", "<=", last_day_of_last_year))

            # Handle "this_au_year" (July 1, 2024 - June 30, 2025)
            elif data.get("scheduled_date") == "this_au_year":
                first_day_of_au_year = date(today.year, 7, 1)  # July 1, 2024
                last_day_of_au_year = date(today.year + 1, 6, 30)  # June 30, 2025
                if domain:
                    domain.insert(0, '&')
                domain.append(("scheduled_date", ">=", first_day_of_au_year))
                domain.append(("scheduled_date", "<=", last_day_of_au_year))

            # Handle "last_au_year" (July 1, 2023 - June 30, 2024)
            elif data.get("scheduled_date") == "last_au_year":
                first_day_of_last_au_year = date(today.year - 1, 7, 1)  # July 1, 2023
                last_day_of_last_au_year = date(today.year, 6, 30)  # June 30, 2024
                if domain:
                    domain.insert(0, '&')
                domain.append(("scheduled_date", ">=", first_day_of_last_au_year))
                domain.append(("scheduled_date", "<=", last_day_of_last_au_year))

            # Handle "this_nz_year" (April 1, 2024 - March 31, 2025)
            elif data.get("scheduled_date") == "this_nz_year":
                first_day_of_nz_year = date(today.year, 4, 1)  # April 1, 2024
                last_day_of_nz_year = date(today.year + 1, 3, 31)  # March 31, 2025
                if domain:
                    domain.insert(0, '&')
                domain.append(("scheduled_date", ">=", first_day_of_nz_year))
                domain.append(("scheduled_date", "<=", last_day_of_nz_year))

            # Handle "last_nz_year" (April 1, 2023 - March 31, 2024)
            elif data.get("scheduled_date") == "last_nz_year":
                first_day_of_last_nz_year = date(today.year - 1, 4, 1)  # April 1, 2023
                last_day_of_last_nz_year = date(today.year, 3, 31)  # March 31, 2024
                if domain:
                    domain.insert(0, '&')
                domain.append(("scheduled_date", ">=", first_day_of_last_nz_year))
                domain.append(("scheduled_date", "<=", last_day_of_last_nz_year))

        if data.get("effective_date_from"):
            if domain:
                domain.insert(0, '&')
            domain.append(("date_done", ">=", data.get("effective_date_from")))

        if data.get("effective_date_to"):
            if domain:
                domain.insert(0, '&')
            domain.append(("date_done", "<=", data.get("effective_date_to")))

        if data.get("effective_date"):
            today = date.today()
            if data.get("effective_date") == "this_month":                
                first_day_of_month = today.replace(day=1)
                last_day_of_month = today.replace(day=1).replace(month=today.month + 1, day=1) - timedelta(days=1)
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_done", ">=", first_day_of_month))
                domain.append(("date_done", "<=", last_day_of_month))

            elif data.get("effective_date") == "this_year":
                first_day_of_year = today.replace(month=1, day=1)
                last_day_of_year = today.replace(month=12, day=31)
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_done", ">=", first_day_of_year))
                domain.append(("date_done", "<=", last_day_of_year))

            # Handle "last_year"
            elif data.get("effective_date") == "last_year":
                last_year = today.year - 1
                first_day_of_last_year = today.replace(year=last_year, month=1, day=1)
                last_day_of_last_year = today.replace(year=last_year, month=12, day=31)
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_done", ">=", first_day_of_last_year))
                domain.append(("date_done", "<=", last_day_of_last_year))

            # Handle "this_au_year" (July 1, 2024 - June 30, 2025)
            elif data.get("effective_date") == "this_au_year":
                first_day_of_au_year = date(today.year, 7, 1)  # July 1, 2024
                last_day_of_au_year = date(today.year + 1, 6, 30)  # June 30, 2025
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_done", ">=", first_day_of_au_year))
                domain.append(("date_done", "<=", last_day_of_au_year))

            # Handle "last_au_year" (July 1, 2023 - June 30, 2024)
            elif data.get("effective_date") == "last_au_year":
                first_day_of_last_au_year = date(today.year - 1, 7, 1)  # July 1, 2023
                last_day_of_last_au_year = date(today.year, 6, 30)  # June 30, 2024
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_done", ">=", first_day_of_last_au_year))
                domain.append(("date_done", "<=", last_day_of_last_au_year))

            # Handle "this_nz_year" (April 1, 2024 - March 31, 2025)
            elif data.get("effective_date") == "this_nz_year":
                first_day_of_nz_year = date(today.year, 4, 1)  # April 1, 2024
                last_day_of_nz_year = date(today.year + 1, 3, 31)  # March 31, 2025
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_done", ">=", first_day_of_nz_year))
                domain.append(("date_done", "<=", last_day_of_nz_year))

            # Handle "last_nz_year" (April 1, 2023 - March 31, 2024)
            elif data.get("effective_date") == "last_nz_year":
                first_day_of_last_nz_year = date(today.year - 1, 4, 1)  # April 1, 2023
                last_day_of_last_nz_year = date(today.year, 3, 31)  # March 31, 2024
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_done", ">=", first_day_of_last_nz_year))
                domain.append(("date_done", "<=", last_day_of_last_nz_year))

        if data.get("state"):
            if domain:
                domain.insert(0, '&')
            domain.append(("state", "in", data.get("state")))

        if domain:
            pickings = self.env["stock.picking"].search(domain)
            for picking in pickings:
                picking_data = {}

                for item in data.get("output_selector"):
                    item_split = item.split(".")
                    if hasattr(picking, item_split[0]):
                        if len(item_split) > 1:                                                 
                            if hasattr(eval("picking."+item_split[0]), item_split[1]):
                                picking_data[item] = getattr(eval("picking."+item_split[0]), item_split[1])
                        else :
                            if isinstance(getattr(picking, item_split[0]), datetime.datetime):
                                picking_data[item] = getattr(picking, item_split[0]).strftime('%Y-%m-%d %H:%M:%S')
                            elif isinstance(getattr(picking, item_split[0]), date):
                                picking_data[item] = getattr(picking, item_split[0]).strftime('%Y-%m-%d')
                            else :
                                picking_data[item] = getattr(picking, item_split[0])

                response.append(picking_data)
            
        return response