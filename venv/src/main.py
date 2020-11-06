# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import mongoengine as db
import data.people as people
import os
import json

def global_init():
    username = "gguan"
    password = "gx398175"
    db_name = "Bug-tracker"

    db_dui = "mongodb+srv://{}:{}@cluster0.axsfc.mongodb.net/{}?retryWrites=true&w=majority".format (username, password, db_name)
    print (db_dui)
    db.connect(alias = 'core', host = db_dui)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    global_init()
    user = people.People (
        username = "gguan",
        email = "gguan@uoregon.edu",
        password = "gguan123456",
        first_name = "xin",
        last_name = "guan"
    ).save()

    db.disconnect(alias='core')
    print(user)
    print(user.username)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
