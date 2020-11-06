from people.py import People


class Team:
    pass
    meta = {
        'db_alias': 'core',
        'collection': 'teams'
    }

    def add_people_to_team(cls, name):
        #have to find the people object in DB and add into the team object


    def transfer_people_to_team(target, source, name):
        #tranfer a people from source team to target team



