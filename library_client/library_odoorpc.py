from odoorpc import ODOO


class LibraryAPI:
    def __init__(self, srv, port, db, user, pwd):
        self.api = ODOO(srv, port=port)
        self.api.login(db, user, pwd)
        self.uid = self.api.env.uid
        self.model = "library.book"
        self.Model = self.api.env[self.model]

    def search_read(self, text=None):
        domain = [("name", "ilike", text)] if text else []
        fields = ["id", "name"]
        return self.Model.search_read(domain, fields)

    def create(self, title):
        vals = {"name": title}
        return self.Model.create(vals)

    def write(self, title, id):
        vals = {"name": title}
        self.Model.write(id, vals)

    def unlink(self, id):
        return self.Model.unlink(id)
