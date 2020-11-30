import mongoengine as db
import people
import datetime

class Ticket (db.Document):
    birthday = db.DateTimeField(default = datetime.datetime.now)
    assigned_to_person = db.ReferenceField('people.People', required = True, DBref = False)
    title = db.StringField(required = True)
    comment = db.ListField(db.StringField(required = True))
    priority = db.IntField(required = True, max_value = 10, min_value = 1)
    creater = db.ReferenceField('people.People', required = True, DBref = False)
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
