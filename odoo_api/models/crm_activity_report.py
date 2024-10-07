
from odoo import models, fields
# import datetime
# from datetime import date
from datetime import date, timedelta, datetime
import logging

_logger = logging.getLogger(__name__)

class CrmActivityReport(models.Model):
    _inherit = 'crm.activity.report'
    
    
    def GetActivity(self,data):
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

        if data.get("activity_type_id"):
            if domain:
                domain.insert(0, '&')
            domain.append(("activity_type_id", "in", data.get("activity_type_id")))

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
        
        if data.get("date_deadline_from"):
            if domain:
                domain.insert(0, '&')
            try:
                date_deadline_from = datetime.strptime(data.get("date_deadline_from"), '%Y-%m-%d %H:%M:%S')
                date_deadline_from = date_deadline_from - timedelta(hours=timezone)
                date_deadline_from = date_deadline_from.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError: 
                date_deadline_from = datetime.strptime(data.get("date_deadline_from"), '%Y-%m-%d')
            domain.append(("date_deadline", ">=", date_deadline_from))

        if data.get("date_deadline_to"):
            if domain:
                domain.insert(0, '&')
            try:
                date_deadline_to = datetime.strptime(data.get("date_deadline_to"), '%Y-%m-%d %H:%M:%S')
                date_deadline_to = date_deadline_to - timedelta(hours=timezone)
                date_deadline_to = date_deadline_to.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError: 
                date_deadline_to = datetime.strptime(data.get("date_deadline_to"), '%Y-%m-%d')
            domain.append(("date_deadline", "<=", date_deadline_to))


        if data.get("date_deadline"):
            today = datetime.now()

            # Handle "this_month"
            if data.get("date_deadline") == "this_month":
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
                domain.append(("date_deadline", ">=", first_day_of_month))
                domain.append(("date_deadline", "<=", last_day_of_month))

            # Handle "this_year"
            elif data.get("date_deadline") == "this_year":
                first_day_of_year = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                first_day_of_year = first_day_of_year - timedelta(hours=timezone)
                
                last_day_of_year = today.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
                last_day_of_year = last_day_of_year - timedelta(hours=timezone)
                
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_deadline", ">=", first_day_of_year))
                domain.append(("date_deadline", "<=", last_day_of_year))

            # Handle "last_year"
            elif data.get("date_deadline") == "last_year":
                last_year = today.year - 1
                first_day_of_last_year = today.replace(year=last_year, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                first_day_of_last_year = first_day_of_last_year - timedelta(hours=timezone)
                
                last_day_of_last_year = today.replace(year=last_year, month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
                last_day_of_last_year = last_day_of_last_year - timedelta(hours=timezone)
                
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_deadline", ">=", first_day_of_last_year))
                domain.append(("date_deadline", "<=", last_day_of_last_year))

            # Handle "this_au_year" (July 1, 2024 - June 30, 2025)
            elif data.get("date_deadline") == "this_au_year":
                first_day_of_au_year = datetime(today.year, 7, 1, 0, 0, 0)
                first_day_of_au_year = first_day_of_au_year - timedelta(hours=timezone)
                
                last_day_of_au_year = datetime(today.year + 1, 6, 30, 23, 59, 59)
                last_day_of_au_year = last_day_of_au_year - timedelta(hours=timezone)
                
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_deadline", ">=", first_day_of_au_year))
                domain.append(("date_deadline", "<=", last_day_of_au_year))

            # Handle "last_au_year" (July 1, 2023 - June 30, 2024)
            elif data.get("date_deadline") == "last_au_year":
                first_day_of_last_au_year = datetime(today.year - 1, 7, 1, 0, 0, 0)
                first_day_of_last_au_year = first_day_of_last_au_year - timedelta(hours=timezone)
                
                last_day_of_last_au_year = datetime(today.year, 6, 30, 23, 59, 59)
                last_day_of_last_au_year = last_day_of_last_au_year - timedelta(hours=timezone)
                
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_deadline", ">=", first_day_of_last_au_year))
                domain.append(("date_deadline", "<=", last_day_of_last_au_year))

            # Handle "this_nz_year" (April 1, 2024 - March 31, 2025)
            elif data.get("date_deadline") == "this_nz_year":
                first_day_of_nz_year = datetime(today.year, 4, 1, 0, 0, 0)
                first_day_of_nz_year = first_day_of_nz_year - timedelta(hours=timezone)
                
                last_day_of_nz_year = datetime(today.year + 1, 3, 31, 23, 59, 59)
                last_day_of_nz_year = last_day_of_nz_year - timedelta(hours=timezone)
                
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_deadline", ">=", first_day_of_nz_year))
                domain.append(("date_deadline", "<=", last_day_of_nz_year))

            # Handle "last_nz_year" (April 1, 2023 - March 31, 2024)
            elif data.get("date_deadline") == "last_nz_year":
                first_day_of_last_nz_year = datetime(today.year - 1, 4, 1, 0, 0, 0)
                first_day_of_last_nz_year = first_day_of_last_nz_year - timedelta(hours=timezone)
                
                last_day_of_last_nz_year = datetime(today.year, 3, 31, 23, 59, 59)
                last_day_of_last_nz_year = last_day_of_last_nz_year - timedelta(hours=timezone)
                
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_deadline", ">=", first_day_of_last_nz_year))
                domain.append(("date_deadline", "<=", last_day_of_last_nz_year))

        if data.get("date_done_from"):
            if domain:
                domain.insert(0, '&')
            try:
                date_done_from = datetime.strptime(data.get("date_done_from"), '%Y-%m-%d %H:%M:%S')
                date_done_from = date_done_from - timedelta(hours=timezone)
                date_done_from = date_done_from.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError: 
                date_done_from = datetime.strptime(data.get("date_done_from"), '%Y-%m-%d')
            domain.append(("date_done", ">=", date_deadline_from))

        if data.get("date_done_to"):
            if domain:
                domain.insert(0, '&')
            try:
                date_done_to = datetime.strptime(data.get("date_done_to"), '%Y-%m-%d %H:%M:%S')
                date_done_to = date_done_to - timedelta(hours=timezone)
                date_done_to = date_done_to.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError: 
                date_done_to = datetime.strptime(data.get("date_done_to"), '%Y-%m-%d')
            domain.append(("date_done", "<=", date_done_to))


        if data.get("date_done"):
            today = datetime.now()

            # Handle "this_month"
            if data.get("date_done") == "this_month":
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

            # Handle "this_year"
            elif data.get("date_done") == "this_year":
                first_day_of_year = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                first_day_of_year = first_day_of_year - timedelta(hours=timezone)
                
                last_day_of_year = today.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
                last_day_of_year = last_day_of_year - timedelta(hours=timezone)
                
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_done", ">=", first_day_of_year))
                domain.append(("date_done", "<=", last_day_of_year))

            # Handle "last_year"
            elif data.get("date_done") == "last_year":
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
            elif data.get("date_done") == "this_au_year":
                first_day_of_au_year = datetime(today.year, 7, 1, 0, 0, 0)
                first_day_of_au_year = first_day_of_au_year - timedelta(hours=timezone)
                
                last_day_of_au_year = datetime(today.year + 1, 6, 30, 23, 59, 59)
                last_day_of_au_year = last_day_of_au_year - timedelta(hours=timezone)
                
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_done", ">=", first_day_of_au_year))
                domain.append(("date_done", "<=", last_day_of_au_year))

            # Handle "last_au_year" (July 1, 2023 - June 30, 2024)
            elif data.get("date_done") == "last_au_year":
                first_day_of_last_au_year = datetime(today.year - 1, 7, 1, 0, 0, 0)
                first_day_of_last_au_year = first_day_of_last_au_year - timedelta(hours=timezone)
                
                last_day_of_last_au_year = datetime(today.year, 6, 30, 23, 59, 59)
                last_day_of_last_au_year = last_day_of_last_au_year - timedelta(hours=timezone)
                
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_done", ">=", first_day_of_last_au_year))
                domain.append(("date_done", "<=", last_day_of_last_au_year))

            # Handle "this_nz_year" (April 1, 2024 - March 31, 2025)
            elif data.get("date_done") == "this_nz_year":
                first_day_of_nz_year = datetime(today.year, 4, 1, 0, 0, 0)
                first_day_of_nz_year = first_day_of_nz_year - timedelta(hours=timezone)
                
                last_day_of_nz_year = datetime(today.year + 1, 3, 31, 23, 59, 59)
                last_day_of_nz_year = last_day_of_nz_year - timedelta(hours=timezone)
                
                if domain:
                    domain.insert(0, '&')
                domain.append(("date_done", ">=", first_day_of_nz_year))
                domain.append(("date_done", "<=", last_day_of_nz_year))

            # Handle "last_nz_year" (April 1, 2023 - March 31, 2024)
            elif data.get("date_done") == "last_nz_year":
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
            activities = self.env["mail.activity"].search(domain)
            for activity in activities:
                activity_data = {}

                for item in data.get("output_selector"):
                    item_split = item.split(".")
                    if hasattr(activity, item_split[0]):
                        if len(item_split) > 1:                                                 
                            if hasattr(eval("activity."+item_split[0]), item_split[1]):
                                activity_data[item] = getattr(eval("activity."+item_split[0]), item_split[1])
                        else :
                            if isinstance(getattr(activity, item_split[0]), datetime):
                                datetime_data = getattr(activity, item_split[0]) + timedelta(hours=timezone)
                                activity_data[item] = datetime_data.strftime('%Y-%m-%d %H:%M:%S')
                            elif isinstance(getattr(activity, item_split[0]), date):
                                activity_data[item] = getattr(activity, item_split[0]).strftime('%Y-%m-%d')
                            else :
                                activity_data[item] = getattr(activity, item_split[0])

                response.append(activity_data)
            
        return response

    def GetActivityCRM(self,data):
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

        if data.get("mail_activity_type_id"):
            if domain:
                domain.insert(0, '&')
            domain.append(("mail_activity_type_id", "in", data.get("mail_activity_type_id")))

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
        
        if data.get("date_from"):
            if domain:
                domain.insert(0, '&')
            try:
                date_from = datetime.strptime(data.get("date_from"), '%Y-%m-%d %H:%M:%S')
                date_from = date_from - timedelta(hours=timezone)
                date_from = date_from.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError: 
                date_from = datetime.strptime(data.get("date_from"), '%Y-%m-%d')
            domain.append(("date", ">=", date_from))

        if data.get("date_to"):
            if domain:
                domain.insert(0, '&')
            try:
                date_to = datetime.strptime(data.get("date_to"), '%Y-%m-%d %H:%M:%S')
                date_to = date_to - timedelta(hours=timezone)
                date_to = date_to.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError: 
                date_to = datetime.strptime(data.get("date_to"), '%Y-%m-%d')
            domain.append(("date", "<=", date_to))


        if data.get("date"):
            today = datetime.now()

            # Handle "this_month"
            if data.get("date") == "this_month":
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
                domain.append(("date", ">=", first_day_of_month))
                domain.append(("date", "<=", last_day_of_month))

            # Handle "this_year"
            elif data.get("date") == "this_year":
                first_day_of_year = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                first_day_of_year = first_day_of_year - timedelta(hours=timezone)
                
                last_day_of_year = today.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
                last_day_of_year = last_day_of_year - timedelta(hours=timezone)
                
                if domain:
                    domain.insert(0, '&')
                domain.append(("date", ">=", first_day_of_year))
                domain.append(("date", "<=", last_day_of_year))

            # Handle "last_year"
            elif data.get("date") == "last_year":
                last_year = today.year - 1
                first_day_of_last_year = today.replace(year=last_year, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                first_day_of_last_year = first_day_of_last_year - timedelta(hours=timezone)
                
                last_day_of_last_year = today.replace(year=last_year, month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
                last_day_of_last_year = last_day_of_last_year - timedelta(hours=timezone)
                
                if domain:
                    domain.insert(0, '&')
                domain.append(("date", ">=", first_day_of_last_year))
                domain.append(("date", "<=", last_day_of_last_year))

            # Handle "this_au_year" (July 1, 2024 - June 30, 2025)
            elif data.get("date") == "this_au_year":
                first_day_of_au_year = datetime(today.year, 7, 1, 0, 0, 0)
                first_day_of_au_year = first_day_of_au_year - timedelta(hours=timezone)
                
                last_day_of_au_year = datetime(today.year + 1, 6, 30, 23, 59, 59)
                last_day_of_au_year = last_day_of_au_year - timedelta(hours=timezone)
                
                if domain:
                    domain.insert(0, '&')
                domain.append(("date", ">=", first_day_of_au_year))
                domain.append(("date", "<=", last_day_of_au_year))

            # Handle "last_au_year" (July 1, 2023 - June 30, 2024)
            elif data.get("date") == "last_au_year":
                first_day_of_last_au_year = datetime(today.year - 1, 7, 1, 0, 0, 0)
                first_day_of_last_au_year = first_day_of_last_au_year - timedelta(hours=timezone)
                
                last_day_of_last_au_year = datetime(today.year, 6, 30, 23, 59, 59)
                last_day_of_last_au_year = last_day_of_last_au_year - timedelta(hours=timezone)
                
                if domain:
                    domain.insert(0, '&')
                domain.append(("date", ">=", first_day_of_last_au_year))
                domain.append(("date", "<=", last_day_of_last_au_year))

            # Handle "this_nz_year" (April 1, 2024 - March 31, 2025)
            elif data.get("date") == "this_nz_year":
                first_day_of_nz_year = datetime(today.year, 4, 1, 0, 0, 0)
                first_day_of_nz_year = first_day_of_nz_year - timedelta(hours=timezone)
                
                last_day_of_nz_year = datetime(today.year + 1, 3, 31, 23, 59, 59)
                last_day_of_nz_year = last_day_of_nz_year - timedelta(hours=timezone)
                
                if domain:
                    domain.insert(0, '&')
                domain.append(("date", ">=", first_day_of_nz_year))
                domain.append(("date", "<=", last_day_of_nz_year))

            # Handle "last_nz_year" (April 1, 2023 - March 31, 2024)
            elif data.get("date") == "last_nz_year":
                first_day_of_last_nz_year = datetime(today.year - 1, 4, 1, 0, 0, 0)
                first_day_of_last_nz_year = first_day_of_last_nz_year - timedelta(hours=timezone)
                
                last_day_of_last_nz_year = datetime(today.year, 3, 31, 23, 59, 59)
                last_day_of_last_nz_year = last_day_of_last_nz_year - timedelta(hours=timezone)
                
                if domain:
                    domain.insert(0, '&')
                domain.append(("date", ">=", first_day_of_last_nz_year))
                domain.append(("date", "<=", last_day_of_last_nz_year))


                if data.get("state"):
                    if domain:
                        domain.insert(0, '&')
                    domain.append(("state", "in", data.get("state")))

        if domain:
            _logger.info(domain)
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
                            if isinstance(getattr(activity, item_split[0]), datetime):
                                datetime_data = getattr(activity, item_split[0]) + timedelta(hours=timezone)
                                activity_data[item] = datetime_data.strftime('%Y-%m-%d %H:%M:%S')
                            elif isinstance(getattr(activity, item_split[0]), date):
                                activity_data[item] = getattr(activity, item_split[0]).strftime('%Y-%m-%d')
                            else :
                                activity_data[item] = getattr(activity, item_split[0])

                response.append(activity_data)
            
        return response