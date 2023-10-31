{
    "name":"Bibiliotekos Valdymo Sistema",
    "version":"16.0.0.1",
    "author":"Paulius Baksys",
    "summary":"Blbliotekos valdymas",
    "sequence":"1",
    "depends":["base", "website", "product", "portal"],
    "license":"LGPL-3",
    "data":[
        "security/ir.model.access.csv",
        "data/data.xml",
        "views/library_book_views.xml",
        "views/menu.xml",
        "views/library_book_borrow_views.xml",
        "views/book_templates.xml",
        "views/website_menu.xml",
        "views/calendar_template.xml"
    ],
    "installable":True,
    "application": True

}
