from odoo import api, models, fields
from datetime import datetime, timedelta


class LibraryBook(models.Model):
    _name = "library.book"
    _description = "Library Book"

    name = fields.Many2one('product.product', string="Knygos pavadinimas", required=True)
    author = fields.Char(string="Autorius")
    book_id = fields.Char(string="Serijos numeris", required=True, copy=False, readonly=True, default="BKxxxxx")
    description = fields.Text(string="Knygos aprašymas")
    quantity = fields.Integer(string="Likutis", required=True)
    allowed_period = fields.Integer(string="Leidžiama pasiėmimo trukmė (dienomis)", default=31)
    state = fields.Selection([("draft", "Draft"), ("confirmed", "Confirmed"), ("rejected", "Rejected")], "State",
                             default="draft", readonly=True)

    def to_confirm(self):
        self.write({"state": "confirmed"})

    def to_reject(self):
        self.write({"state": "rejected"})

    def to_draft(self):
        self.write({"state": "draft"})

    @api.model
    def create(self, vals):
        vals['book_id'] = self.env['ir.sequence'].next_by_code('library.book')
        res = super(LibraryBook, self).create(vals)
        return res
