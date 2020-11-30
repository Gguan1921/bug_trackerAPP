# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import mongoengine as db
import os
import json
import datetime

class Ticket (db.EmbeddedDocument):
    birthday = db.DateTimeField(default = datetime.datetime.now)
    assigned_to_person = db.ReferenceField('People', required = True, DBref = False)
    title = db.StringField(required = True)
    comment = db.ListField(db.StringField(required = True))
    priority = db.IntField(required = True, max_value = 10, min_value = 1)
    creater = db.ReferenceField('People', required = True, DBref = False)
    compeleted = db.BooleanField(default = False)
    meta = {
        'allow_inheritance': True,
        'db_alias': 'core',
        'collection':'Ticket',
        'indexes':["title", "id"],
        'ordering': ["-birthday"]
    }

class Feature_ticket (Ticket):
    pass

class Bug_ticket (Ticket):
    pass

class Project(db.Document):
    birthday = db.DateTimeField(default = datetime.datetime.now)
    title = db.StringField(required = True)
    description = db.StringField(required = True)
    comment = db.StringField()
    complete = db.BooleanField(required = True, default = False)
    required_ticket = db.ListField(db.EmbeddedDocumentField('Ticket'))
    team = db.ReferenceField('Team')

    def edit_comment(self, comment):
        self.comment = comment

    def add_ticket(self, ticket):
        self.required_ticket.append(ticket)
        self.save()

    def delete_ticket(self, ticket):
        if ticket in self.required_ticket:
            self.required_ticket.remove(ticket)

        # ticket_num = len(self.required_ticket)
        #
        # for i in range(ticket_num):
        #     if cls.required_ticket[i] == ticket:
        #         cls.required_ticket.pop(i)

    meta = {
        'allow_inheritance': True,
        'db_alias': 'core',
        'collection': 'Projects',
        'indexes':["title"],
        'ordering':["-birthday"]
    }

class Team (db.Document):
    name = db.StringField(required = True, unique = True)
    birthday = db.DateTimeField(default = datetime.datetime.now)
    member = db.ListField(db.ReferenceField('People'))
    project = db.ListField(db.ReferenceField('Project'))
    admin = db.ListField(db.ReferenceField('Admin'))

    def assign_project_to_team(self, project):
      self.project.append(project)

    def add_people_to_team(self, people):
      #have to find the people object in DB and add into the team object
      if people not in self.member:
          self.member.append(people)

    def transfer_people_to_team(self, target, people):
      #tranfer a person from source team to target team
      if people in self.member:
          self.member.remove(people)
      # else:
      #     raise Exception("{} is not found in the team: {}".format(people.first_name + ' ' + people.last_name, self.name))
          target.member.append(people)

    meta = {
        'allow_inheritance': True,
        'db_alias': 'core',
        'collection':'Teams',
        'indexes':["name"]
    }

class People(db.Document):

    register_date = db.DateTimeField(default = datetime.datetime.now)
    first_name = db.StringField(required = True)
    last_name = db.StringField(required = True)
    username = db.StringField(required = True, unique = True)
    password = db.StringField(required = True)
    email = db.EmailField(required = True, unique = True)
    team = db.ListField(db.ReferenceField('Team', DBref = False))
    project = db.ListField(db.ReferenceField('Project'))
    ticket_list = db.ListField(db.EmbeddedDocumentField('Ticket', DBref = False),  required = False)
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

    def submit_ticket(self, title, comment, priority):
        ticket_buffer = Ticket.Ticket(
            title = title,
            comment = comment,
            priority = priority,
            creater = self
        )

        self.ticket_list.append(ticket_buffer)

    def Developer_menu(self):
        option_D = 1
        result = None
        while int(option_D) > 0 or int(option_D) < 5:
            print()
            print("1. Display your teams.")
            print("2. Display your projects.")
            print("3. Display your tickets.")
            print("4. Create new tickets.")
            print("5. Exit")
            option_D = input("Enter 1, 2, 3, 4, or 5\n")
            if option_D == '1':
                # print(db.People().find({}, {name: 1, admin: 1, _id: 0}))
                #view team (only see the teams he joined in)
                if self.team == []:
                    print("You haven't been in any teams.")
                    continue
                for team in self.team:
                    print(team.to_json(indent=4))
                continue
            if option_D == '2':
                #view project -> display_project
                if self.project == []:
                    print("You haven't had any projects.")
                    continue
                for project in self.project:
                    print(project.to_json(indent=4))
                    print()
            if option_D == '3':
                #view ticket -> display_ticket
                if self.ticket_list == []:
                    print("You don't have any tickets")
                    continue
                for ticket in self.ticket_list:
                    print(ticket.to_json(indent=4))
                    print()
            if option_D == '4':
                #create_ticket(let the user to choose which project to add in)
                project = input("Which project do you want to add ticket in? Type in Project _id:\n")
                while (len(Project.objects(pk = project)) == 0):
                    print("Unmatched project_id")
                    project = input("Which project do you want to add ticket in? Type in Project _id:\n")
                project_buffer = Project.objects(pk = project)
                project_buffer = project_buffer[0]
                title = input("What is the title of this ticket?\n")
                comment = input("What is the comment you want to add in?\n")

                while True:
                    try:
                        priority = int(input("What is the priority of this ticket?\n"))
                        while priority > 10 or priority < 1:
                            priority = int(input("Enter an integer from 1 to 10:"))
                        break
                    except ValueError:
                        print("Enter an integer from 1 to 10:")

                assigned_to_person = input("Which person(username) are you going to assign this ticket?\n")
                while len(People.objects(username = assigned_to_person)) == 0:
                    print("Unmatched registered username.")
                    assigned_to_person = input("Which person(username) are you going to assign this ticket?\n")
                assigned_to_person_buffer = People.objects(username = assigned_to_person)
                assigned_to_person_buffer = assigned_to_person_buffer[0]

                new_ticket = Ticket(
                    title = title,
                    comment = comment,
                    priority = priority,
                    assigned_to_person = assigned_to_person_buffer,
                    creater = self
                )
                project_buffer.required_ticket.append(new_ticket)
                project_buffer.save()
                assigned_to_person.ticket_list.append(new_ticket)
                assigned_to_person.save()

    def create_ticket(self, project, ticket):
        pass

    meta = {
        'db_alias': 'core',
        'collection':'People',
        'indexes':["username", "email"],
        'ordering': ["-register_date"]
    }

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

    def Admin_menu(self):
        result = None
        while True:
            print()
            print("Admin Menu")
            print("1. Check who is not in any teams yet.")
            print("2. View all teams.")
            print("3. View all projects.")
            print("4. View all tickets.")
            print("5. Create a new team")
            print("6. Assign project to team")
            print("7. Exit")
            option_A = input("Enter 1, 2, 3, 4, 5, or 6\n")
            if option_A == '1':
                #check who is not in any teams yet.
                result = People.objects(team = [])
                if result == []:
                    print("Everyone has been assigned to teams\n")
                    continue
                for person in result:
                    print()
                    person.display_people()
                print("1. Assign people to teams")
                print("2. Go back to Menu")
                option_A1 = input("Enter 1 or 2\n")
                if option_A1 == "2":
                    continue
                elif option_A1 == "1":
                    person_username = input("Enter this person's username: ")
                    while len((People.objects(username = person_username)) == 0):
                        print("Unmatched registered username.")
                        person_username = input("Enter this person's username: ")
                    person = People.objects(username = person_username)
                    person = person[0]
                    team_name = input("Enter the team name to join in: ")
                    if Team.objects() == None:
                        print("No teams have been created.")
                        continue
                    while len((Team.objects(name = team_name)) == 0):
                        print("Unmatched team name.")
                        team_name = input("Enter the team name to join in: ")
                    team = Team.objects(name = team_name)
                    team = team[0]
                    if person not in team.member:
                        team.member.append(person)
                        person.team.append(team)
                        print(person.to_json(indent=4))
                        print("User: ", person.username, " is now assigned to team: ", team.name)
                        continue
                    else:
                        break

                else:
                    continue
            elif option_A == '2':
                #view team (see all teams)
                if Team.objects() == None:
                    print("No team has been created.")
                    continue
                else:
                    for team in Team.objects():
                        print(team.to_json(indent=4))
                        print()
                    continue
            elif option_A == '3':
                #view all projects -> display_project
                if Project.objects() == None:
                    print("No project exists")
                    continue
                else:
                    for project in Project.objects():
                        print(project.to_json(indent=4))
                        print()

            elif option_A == '4':
                #view ticket -> display_ticket
                for project in Project.objects():
                    if project.required_ticket == []:
                        continue
                    else:
                        for ticket in project.required_ticket:
                            print(ticket.to_json(indent=4))
                            print()

            elif option_A == '5':
                #create team
                new_name = input("\nEnter a name for this team: ")
                while len(Team.objects(name = new_name)) != 0:
                    print("duplicated team name")
                    new_name = input("Enter a name for this team: ")

                member_list = []
                person_username = input("Add a person(username) to this team: ")
                while len(People.objects(username = person_username)) == 0:
                    print("Unmatched registered username.")
                    person_username = input("Add a person(username) to this team: ")
                person = People.objects(username = person_username)
                person = person[0]
                if person in member_list:
                    print("This person has been added to this team.")
                    continue
                member_list.append(person)

                project_list = []
                project = input("Add a project(Project_ids) to this team: ")
                while len(Project.objects(pk = project)) == 0:
                    print("Unmatched project _id.")
                    project = input("Add a project(Project_ids) to this team: ")
                project_buffer = Project.objects(pk = project)
                project_buffer = project_buffer[0]
                if project_buffer.team != None:
                    print("This project has already been assigned to another team.")
                else:
                    project_list.append(Project.objects(pk = project))
                # while True:
                #     project = input("Add a project(Project_ids) to this team: ")
                #     elif project == Project.objects(_id = project)._id:
                #         while Project.objects(_id = project).team != None:
                #             print("This project has already been assigned to another team.")
                #             project = input("(Press \"return\" to go back. Add another project(Project_ids) to this team: ")
                #             if project == '\n':
                #                 break
                #         project_list.append(Project.objects(_id = project))
                    # else:
                    #     print("Unmatched Project_id.")
                admin_list = []
                admin = input("Add an Admin(username) to this team: ")
                while len(Admin.objects(username = admin)) == 0:
                    print("Unmatched Admin username.")
                    admin = input("Add an Admin(username) to this team: ")
                admin_buffer = Admin.objects(username = admin)
                admin_buffer = admin_buffer[0]
                admin_list.append(admin_buffer)

                new_team = Team (
                    name = new_name,
                    member = member_list,
                    project = project_list,
                    admin = admin_list
                ).save()
                for people in member_list:
                    people.team.append(new_team).save()
                if project_list != []:
                    for project in project_list:
                        project.team = new_team.save()
            elif option_A == '6':
                #assign_project_to_team -> Team.assigned_to_team
                project = input("Enter the Project_id: ")
                while (len(Project.objects(pk = project)) == 0):
                    print("Unmatched project _id.")
                    project = input("Add a project(Project_ids) to this team: ")
                project_buffer = Project.objects(pk = project)
                project_buffer = project_buffer[0]
                if len(project_buffer.team) != 0:
                    print("This project has already been assigned to another team.")
                else:
                    team = input("Enter the team name: ")
                    while (len(Team.objects(name = team)) == 0):
                        print("Unmatched team name.")
                        team = input("Enter the team name: ")
                    team_buffer = Team.objects(name = team)
                    team_buffer = team_buffer[0]

                    #save into this team
                    team_buffer.append(project_buffer).save()
                    #save into all team members
                    for people in team_buffer.member:
                        people.project.append(project_buffer).save()

            elif option_A == '7':
                break

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

def global_init():
    username = "gguan"
    password = "gx398175"
    db_name = "Bug-tracker"

    db_dui = "mongodb+srv://{}:{}@cluster0.axsfc.mongodb.net/{}?retryWrites=true&w=majority".format (username, password, db_name)
    print (db_dui)
    db.connect(alias = 'core', host = db_dui)

def start_menu():
    option = -1
    result = None
    while int(option) < 1 or int(option) > 2:
        print()
        print ('1.Register new user')
        print ('2.Sign in')
        print ('3.Exit')
        option = input("Enter 1, 2, or 3.\n")
        if option == '1':
            result = register()
            if result != None:
                return result
        elif option == '2':
            result = sign_in()
            if result != None:
                return result
        elif option == '3':
            return None



def register():
    people_buf = Admin()

    username = input('\nRegistration Page.\nPlease enter username (enter exit to quit): ')
    if (username == 'exit'):
        return None;

    while(people_buf.people_search(username = username) != None):
        print("duplicated username!")
        username = input('Please enter username: ')

    password = input('Please enter password: ')
    password_confirm = input('Please confirm password: ')
    while password != password_confirm:
        password = input('Please enter password: ')
        password_confirm = input('Please confirm password: ')

    email = input('Please enter email: ')
    while(people_buf.people_search(email = email) != None):
        print("duplicate email!")
        email = input('Please enter email: ')
    first_name = input('Please enter your first name:')
    last_name = input('Please enter your last name:')
    option = input('Please choose your role\n1. Dev\n2. Admin\n')
    while int(option) < 1 or int(option) > 2:
        print ('Please enter 1 or 2')
        option = input('Please choose your role\n1. Dev\n2. Admin\n')


    if option == '1':
        new_employee = people.Developer (
        username = username,
        email = email,
        password = password,
        first_name = first_name,
        last_name = last_name,
        title = "Developer"
        ).save()
    elif option == '2':
        new_employee = people.Admin (
        username = username,
        email = email,
        password = password,
        first_name = first_name,
        last_name = last_name,
        title = "Admin"
        ).save()

    return new_employee

def sign_in():

    username = input('\nSign in Page.\nPlease enter username (enter exit to quit): ')
    if (username == 'exit'):
        return None;

    while(len(People.objects(username = username)) == 0):
        print("Unregistered username!")
        username = input('Please enter username: ')
    #print(People.objects(username = username))
    buffer = People.objects(username = username)
    password = input('Please enter password: ')
    buffer = buffer[0]
    count = 5
    while (buffer.password != password):
        count = count - 1
        if count == 0:
            print("Unable to log in.")
            return None
        print("Password fails. Unable to sign in.")
        password = input(str(count) + "times left. Please re-enter password:")

    return buffer
# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    global_init()

    project = Project(
        title = "Term Project",
        description = "Fall 2020 CIS 407",
        comment = "Mongodb"
    )

    project = Project(
        title = "Term Project1",
        description = "Fall 2020 CIS 407(1)",
        comment = "Mongodb(1)"
    )
    #print(Project.objects(pk='5fc49c0d730c819fb0d19372').to_json(indent=4))

    employee = start_menu()
    if employee != None:
        employee.display_people()
        if employee.title == "Developer":
            employee.Developer_menu()
        if employee.title == "Admin":
            employee.Admin_menu()
    # employee1 = people.Admin()
    #
    # emp_list = employee1.people_search(last_name='guan')
    # for employee in emp_list:
    #     employee.display_people()
    #
    # print('Search Xin')
    #
    # emp_list = employee1.people_search(first_name='jklg')
    # if (emp_list != None):
    #     for employee in employee1.people_search(first_name='jklg'):
    #         employee.display_people()

    db.disconnect(alias='core')
