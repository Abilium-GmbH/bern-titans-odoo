
import logging
from contextlib import contextmanager
from functools import wraps
from requests import HTTPError
import pytz
from dateutil.parser import parse

from odoo import api, fields, models, registry, _
from odoo.tools import ormcache_context
from odoo.exceptions import UserError
from odoo.osv import expression

from odoo.addons.google_calendar.utils import google_calendar, google_event
from odoo.addons.google_account.models.google_service import TIMEOUT

_logger = logging.getLogger(__name__)


class GoogleSync(models.AbstractModel):
    _inherit = 'google.calendar.sync'

    #def _sync_odoo2google(self, google_service: google_calendar.GoogleCalendarService):
    #    _logger.info("DO NOT SYNC BACK TO GOOGLE")
    #    return