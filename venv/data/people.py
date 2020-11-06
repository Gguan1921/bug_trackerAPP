import mongoengine as db
import datetime
import data.Ticket as ticket
import data.Project as porject
import json
import os


class People(db.Document):
    register_date = db.DateTimeField(default = datetime.datetime.now)
    first_name = db.StringField(required = True)
    last_name = db.StringField(required = True)
    username = db.StringField(required = True, unique = True)
    password = db.StringField(required = True)
    email = db.StringField(required = True)

    def json(self):
        user_dict: {
            "first name": self.first_name,
            "last name": self.last_name,
            "username": self.username,
            "password": self.password,
            "email": self.email,
        }
        return json.dumps(user_dict)

    # Ticket_ids = db.ListField(db.ReferenceField(ticket))(required = False)
    # Project_ids = db.ListField(db.ReferenceField(project))(required = False)

    meta = {
        'db_alias': 'core',
        'collection':'People',
        'allow_inheritance': True,
        'indexes':["username", "email"],
        'ordering': ["-register_date"]
    }

    # def get_name(self):
    #     return self.name
    #
    # def change_password(self, old_pwd, new_pwd):
    #     if old_pwd == self.password:
    #         self.password = new_pwd
    #
    # def sbumit_ticket (self, ticket):
    #     pass


# class Developer(People):
#     def __init__(self, name, username, password):
#         super().__init__(name, username, password)
#         self.team = []
#
#     def submit_ticket(self, ticket):
#         #make it submit all tickets
#         pass
#
#
# class Admin(People):
#     def __init__(self, name, username, password):
#         super().__init__(name, username, password)
#         self.feature_tickets = []
#         self.employee = []
#
#     def submit_ticket(self, ticket):
#         # make it submit all tickets
#         # make it only submit feature ticket
#         pass
