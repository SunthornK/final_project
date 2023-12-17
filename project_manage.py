import csv
import datetime
from database import Database, Table, Csv


def initializing():
    my_db = Database()
    persons_data = Csv("persons.csv").read_csv()
    login_data = Csv("login.csv").read_csv()
    project_data = Csv("project.csv").read_csv()
    advisor_pending_request = Csv("advisor_pending_request.csv").read_csv()
    member_pending_request = Csv("member_pending_request.csv").read_csv()
    persons_table = Table('persons', persons_data)
    login_table = Table('login', login_data)
    project_table = Table('project', project_data)
    member_pending_request_table = Table('member_pending_request', member_pending_request)
    advisor_pending_request_table = Table('advisor_pending_request', advisor_pending_request)
    my_db.insert(persons_table)
    my_db.insert(login_table)
    my_db.insert(project_table)
    my_db.insert(member_pending_request_table)
    my_db.insert(advisor_pending_request_table)
    return my_db


def login():
    my_db = initializing()
    login_search = my_db.search('login')
    print("Sign in to continue")
    found = False
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        for user_data in login_search.table:
            if username in user_data['username']:
                if password == user_data['password']:
                    user_id = user_data['ID']
                    role = user_data['role']
                    print("Login successful!\n")
                    return user_id, role
                else:
                    found = True
                    print("Incorrect password. Please try again.")
        if not found:
            print("Username not found. Please try again.")


# Define a function called exit
def exit_program(my_db):
    my_db.update_login_csv()
    my_db.update_member_pending_request_csv()
    my_db.update_project_csv()
    print("Data saved. Exiting the program.")


class Admin:
    def __init__(self, user_info):
        self.user_info = user_info


class Student:
    def __init__(self, user_id, my_db):
        self.user_id = user_id
        self.my_db = my_db

    def check_pending_requests(self):
        pending_requests = self.my_db.search('member_pending_request').filter(
            lambda request: request['to_be_member'] == self.user_id
        )
        return pending_requests

    def accept_request(self, request_id):
        member_pending_request_table = self.my_db.search('member_pending_request')
        project_table = self.my_db.search('project')

        request = member_pending_request_table.filter(
            lambda r: r['request_id'] == request_id and r['to_be_member'] == self.user_id
        )
        if request:
            # Update the Member_pending_request table
            request[0]['Response'] = "Accepted"
            request[0]['Response_date'] = datetime.date.today().strftime("%m/%d/%y")

            # Add the student to the project (update Project table)
            project_id = request[0]['ProjectID']
            project = project_table.filter(
                lambda p: p['project_id'] == project_id
            )
            if project:
                if 'Member1' not in project[0]:
                    project[0]['Member1'] = self.user_id
                else:
                    project[0]['Member2'] = self.user_id
                print(f"Request for member {request_id} accepted.")
            else:
                print(f"Project with ID {project_id} not found.")
        else:
            print(f"Request for member {request_id} not found.")

    def deny_request(self, request_id):
        member_pending_request_table = self.my_db.search('member_pending_request')

        request = member_pending_request_table.filter(
            lambda r: r['request_id'] == request_id and r['to_be_member'] == self.user_id
        )
        if request:
            request[0]['Response'] = "Denied"
            request[0]['Response_date'] = datetime.date.today().strftime("%m/%d/%y")
            print(f"Request for member {request_id} denied.")
        else:
            print(f"Request for member {request_id} not found.")

    def create_project_and_become_lead(self, project_name):
        member_pending_request_table = self.my_db.search('member_pending_request')
        login_table = self.my_db.search('login')
        project_table = self.my_db.search('project')

        # Deny all existing member requests
        self.deny_all_member_requests()

        # Create a new project
        new_project = {
            "project_id": len(project_table.table) + 1,
            "project_name": project_name,
            "lead_id": self.user_id,
            "members": []
        }
        project_table.insert(new_project)

        # Update the Login table to mark the user as a project lead
        login_table.update('ID', self.user_id, {'role': 'lead'})

        print(f"Project '{project_name}' created, and {self.user_id} is now the lead.")

    def deny_all_member_requests(self):
        member_pending_request_table = self.my_db.search('member_pending_request')

        if user_role == "student":
            pending_requests = member_pending_request_table.table
            for request in pending_requests:
                self.deny_request(request['request_id'])

    def send_member_requests(self, project_id, member_ids):
        member_pending_request_table = self.my_db.search('member_pending_request')
        login_table = self.my_db.search('login')
        project_table = self.my_db.search('project')

        # Check if the user is a lead of the specified project
        project = project_table.filter(lambda p: p['project_id'] == project_id)
        if project and project[0]['lead_id'] == self.user_id:
            for member_id in member_ids:
                # Check if the member is a student (not a member or lead)
                member = login_table.filter(lambda m: m['ID'] == member_id and m['role'] == 'student')
                if member:
                    # Add request to Member_pending_request table
                    new_request = {
                        "request_id": len(member_pending_request_table.table) + 1,
                        "ProjectID": project_id,
                        "to_be_member": member_id,
                        "Response": "Pending",
                        "Response_date": "Pending"
                    }
                    member_pending_request_table.insert(new_request)
                    print(f"Request sent to student {member_id}.")
                else:
                    print(f"User {member_id} is not a student or is already a member/lead.")
        else:
            print(f"You are not the lead of the project with ID {project_id}.")

    def display_menu(self, has_pending_requests):
        print("-" * 50)
        print("Menu:")
        print("1. Check Pending Requests")
        if has_pending_requests:
            print(" 2. Accept Request")
            print(" 3. Deny Request")
        print("4. Create Project and Become Lead")
        print("5. Send Member Requests")
        print("6. Quit")

    def run_menu(self):
        while True:
            pending_requests = self.check_pending_requests()
            has_pending_requests = len(pending_requests.table) > 0

            self.display_menu(has_pending_requests)
            choice = input("Enter your choice (1-6): ")

            if choice == '1':
                print("Pending Requests:")
                if len(pending_requests.table) == 0:
                    print("No pending requests.")
                else:
                    print(pending_requests)
            elif has_pending_requests and choice == '2':
                request_id = input("Enter the request ID to accept: ")
                self.accept_request(request_id)
            elif has_pending_requests and choice == '3':
                request_id = input("Enter the request ID to deny: ")
                self.deny_request(request_id)
            elif choice == '4':
                project_name = input("Enter the project name to create: ")
                self.create_project_and_become_lead(project_name)
            elif choice == '5':
                project_id = input("Enter the project ID to send requests: ")
                member_ids = input("Enter member IDs (comma-separated): ").split(',')
                member_ids = [int(member_id) for member_id in member_ids]
                self.send_member_requests(project_id, member_ids)
            elif choice == '6':
                exit_program(self.my_db)
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")


# class Lead_Student:
# class Member_Student:
# class Faculty:
# class Advisor:
# make calls to the initializing and login functions defined above

my_db = initializing()
print()
val = login()
user_id, user_role = val

# based on the return value for login, activate the code that performs activities according to the role defined for that person_id
if val[1] == 'admin':
    pass
elif val[1] == 'student':
    student = Student(user_id, my_db)
    student.run_menu()

# elif val[1] == 'member':
#     see and do member-related activities
# elif val[1] == 'lead':
#     see and do lead-related activities
# elif val[1] == 'faculty':
#     see and do faculty-related activities
# elif val[1] == 'advisor':
#     see and do advisor-related activities

# once everything is done, make a call to the exit function
exit_program(my_db)
