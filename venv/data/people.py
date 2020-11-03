import mongoengine as db
import datetime
import data.Ticket as ticket


class People(db.EmbeddedDocument):
    registered_date = db.DateTimeField(default = datetime.datetime.now)
    birthday = db.DateTimeField(required = True)
    name = db.StringField(required = True)
    username = db.StringField(required = True)
    password = db.StringField(required = True)

    Ticket_ids = db.EmbeddedDocumentListField(ticket)(required = False)
    db.ReferenceField
    Project_ids = db.ListField(required = False)

    meta = {'allow_inheritance': True}

    # def get_name(self):
    #     return self.name
    #
    # def change_password(self, old_pwd, new_pwd):
    #     if old_pwd == self.password:
    #         self.password = new_pwd
    #
    # def sbumit_ticket (self, ticket):
    #     pass


class Developer(People):
    def __init__(self, name, username, password):
        super().__init__(name, username, password)
        self.team = []

    def submit_ticket(self, ticket):
        #make it submit all tickets
        pass


class Admin(People):
    def __init__(self, name, username, password):
        super().__init__(name, username, password)
        self.feature_tickets = []
        self.employee = []

    def submit_ticket(self, ticket):
        # make it submit all tickets
        # make it only submit feature ticket
        pass
