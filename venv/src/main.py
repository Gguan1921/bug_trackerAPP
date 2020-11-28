# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import mongoengine as db
import people
import os
import json
import team
import Project
import Ticket
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
    employee1 = people.Admin()
    employee1.first_name = "yuyao"
    employee1.last_name = "zhuge"
    employee1.username = "yzhuge"
    employee1.password = "yzhuge123456"
    employee1.email = "yzhuge@uoregon.edu"
    employee1.save()


    employee2 = people.Developer (
        username = "gguan",
        email = "gguan@uoregon.edu",
        password = "gguan123456",
        first_name = "xin",
        last_name = "guan",
    ).save()

    employee3 = people.Developer (
        username = "12234",
        email = "1234@gmail.com",
        password = "gguan123456",
        first_name = "grayson",
        last_name = "guan",
    ).save()

    employee4 = people.Developer (
        username = "hellp",
        email = "fkjafds@gmail.com",
        password = "gguan123456",
        first_name = "main",
        last_name = "guan",
    ).save()

    for employee in employee1.people_search(last_name='guan'):
        employee.display_people()

    for employee in employee1.people_search(first_name='xin'):
        employee.display_people()

    db.disconnect(alias='core')
