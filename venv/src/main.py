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

def start_menu():
    option = -1
    result = None
    while int(option) < 1 or int(option) > 2:
        print ('1.Register new user')
        print ('2.Sign in')
        print ('3.Exit')
        option = input()
        if option == '1':
            result = register()
            if result != None:
                return result
        elif option == '2':
            pass
        elif option == '3':
            pass



def register():
    people_buf = people.Admin()

    username = input('Please enter username (enter exit to quit): ')
    if (username == 'exit'):
        return None;

    while(people_buf.people_search(username = username) != None):
        print("duplicate username!")
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
    option = input('Please choose your role\n1. Dev\n2. Admin')
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
        ).save()
    elif option == '2':
        new_employee = people.Admin (
        username = username,
        email = email,
        password = password,
        first_name = first_name,
        last_name = last_name,
        ).save()

    return new_employee

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    global_init()

    employee = start_menu()

    employee.display_people()
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