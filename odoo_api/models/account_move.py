
from odoo import models, fields
# import datetime
# from datetime import date
from datetime import date, timedelta, datetime
import logging

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    
    def GetInvoice(self,data):
        timezone = 0
        domain = []
        response = []

        if data.get("time_zone"):
            timezone = data.get("time_zone")

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
            try:
                create_date_from = datetime.strptime(data.get("create_date_from"), '%Y-%m-%d %H:%M:%S')
                create_date_from = create_date_from - timedelta(hours=timezone)
                create_date_from = create_date_from.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError: 
                create_date_from = datetime.strptime(data.get("create_date_from"), '%Y-%m-%d')
            domain.append(("create_date", ">=", create_date_from))

        if data.get("create_date_to"):
            if domain:
                domain.insert(0, '&')
            try:
                create_date_to = datetime.strptime(data.get("create_date_to"), '%Y-%m-%d %H:%M:%S')
                create_date_to = create_date_to - timedelta(hours=timezone)
                create_date_to = create_date_to.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError: 
                create_date_to = datetime.strptime(data.get("create_date_to"), '%Y-%m-%d')
            domain.append(("create_date", "<=", create_date_to))

        if data.get("update_from"):
            if domain:
                domain.insert(0, '&')
            try:
                update_from = datetime.strptime(data.get("update_from"), '%Y-%m-%d %H:%M:%S')
                update_from = update_from - timedelta(hours=timezone)
                update_from = update_from.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError: 
                update_from = datetime.strptime(data.get("update_from"), '%Y-%m-%d')
            domain.append(("write_date", ">=", update_from))

        if data.get("update_to"):
            if domain:
                domain.insert(0, '&')
            try:
                update_to = datetime.strptime(data.get("update_to"), '%Y-%m-%d %H:%M:%S')
                update_to = update_to - timedelta(hours=timezone)
                update_to = update_to.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError: 
                update_to = datetime.strptime(data.get("update_to"), '%Y-%m-%d')
            domain.append(("write_date", "<=", update_to))
        
        if data.get("invoice_date_from"):
            if domain:
                domain.insert(0, '&')
            domain.append(("invoice_date", ">=", data.get("invoice_date_from")))

        if data.get("invoice_date_to"):
            if domain:
                domain.insert(0, '&')
            domain.append(("invoice_date", "<=", data.get("invoice_date_to")))

        if data.get("invoice_date"):
            today = date.today()
            
            # Handle "this_month"
            if data.get("invoice_date") == "this_month":
                first_day_of_month = today.replace(day=1)
                # first_day_of_month = first_day_of_month + timedelta(hours=timezone)
                last_day_of_month = (today.replace(day=1).replace(month=today.month + 1) - timedelta(days=1)
                                    if today.month < 12 else today.replace(month=12, day=31))
                # last_day_of_month = last_day_of_month + timedelta(hours=timezone)
                if domain:
                    domain.insert(0, '&')
                domain.append(("invoice_date", ">=", first_day_of_month))
                domain.append(("invoice_date", "<=", last_day_of_month))

            # Handle "this_year"
            elif data.get("invoice_date") == "this_year":
                first_day_of_year = today.replace(month=1, day=1)
                # first_day_of_year = first_day_of_year + timedelta(hours=timezone)
                last_day_of_year = today.replace(month=12, day=31)
                # last_day_of_year = last_day_of_year + timedelta(hours=timezone)
                if domain:
                    domain.insert(0, '&')
                domain.append(("invoice_date", ">=", first_day_of_year))
                domain.append(("invoice_date", "<=", last_day_of_year))

            # Handle "last_year"
            elif data.get("invoice_date") == "last_year":
                last_year = today.year - 1
                first_day_of_last_year = today.replace(year=last_year, month=1, day=1)
                # first_day_of_last_year = first_day_of_last_year + timedelta(hours=timezone)
                last_day_of_last_year = today.replace(year=last_year, month=12, day=31)
                # last_day_of_last_year = last_day_of_last_year + timedelta(hours=timezone)
                if domain:
                    domain.insert(0, '&')
                domain.append(("invoice_date", ">=", first_day_of_last_year))
                domain.append(("invoice_date", "<=", last_day_of_last_year))

            # Handle "this_au_year" (July 1, 2024 - June 30, 2025)
            elif data.get("invoice_date") == "this_au_year":
                first_day_of_au_year = date(today.year, 7, 1) 
                # first_day_of_au_year = first_day_of_au_year + timedelta(hours=timezone)
                last_day_of_au_year = date(today.year + 1, 6, 30) 
                # last_day_of_au_year = last_day_of_au_year + timedelta(hours=timezone)
                if domain:
                    domain.insert(0, '&')
                domain.append(("invoice_date", ">=", first_day_of_au_year))
                domain.append(("invoice_date", "<=", last_day_of_au_year))

            # Handle "last_au_year" (July 1, 2023 - June 30, 2024)
            elif data.get("invoice_date") == "last_au_year":
                first_day_of_last_au_year = date(today.year - 1, 7, 1)  # July 1, 2023
                # first_day_of_last_au_year = first_day_of_last_au_year + timedelta(hours=timezone)
                last_day_of_last_au_year = date(today.year, 6, 30)  # June 30, 2024
                # last_day_of_last_au_year = last_day_of_last_au_year + timedelta(hours=timezone)
                if domain:
                    domain.insert(0, '&')
                domain.append(("invoice_date", ">=", first_day_of_last_au_year))
                domain.append(("invoice_date", "<=", last_day_of_last_au_year))

            # Handle "this_nz_year" (April 1, 2024 - March 31, 2025)
            elif data.get("invoice_date") == "this_nz_year":
                first_day_of_nz_year = date(today.year, 4, 1)  # April 1, 2024
                # first_day_of_nz_year = first_day_of_nz_year + timedelta(hours=timezone)
                last_day_of_nz_year = date(today.year + 1, 3, 31)  # March 31, 2025
                # last_day_of_nz_year = last_day_of_nz_year + timedelta(hours=timezone)
                if domain:
                    domain.insert(0, '&')
                domain.append(("invoice_date", ">=", first_day_of_nz_year))
                domain.append(("invoice_date", "<=", last_day_of_nz_year))

            # Handle "last_nz_year" (April 1, 2023 - March 31, 2024)
            elif data.get("invoice_date") == "last_nz_year":
                first_day_of_last_nz_year = date(today.year - 1, 4, 1)  # April 1, 2023
                # first_day_of_last_nz_year = first_day_of_last_nz_year + timedelta(hours=timezone)
                last_day_of_last_nz_year = date(today.year, 3, 31)  # March 31, 2024
                # last_day_of_last_nz_year = last_day_of_last_nz_year + timedelta(hours=timezone)
                if domain:
                    domain.insert(0, '&')
                domain.append(("invoice_date", ">=", first_day_of_last_nz_year))
                domain.append(("invoice_date", "<=", last_day_of_last_nz_year))




        if data.get("state"):
            if domain:
                domain.insert(0, '&')
            domain.append(("state", "in", data.get("state")))

        if domain:
            _logger.info(domain)
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
                            if isinstance(getattr(invoice, item_split[0]), datetime):
                                datetime_data = getattr(invoice, item_split[0]) + timedelta(hours=timezone)
                                invoice_data[item] = datetime_data.strftime('%Y-%m-%d %H:%M:%S')
                            elif isinstance(getattr(invoice, item_split[0]), date):
                                invoice_data[item] = getattr(invoice, item_split[0]).strftime('%Y-%m-%d')
                            else :
                                invoice_data[item] = getattr(invoice, item_split[0])

                response.append(invoice_data)
            
        return response