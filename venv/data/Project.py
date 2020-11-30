import mongoengine as db
import datetime
import Ticket

class Project(db.Document):
    birthday = db.DateTimeField(default = datetime.datetime.now)
    title = db.StringField(required = True)
    description = db.StringField(required = True)
    comment = db.StringField()
    complete = db.BooleanField(required = True, default = False)
    required_ticket = db.ListField(db.ReferenceField('Ticket.Ticket'))
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
