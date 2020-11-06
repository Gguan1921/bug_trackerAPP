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
    email = db.StringField(required = True, unique = True)

    ticket_list = db.ListField(db.ReferenceField('ticket.Ticket', DBref = False),  required = False)

    meta = {
        'abstract':True,
        'allow_inheritance': True,
    }

    # def get_name(self):
    #     pass
    #     return self.name
    #
    # def change_password(self, old_pwd, new_pwd):
    #     if old_pwd == self.password:
    #         self.password = new_pwd
    #
    # def sbumit_ticket (self, ticket):
    #     pass


class Developer(People):
    # Project_ids = db.ListField(db.ReferenceField(project))(required = False)


    def submit_ticket(self, title, comment, priority):
        ticket_buffer = ticket.Ticket(
            title = title,
            comment = comment,
            priority = priority,
            creater = self
        ).save()

        self.ticket_list.append(ticket_buffer)
        self.save()
        pass


    meta = {
        'db_alias': 'core',
        'collection':'People',
        'indexes':["username", "email"],
        'ordering': ["-register_date"]
    }



# class Admin(People):
#
#     def submit_ticket(self, ticket):
#         # make it submit all tickets
#         # make it only submit feature ticket
#         pass
#
#     meta = {
#         'db_alias': 'core',
#         'collection':'People',
#         'indexes':["username", "email"],
#         'ordering': ["-register_date"]
#     }

