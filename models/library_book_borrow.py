from odoo import api, models, fields, exceptions
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

from odoo.odoo.exceptions import UserError

class LibraryBookBorrow(models.Model):
    _name = "library.book.borrow"
    _description = "Library book borrow"

    name = fields.Many2one("library.book", string="Knyga", required=True)
    serial_num = fields.Char(related="name.book_id", string="Serijos numeris", readonly=True, required=True)
    customer_id = fields.Many2one("res.partner", string="Klientas", required=True)
    borrow_date = fields.Date(string="Pasiėmimo data", default=fields.Date.today(), required=True)
    return_date = fields.Date(string="Grąžinimo data",
                              default=lambda self: (datetime.now() + timedelta(days=31)).date(), required=True)
    days = fields.Integer(string="Viso dienų", compute="get_days")
    event_id = fields.Many2one("calendar.event", string="Įvykis")
    state = fields.Selection([("draft", "Draft"), ("confirmed", "Confirmed"), ("rejected", "Rejected")], "State",
                             default="draft", readonly=True)

    @api.constrains('borrow_date', 'return_date')
    def check_dates(self):
        if self.borrow_date > self.return_date:
            raise ValidationError("Dėmesio! Klaidinga Pasiėmimo data")

    @api.depends('borrow_date', 'return_date')
    def get_days(self):
        for req in self:
            req.days = (req.return_date - req.borrow_date).days

    def to_confirm(self):
        self.write({"state": "confirmed"})
        self.send_mesage_to_customer()

    def to_reject(self):
        self.write({"state": "rejected"})

    def to_draft(self):
        self.write({"state": "draft"})

    # Creating event in calendar
    @api.model
    def create(self, vals):
        if "calendar.event" in self.env:
            borrow = super(LibraryBookBorrow, self).create(vals)
            if borrow.borrow_date and borrow.return_date:
                book_name = borrow.name.name.name
                event = self.env["calendar.event"].create({
                    "name": book_name,
                    "start": borrow.borrow_date,
                    "stop": borrow.return_date,
                    "partner_ids": [(6, 0, [borrow.customer_id.id])],
                })
                borrow.event_id = event.id
            return borrow
        else:
            raise exceptions.UserError("The calendar module is not installed!")

    def send_mesage_to_customer(self):
        msg_subject = "Knygos priskyrimas"
        msg_body = f"Knyga <strong>{self.name.name.name}</strong> buvo priskirta jums. Ją grąžinti reikia iki <strong>{self.return_date}</strong>"
        partner_id = self.customer_id.id
        self.env["mail.message"].create({
            "model": "res.partner",
            "res_id": partner_id,
            "message_type": 'comment',
            "subject": msg_subject,
            "body": msg_body
        })

    def unlink(self):
        for record in self:
            if record.event_id:
                record.event_id.unlink()
        return super(LibraryBookBorrow, self).unlink()

