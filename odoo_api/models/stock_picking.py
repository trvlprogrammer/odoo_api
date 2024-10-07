
from odoo import models, fields
# import datetime
# from datetime import date
from datetime import date, timedelta, datetime
import logging

_logger = logging.getLogger(__name__)
class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    
    def GetDeliveryOrder(self,data):
        domain = []
        timezone = 0
        response = []

        if data.get("time_zone"):
            timezone = data.get("time_zone")

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
            today = datetime.now()
            if data.get("scheduled_date") == "this_month":                
                first_day_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                first_day_of_month = first_day_of_month - timedelta(hours=timezone)
                
                if today.month == 12:  # Handle December case
                    last_day_of_month = today.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
                else:
                    first_day_of_next_month = today.replace(day=1, month=today.month + 1, hour=0, minute=0, second=0, microsecond=0)
                    last_day_of_month = first_day_of_next_month - timedelta(seconds=1)
                
                last_day_of_month = last_day_of_month - timedelta(hours=timezone)
                if domain:
                    domain.insert(0, '&')
                domain.append(("scheduled_date", ">=", first_day_of_month))
                domain.append(("scheduled_date", "<=", last_day_of_month))

            elif data.get("scheduled_date") == "this_year":
                first_day_of_year = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                first_day_of_year = first_day_of_year - timedelta(hours=timezone)
                
                last_day_of_year = today.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
                last_day_of_year = last_day_of_year - timedelta(hours=timezone)
                if domain:
                    domain.insert(0, '&')
                domain.append(("scheduled_date", ">=", first_day_of_year))
                domain.append(("scheduled_date", "<=", last_day_of_year))

            # Handle "last_year"
            elif data.get("scheduled_date") == "last_year":
                last_year = today.year - 1
                first_day_of_last_year = today.replace(year=last_year, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                first_day_of_last_year = first_day_of_last_year - timedelta(hours=timezone)
                
                last_day_of_last_year = today.replace(year=last_year, month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
                last_day_of_last_year = last_day_of_last_year - timedelta(hours=timezone)
                if domain:
                    domain.insert(0, '&')
                domain.append(("scheduled_date", ">=", first_day_of_last_year))
                domain.append(("scheduled_date", "<=", last_day_of_last_year))

            # Handle "this_au_year" (July 1, 2024 - June 30, 2025)
            elif data.get("scheduled_date") == "this_au_year":
                first_day_of_au_year = datetime(today.year, 7, 1, 0, 0, 0)
                first_day_of_au_year = first_day_of_au_year - timedelta(hours=timezone)
                
                last_day_of_au_year = datetime(today.year + 1, 6, 30, 23, 59, 59)
                last_day_of_au_year = last_day_of_au_year - timedelta(hours=timezone)
                if domain:
                    domain.insert(0, '&')
                domain.append(("scheduled_date", ">=", first_day_of_au_year))
                domain.append(("scheduled_date", "<=", last_day_of_au_year))

            # Handle "last_au_year" (July 1, 2023 - June 30, 2024)
            elif data.get("scheduled_date") == "last_au_year":
                first_day_of_last_au_year = datetime(today.year - 1, 7, 1, 0, 0, 0)
                first_day_of_last_au_year = first_day_of_last_au_year - timedelta(hours=timezone)
                
                last_day_of_last_au_year = datetime(today.year, 6, 30, 23, 59, 59)
                last_day_of_last_au_year = last_day_of_last_au_year - timedelta(hours=timezone)
                if domain:
                    domain.insert(0, '&')
                domain.append(("scheduled_date", ">=", first_day_of_last_au_year))
                domain.append(("scheduled_date", "<=", last_day_of_last_au_year))

            # Handle "this_nz_year" (April 1, 2024 - March 31, 2025)
            elif data.get("scheduled_date") == "this_nz_year":
                first_day_of_nz_year = datetime(today.year, 4, 1, 0, 0, 0)
                first_day_of_nz_year = first_day_of_nz_year - timedelta(hours=timezone)
                
                last_day_of_nz_year = datetime(today.year + 1, 3, 31, 23, 59, 59)
                last_day_of_nz_year = last_day_of_nz_year - timedelta(hours=timezone)
                if domain:
                    domain.insert(0, '&')
                domain.append(("scheduled_date", ">=", first_day_of_nz_year))
                domain.append(("scheduled_date", "<=", last_day_of_nz_year))

            # Handle "last_nz_year" (April 1, 2023 - March 31, 2024)
            elif data.get("scheduled_date") == "last_nz_year":
                first_day_of_last_nz_year = datetime(today.year - 1, 4, 1, 0, 0, 0)
                first_day_of_last_nz_year = first_day_of_last_nz_year - timedelta(hours=timezone)
                
                last_day_of_last_nz_year = datetime(today.year, 3, 31, 23, 59, 59)
                last_day_of_last_nz_year = last_day_of_last_nz_year - timedelta(hours=timezone)
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
            today = datetime.now()
            if data.get("effective_date") == "this_month":                
                first_day_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                first_day_of_month = first_day_of_month - timedelta(hours=timezone)
                
                if today.month == 12:  # Handle December case
                    last_day_of_month = today.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
                else:
                    first_day_of_next_month = today.replace(day=1, month=today.month + 1, hour=0, minute=0, second=0, microsecond=0)
                    last_day_of_month = first_day_of_next_month - timedelta(seconds=1)
                
                last_day_of_month = last_day_of_month - timedelta(hours=timezone)
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_done", ">=", first_day_of_month))
                domain.append(("date_done", "<=", last_day_of_month))

            elif data.get("effective_date") == "this_year":
                first_day_of_year = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                first_day_of_year = first_day_of_year - timedelta(hours=timezone)
                
                last_day_of_year = today.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
                last_day_of_year = last_day_of_year - timedelta(hours=timezone)
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_done", ">=", first_day_of_year))
                domain.append(("date_done", "<=", last_day_of_year))

            # Handle "last_year"
            elif data.get("effective_date") == "last_year":
                last_year = today.year - 1
                first_day_of_last_year = today.replace(year=last_year, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                first_day_of_last_year = first_day_of_last_year - timedelta(hours=timezone)
                
                last_day_of_last_year = today.replace(year=last_year, month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
                last_day_of_last_year = last_day_of_last_year - timedelta(hours=timezone)
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_done", ">=", first_day_of_last_year))
                domain.append(("date_done", "<=", last_day_of_last_year))

            # Handle "this_au_year" (July 1, 2024 - June 30, 2025)
            elif data.get("effective_date") == "this_au_year":
                first_day_of_au_year = datetime(today.year, 7, 1, 0, 0, 0)
                first_day_of_au_year = first_day_of_au_year - timedelta(hours=timezone)
                
                last_day_of_au_year = datetime(today.year + 1, 6, 30, 23, 59, 59)
                last_day_of_au_year = last_day_of_au_year - timedelta(hours=timezone)
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_done", ">=", first_day_of_au_year))
                domain.append(("date_done", "<=", last_day_of_au_year))

            # Handle "last_au_year" (July 1, 2023 - June 30, 2024)
            elif data.get("effective_date") == "last_au_year":
                first_day_of_last_au_year = datetime(today.year - 1, 7, 1, 0, 0, 0)
                first_day_of_last_au_year = first_day_of_last_au_year - timedelta(hours=timezone)
                
                last_day_of_last_au_year = datetime(today.year, 6, 30, 23, 59, 59)
                last_day_of_last_au_year = last_day_of_last_au_year - timedelta(hours=timezone)
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_done", ">=", first_day_of_last_au_year))
                domain.append(("date_done", "<=", last_day_of_last_au_year))

            # Handle "this_nz_year" (April 1, 2024 - March 31, 2025)
            elif data.get("effective_date") == "this_nz_year":
                first_day_of_nz_year = datetime(today.year, 4, 1, 0, 0, 0)
                first_day_of_nz_year = first_day_of_nz_year - timedelta(hours=timezone)
                
                last_day_of_nz_year = datetime(today.year + 1, 3, 31, 23, 59, 59)
                last_day_of_nz_year = last_day_of_nz_year - timedelta(hours=timezone)
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_done", ">=", first_day_of_nz_year))
                domain.append(("date_done", "<=", last_day_of_nz_year))

            # Handle "last_nz_year" (April 1, 2023 - March 31, 2024)
            elif data.get("effective_date") == "last_nz_year":
                first_day_of_last_nz_year = datetime(today.year - 1, 4, 1, 0, 0, 0)
                first_day_of_last_nz_year = first_day_of_last_nz_year - timedelta(hours=timezone)
                
                last_day_of_last_nz_year = datetime(today.year, 3, 31, 23, 59, 59)
                last_day_of_last_nz_year = last_day_of_last_nz_year - timedelta(hours=timezone)
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_done", ">=", first_day_of_last_nz_year))
                domain.append(("date_done", "<=", last_day_of_last_nz_year))

        if data.get("state"):
            if domain:
                domain.insert(0, '&')
            domain.append(("state", "in", data.get("state")))

        if domain:
            _logger.info(domain)
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
                            if isinstance(getattr(picking, item_split[0]), datetime):
                                datetime_data = getattr(picking, item_split[0]) + timedelta(hours=timezone)
                                picking_data[item] = datetime_data.strftime('%Y-%m-%d %H:%M:%S')
                            elif isinstance(getattr(picking, item_split[0]), date):
                                picking_data[item] = getattr(picking, item_split[0]).strftime('%Y-%m-%d')
                            else :
                                picking_data[item] = getattr(picking, item_split[0])

                response.append(picking_data)
            
        return response