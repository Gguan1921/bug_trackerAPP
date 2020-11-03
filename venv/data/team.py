from people.py import People


class Team:
    def __init__(self, num_members = 0, admin = None, dev_lead = None, team_member = []):
        self.num_crewmate = num_members
        self.admin = admin
        self.developer_lead = dev_lead
        self.team_member = []

        meta = {
            'db_alias': 'core',
            'collection': 'team'
        }

    def add_people_to_team(cls, name):
        #have to find the people object in DB and add into the team object


    def transfer_people_to_team(target, source, name):
        #tranfer a people from source team to target team



