import mongoengine as db
import datetime
import Ticket
import Project
import json
import os
import team

class People(db.Document):

    register_date = db.DateTimeField(default = datetime.datetime.now)
    first_name = db.StringField(required = True)
    last_name = db.StringField(required = True)
    username = db.StringField(required = True, unique = True)
    password = db.StringField(required = True)
    email = db.EmailField(required = True, unique = True)
    team = db.ListField(db.ReferenceField('team.Team', DBref = False))
    project = db.ListField(db.ReferenceField('Project.Project'))
    ticket_list = db.ListField(db.ReferenceField('ticket.Ticket', DBref = False),  required = False)
    title = db.StringField(required = True)

    def assign_project_to_people(self, project):
        self.project.append(project)

    def display_people(self):
        if self is None:
            print ('nothing is display')

        print(self.to_json(indent=4))
        # print("username: {}".format(self.username))
        # print("first_name: {}".format(self.first_name))
        # print("last_name: {}".format(self.last_name))

    def change_password(self, old_pwd, new_pwd):
        if old_pwd == self.password:
            self.password = new_pwd

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

    def Developer_menu(self):
        option = -1
        result = None
        while int(option) < 1 or int(option) > 2:
            print()
            print("1. Display your teams.")
            print("2. Display your projects.")
            print("3. Display your tickets.")
            print("4. Create new tickets.")
            option = input("Enter 1, 2, 3, or 4\n")
            if option == '1':
                # print(db.People().find({}, {name: 1, admin: 1, _id: 0}))
        #view team (only see the teams he joined in)
                for team in self.team:
                    print(json.dumps(team, indent=4))
        #view project -> display_project
        #view ticket -> display_ticket
        #create_ticket(let the user to choose which project to add in)


    def create_ticket(self, project, ticket):
        pass

    meta = {
        'db_alias': 'core',
        'collection':'People',
        'indexes':["username", "email"],
        'ordering': ["-register_date"]
    }

# employee1 = People(first_name = "yuyao",last_name = "zhuge",username = "yzhuge",password = "9801",email = "gmail.com")
# print(employee1.email)

# employee = People.objects(username = "yzhuge")
# employee.display_people()

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

    def display_teams(self):
        if team.Team.objects(name) is None:
            print("Nothing to display.")
        else:
            for i in team.Team.objects:
                pass
    def Admin_menu(self):

        option = -1
        result = None
        while int(option) < 1 or int(option) > 2:
            print()
            print("1. Check who is not in any teams yet.")
            print("2. Display your projects.")
            print("3. Display your tickets.")
            print("4. Create new tickets.")
            option = input("Enter 1, 2, 3, or 4\n")
            if option == '1':
                result = People.objects(team = [])
                if result == []:
                    print("Everyone has been assigned to teams\n")
                    continue
                for person in result:
                    print()
                    person.display_people()
                print("1. Assign people to teams")
                print("2. Go back to Menu")
                option1 = input("Enter 1 or 2\n")
                if option1 == "1":
                    person_username = input("Enter this person's username: ")
                    while (People.objects(username = person_username) == None):
                        print("Unmatched registered username.")
                        person_username = input("Enter this person's username: ")
                    person = People.objects(username = person_username)
                    person = person[0]
                    team_name = input("Enter the team name to join in: ")
                    team = Team.objects(name = team_name)
                    team = team[0]
                    if person not in team.member:
                        team.member.append(person)
                    else:
                        print("User: ", person)
        #check who is not in any teams yet.
        #view team (see all teams)
        #view project -> display_project
        #view ticket -> display_ticket
        #create team
        #assign_project_to_team -> Team.assigned_to_team


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
