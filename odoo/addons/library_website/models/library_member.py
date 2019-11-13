from odoo import fields
from odoo import models


class Member(models.Model):
    _inherit = "library.member"
    user_id = fields.Many2one("res.users")
