from odoo import http
from odoo.addons.portal.controllers import portal


class Controller(http.Controller):

    # For books
    @http.route("/library/books", auth="public", website=True)
    def display_books(self):
        books = http.request.env["library.book"].search([])
        return http.request.render("library.portal_library_books", {
            "books": books
        })

    @http.route("/library/books/<model('library.book'):book>", auth="public", website=True)
    def display_book_detail(self, book):
        return http.request.render("library.book_detail", {
            "book": book
        })

    # For Calendar
    @http.route("/calendar/events", auth="public", website=True)
    def display_events(self):
        events = http.request.env["calendar.event"].search([])
        return http.request.render("library.doc_calendar_event_details_template", {
            "events": events
        })

    @http.route("/calendar/events/<model('calendar.event'):event>", auth="public", website=True)
    def display_event_detail(self, event):
        return http.request.render("library.calendar_event_details_template", {
            "event": event
        })


class LibraryCustomerPortal(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super(LibraryCustomerPortal, self)._prepare_home_portal_values(counters)
        count_books = http.request.env["library.book"].search_count([])
        values.update({
            "count_books": count_books,
        })
        return values


class CalendarCustomerPortal(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super(CalendarCustomerPortal, self)._prepare_home_portal_values(counters)
        count_events = http.request.env["calendar.event"].search_count([])
        values.update({
            "count_events": count_events,
        })
        return values
