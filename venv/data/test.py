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
    print(People.objects(username = username))
    while (People.objects(username = username) == []):
        print("Unregistered username!")
        username = input('Please enter username: ')
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
