from odoo import exceptions
from odoo.tests.common import TransactionCase


class TestWizard(TransactionCase):
    def setUp(self):
        super().setUp()
        admin_user = self.env.ref("base.user_admin")
        self.Checkout = self.env["library.checkout"].sudo(admin_user)
        self.Wizard = self.env["library.checkout.massmessage"].sudo(admin_user)
        a_member = self.env["library.member"].create({"name": "Test Member"})
        self.checkout0 = self.Checkout.create({"member_id": a_member.id})
        self.Wizard0 = self.Wizard.with_context(active_ids=self.checkout0.ids)

    def test_button_send(self):
        """Send button should create messages on Checkouts"""
        msgs_before = len(self.checkout0.message_ids)
        wizard0 = self.Wizard0.create({"message_body": "Hello"})
        wizard0.button_send()

        msgs_after = len(self.checkout0.message_ids)
        self.assertEqual(
            msgs_after,
            msgs_before + 1,
            "Expected one additional message in the Checkout",
        )

    def test_button_send_empty_body(self):
        """Send button errors on empty body message"""
        wizard0 = self.Wizard0.create({"message_body": ""})
        with self.assertRaises(exceptions.UserError):
            wizard0.button_send()
