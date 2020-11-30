import people
import Project
import mongoengine as db
import datetime



class Team (db.Document):
    name = db.StringField(required = True, unique = True)
    birthday = db.DateTimeField(default = datetime.datetime.now)
    member = db.ListField(db.ReferenceField('people.People'))
    project = db.ListField(db.ReferenceField('Project.Project'))
    admin = db.StringField()

    def assign_project_to_team(self, project):
      self.project.append(project)

    def add_people_to_team(self, people):
      #have to find the people object in DB and add into the team object
      if people not in self.member:
          self.member.append(people)
      self.save()

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
