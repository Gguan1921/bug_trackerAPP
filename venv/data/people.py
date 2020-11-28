import mongoengine as db
import datetime
import Ticket
import os


class People(db.Document):
    import team
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
        print("username: {}".format(self.username))
        print("first_name: {}".format(self.first_name))
        print("last_name: {}".format(self.last_name))

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

    def people_search(self, first_name=None, last_name=None):
        if first_name is None and last_name is None:
            print("No parameter entered.")
            return None
        elif first_name is None:
            return People.last_name.search_text(last_name).order_by('$text_score')
        else:
            return People.first_name.search_text(first_name).order_by('$text_score')

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
