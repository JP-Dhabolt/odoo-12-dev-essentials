from odoo import api
from odoo import exceptions
from odoo import fields
from odoo import models

stage_model = "library.checkout.stage"


class Checkout(models.Model):
    _name = "library.checkout"
    _description = "Checkout Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    member_id = fields.Many2one("library.member", required=True)
    user_id = fields.Many2one("res.users", "Librarian", default=lambda s: s.env.uid)
    request_date = fields.Date(default=lambda s: fields.Date.today())
    line_ids = fields.One2many(
        "library.checkout.line", "checkout_id", string="Borrowed Books"
    )
    checkout_date = fields.Date(readonly=True)
    closed_date = fields.Date(readonly=True)
    member_image = fields.Binary(related="member_id.partner_id.image")
    num_other_checkouts = fields.Integer(compute="_compute_num_other_checkouts")
    num_books = fields.Integer(compute="_compute_num_books", store=True)
    color = fields.Integer("Color Index")
    priority = fields.Selection(
        [("0", "Low"), ("1", "Normal"), ("2", "High")], "Priority", default="1"
    )
    kanban_state = fields.Selection(
        [
            ("normal", "In Progress"),
            ("blocked", "Blocked"),
            ("done", "Ready for the next stage"),
        ],
        "Kanban State",
        default="normal",
    )

    @api.model
    def create(self, vals):
        # Code before create: should use the `vals` dict
        if "stage_id" in vals:
            Stage = self.env[stage_model]
            new_state = Stage.browse(vals["stage_id"]).state
            if new_state == "open":
                vals["checkout_date"] = fields.Date.today()
        new_record = super().create(vals)
        # Code after create: can use the `new_record` created
        if new_record.state == "done":
            raise exceptions.UserError(
                "Not allowed to create a checkout in the done state"
            )
        return new_record

    @api.multi
    def write(self, vals):
        # Code before write: can use `self`, with the old values
        if "stage_id" in vals:
            Stage = self.env[stage_model]
            new_state = Stage.browse(vals["stage_id"]).state
            if new_state == "open" and self.state != "open":
                vals["checkout_date"] = fields.Date.today()
            if new_state == "done" and self.state != "done":
                vals["closed_date"] = fields.Date.today()
        super_return = super().write(vals)
        # Code after write: can use `self`, with the updated values
        return super_return

    @api.model
    def _default_stage(self):
        Stage = self.env[stage_model]
        return Stage.search([], limit=1)

    @api.model
    def _group_expand_stage_id(self, stages, domain, order):
        return stages.search([], order=order)

    stage_id = fields.Many2one(
        stage_model, default=_default_stage, group_expand="_group_expand_stage_id"
    )
    state = fields.Selection(related="stage_id.state")

    @api.onchange("member_id")
    def onchange_member_id(self):
        today = fields.Date.today()
        if self.request_date != today:
            self.request_date = fields.Date.today()
            return {
                "warning": {
                    "title": "Changed Request Date",
                    "message": "Request date changed to today.",
                }
            }

    def button_done(self):
        Stage = self.env[stage_model]
        done_stage = Stage.search([("state", "=", "done")], limit=1)
        for checkout in self:
            checkout.stage_id = done_stage
        return True

    def _compute_num_other_checkouts(self):
        for checkout in self:
            domain = [
                ("member_id", "=", checkout.member_id.id),
                ("state", "in", ["open"]),
                ("id", "!=", checkout.id),
            ]
            checkout.num_other_checkouts = self.search_count(domain)

    @api.depends("line_ids")
    def _compute_num_books(self):
        for checkout in self:
            checkout.num_books = len(checkout.line_ids)


class CheckoutLine(models.Model):
    _name = "library.checkout.line"
    _description = "Borrow Request Line"

    checkout_id = fields.Many2one("library.checkout")
    book_id = fields.Many2one("library.book")
