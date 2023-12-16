from database import Database, Table, Csv


def initializing():
    persons_data = Csv("persons.csv").read_csv()
    login_data = Csv("login.csv").read_csv()
    persons_table = Table('persons', persons_data)
    login_table = Table('login', login_data)
    my_db = Database()
    my_db.insert(persons_table)
    my_db.insert(login_table)
    return my_db


def login():
    my_db = initializing()
    login_search = my_db.search('login')
    print("Sign in to continue")
    found = False
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        for i in login_search.table:
            if username in i['username']:
                if password == i['password']:
                    user_id = i['ID']
                    role = i['role']
                    print("Login successful!")
                    return user_id, role
                else:
                    found = True
                    print("Incorrect password. Please try again.")
        if found is False:
            print("Username not found. Please try again.")


# define a function called exit
def exit():
    pass


class Admin:
    def __init__(self):
        pass


# class Student:
# class Lead_Student:
# make calls to the initializing and login functions defined above

initializing()
print()
val = login()

# based on the return value for login, activate the code that performs activities according to the role defined for that person_id

# if val[1] = 'admin':
#     see and do admin related activities
# elif val[1] = 'student':
#     see and do student related activities
# elif val[1] = 'member':
#     see and do member related activities
# elif val[1] = 'lead':
#     see and do lead related activities
# elif val[1] = 'faculty':
#     see and do faculty related activities
# elif val[1] = 'advisor':
#     see and do advisor related activities

# once everything is done, make a call to the exit function
exit()
