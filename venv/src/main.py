# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import mongoengine as db


import mongoengine


def global_init():
    username = "gguan"
    password = "gx398175"
    db_name = "But_tracker"
    db_dui = "mongodb + srv: // {}: {}@cluster0.axsfc.mongodb.net/{}?retryWrites = true & w = majority".format (
        username, password, db_name)

    db.connect(db_dui)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    global_init()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
