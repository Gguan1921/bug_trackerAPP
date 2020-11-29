import mongoengine as db
import datetime
import data.Ticket as ticket
import data.Project as porject
import json
import os
import data.team as team

class People(db.Document):

    register_date = db.DateTimeField(default = datetime.datetime.now)
    first_name = db.StringField(required = True)
    last_name = db.StringField(required = True)
    username = db.StringField(required = True, unique = True)
    password = db.StringField(required = True)
    email = db.StringField(required = True, unique = True)
    team = db.ListField(db.ReferenceField('team.Team', DBref = False))
    project = db.ListField(db.ReferenceField('Project.Project'))
    ticket_list = db.ListField(db.ReferenceField('ticket.Ticket', DBref = False),  required = False)

    def assign_project_to_people(self, project):
        self.project.append(project)

    def display_people(self):
        if self is None:
            print ('nothing is display')
        print("username: {}".format(self.username))
        print("first_name: {}".format(self.first_name))
        print("last_name: {}".format(self.last_name))

    meta = {
        'allow_inheritance': True,
        'db_alias': 'core',
        'collection': 'People',
        'indexes': ["username", "email"],
        'ordering': ["-register_date"]
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
        ticket_buffer = Ticket.Ticket(
            title = title,
            comment = comment,
            priority = priority,
            creater = self
        )#.save()

        self.ticket_list.append(ticket_buffer)
        # self.save()
        # pass


    meta = {
        'db_alias': 'core',
        'collection':'People',
        'indexes':["username", "email"],
        'ordering': ["-register_date"]
    }

# employee1 = People(first_name = "yuyao",last_name = "zhuge",username = "yzhuge",password = "9801",email = "gmail.com")
# print(employee1.email)

class Admin(People):

    def people_search(self, first_name='', last_name='', username = '', email = ''):
        buffer = None

        if first_name == last_name == username == email =='':
            print("No parameter entered.")
            return None
        elif username != '':
            buffer = People.objects(username = username)
        elif email != '':
            buffer = People.objects(email=email)
        elif first_name != '' and last_name != '':
            buffer = People.objects(first_name = first_name, last_name = last_name)
        elif first_name =='' and last_name != '':
            buffer = People.objects(last_name = last_name)
        elif last_name == '' and first_name != '':
            buffer = People.objects(first_name = first_name)

        if len(buffer) == 0:
            return None

        return buffer

    def submit_ticket(self, ticket):
        # make it submit all tickets
        # make it only submit feature ticket
        pass

    meta = {
        'db_alias': 'core',
        'collection':'People',
        'indexes':["username", "email"],
        'ordering': ["-register_date"]
    }