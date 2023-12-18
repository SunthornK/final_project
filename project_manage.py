
import datetime
import random

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


def exit_program(my_db):
    my_db.update_login_csv()
    my_db.update_member_pending_request_csv()
    my_db.update_project_csv()
    print("Data saved. Exiting the program.")


class Student:
    def __init__(self, user_id, my_db):
        self.user_id = user_id
        self.member_requests = my_db.search('member_pending_request')
        self.login_table = my_db.search('login')
        self.project_table = my_db.search('project')

    def check_pending_requests(self):
        pending_requests = self.member_requests.filter(
            lambda x: x['to_be_member'] == self.user_id).filter(lambda x: x["Response"] == "Pending")
        return pending_requests.table

    def accept_request(self, project_id):
        invited = self.project_table.filter(lambda x: x["Project_ID"] == project_id)
        for i in invited:
            if i["Member1"] == "None":
                self.login_table.update('ID', self.user_id, 'role', 'member')
                self.project_table.update('Project_ID', project_id, 'Member1', self.user_id)
                self.member_requests.update('to_be_member', project_id, 'Response', 'Accepted')
                self.member_requests.update('to_be_member', project_id, 'Response_date',
                                            datetime.date.today().strftime("%m"
                                                                           "/%d/%y"))

            elif i["Member2"] == "None":
                self.login_table.update('ID', self.user_id, 'role', 'member')
                self.project_table.update('Project_ID', project_id, 'Member2', self.user_id)
                self.member_requests.update('to_be_member', project_id, 'Response', 'Accepted')
                self.member_requests.update('to_be_member', project_id, 'Response_date',
                                            datetime.date.today().strftime("%m"
                                                                           "/%d/%y"))
            else:
                print("Project is full")

    def deny_request(self, request_id):
        request = self.member_requests.filter(
            lambda r: r['request_id'] == request_id and r['to_be_member'] == self.user_id
        )
        if request:
            self.member_requests.update('to_be_member', request_id, 'Response', 'Denied')
            self.member_requests.update('to_be_member', request_id, 'Response_date',
                                        datetime.date.today().strftime("%m"
                                                                       "/%d/%y"))
        else:
            print(f"Request for member {request_id} not found.")

    def generate_project_id(self):
        return ''.join([f'{random.randint(0, 9)}' for _ in range(6)])

    def create_project_and_become_lead(self, project_name):
        self.deny_all_member_requests()
        new_project = {
            "ProjectID": self.generate_project_id(),
            "Title": project_name,
            "Lead": self.user_id,
            "Member1": "None",
            "Member2": "None",
            "Advisor": "None",
            "Status": "pending member"
        }
        self.project_table.insert(new_project)
        self.project_table.update('ID', self.user_id, 'role', 'lead')
        print(f"Project '{project_name}' created, and {self.user_id} is now the lead.")

    def deny_all_member_requests(self):
        for request in self.member_requests.table:
            self.deny_request(request['to_be_member'])

    def student_menu(self, has_pending_requests):
        print("-" * 50)
        print("Student Menu:")
        print("1. Check Pending Requests")
        if has_pending_requests:
            print(" 2. Accept Request")
            print(" 3. Deny Request")
        print("4. Create Project and Become Lead")
        print("5. Quit")

    def run_menu(self):
        while True:
            pending_requests = self.check_pending_requests()
            has_pending_requests = len(pending_requests.table) > 0

            self.student_menu(has_pending_requests)
            choice = input("Enter your choice (1-6): ")

            if choice == '1':
                print("Pending Requests:")
                if len(pending_requests.table) == 0:
                    print("No pending requests.")
                else:
                    print(pending_requests)
            elif has_pending_requests and choice == '2':
                request_id = input("Enter the request project ID to accept: ")
                self.accept_request(request_id)
            elif has_pending_requests and choice == '3':
                request_id = input("Enter the request project ID to deny: ")
                self.deny_request(request_id)
            elif choice == '4':
                project_name = input("Enter the project name to create: ")
                self.create_project_and_become_lead(project_name)
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")


class Lead:
    def __init__(self, user_id, my_db):
        self.user_id = user_id
        self.member_requests = my_db.search('member_pending_request')
        self.login_table = my_db.search('login')
        self.project_table = my_db.search('project')
        self.adviser_request = my_db.search('advisor_pending_request')

    def view_project_status(self):
        my_project = self.project_table.filter(
            lambda request: request['Lead'] == self.user_id
        )
        return my_project

    def send_member_requests(self, project_id, member_ids):
        # Check if the user is a lead of the specified project
        project = self.project_table.filter(lambda p: p['ProjectID'] == project_id)
        check_if_lead_of_project = self.project_table.filter(lambda request: request['Lead'] == self.user_id)
        if project and check_if_lead_of_project:
            # Check if the member is a student (not a member or lead)
            member = self.login_table.filter(lambda m: m['ID'] == member_ids and m['role'] == 'student')
            if member:
                # Add request to Member_pending_request table
                new_request = {
                    "ProjectID": project_id,
                    "to_be_member": member_ids,
                    "Response": "Pending",
                    "Response_date": "Pending"
                }
                self.member_requests.insert(new_request)
                print(f"Request sent to student {member_ids}.")
            else:
                print(f"User {member_ids} is not a student or is already a member/lead.")
        else:
            print(f"You are not the lead of the project with ID {project_id}.")

    def view_responses(self, project_id):
        response = self.member_requests.filter(
            lambda request: request['ProjectID'] == project_id).filter(lambda x: x["Response"] != "Pending")
        return response

    def send_advisor_request(self, project_id, advisor_id):
        # Check if all potential members have responded
        pending_members = self.member_requests.filter(
            lambda req: req['ProjectID'] == project_id and req['Response'] == 'Pending'
        )
        if pending_members:
            print("Cannot send advisor request until all potential members have responded.")
            return

        # Check if the advisor is valid (exists and is not already associated with the project)
        advisor = self.login_table.filter(
            lambda adv: adv['ID'] == advisor_id and adv['role'] == 'advisor'
        )
        project = self.project_table.filter(
            lambda p: p['project_id'] == project_id and p['lead_id'] == self.user_id
        )
        if advisor and project:
            # Check if the advisor is not already associated with the project
            associated_advisor = project[0].get('AdvisorID')
            if associated_advisor != advisor_id:
                print("An advisor is already associated with this project.")
                return

            # Add request to Advisor_pending_request table
            new_request = {
                "ProjectID": project_id,
                "to_be_advisor": advisor_id,
                "Response": "Pending",
                "Response_date": "Pending",
            }
            self.adviser_request.insert(new_request)
            print(f"Advisor request sent to advisor {advisor_id}.")
        else:
            print("Invalid advisor or project.")

    def lead_menu(self):
        print("-" * 50)
        print("Lead Menu:")
        print("1. View Project Status")
        print("2. View Responses to Requests")
        print("3. Modify Project Information")
        print("4. Send Advisor Request")
        print("5. Send Member Requests")
        print("6. Quit")

    def modify_project_information(self, project_id, new_title):
        self.project_table.update('ProjectID', project_id, 'Title', f'{new_title}')

    def run_menu(self):
        while True:
            self.lead_menu()
            choice = input("Enter your choice (1-6): ")
            if choice == '1':
                print(self.view_project_status())
            elif choice == '2':
                project_id = input("Enter the project ID to view responses: ")
                print(self.view_responses(project_id))
            elif choice == '3':
                project_id = input("Enter the project ID to modify information: ")
                new_title = input("Enter the new project title: ")
                self.modify_project_information(project_id, new_title)
            elif choice == '4':
                project_id = input("Enter the project ID to send advisor request: ")
                advisor_id = input("Enter the advisor ID: ")
                self.send_advisor_request(project_id, advisor_id)
            elif choice == '5':
                project_id = input("Enter the project ID to send member request: ")
                invited_id = input("Enter the ID of who you want to invite: ")
                self.send_member_requests(project_id, invited_id)
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")


class Member:
    def __init__(self, user_id, my_db):
        self.user_id = user_id
        self.member_requests = my_db.search('member_pending_request')
        self.project_table = my_db.search('project')

    def view_responses(self, project_id):
        response = self.member_requests.filter(
            lambda request: request['ProjectID'] == project_id).filter(lambda x: x["Response"] != "Pending")
        return response

    def view_project_status(self):
        my_project = self.project_table.filter(
            lambda x: x['Lead'] == self.user_id
        )
        return my_project

    def modify_project_information(self, project_id, new_title):
        self.project_table.update('ProjectID', project_id, 'Title', f'{new_title}')

    def member_menu(self):
        print("-" * 50)
        print("Member Menu:")
        print("1. View Project Status")
        print("2. View Responses to Requests")
        print("3. Modify Project Information")
        print("4. Quit")

    def run_menu(self):
        while True:
            self.member_menu()
            choice = input("Enter your choice (1-4): ")
            if choice == '1':
                print(self.view_project_status())
            elif choice == '2':
                project_id = input("Enter the project ID to view responses: ")
                print(self.view_responses(project_id))
            elif choice == '3':
                project_id = input("Enter the project ID to modify information: ")
                new_title = input("Enter the new project title: ")
                self.modify_project_information(project_id, new_title)
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")

class Faculty:
    def __init__(self, user_id, my_db):
        self.user_id = user_id
        self.advisor_requests = my_db.search('advisor_pending_request')
        self.login_table = my_db.search('login')
        self.project_table = my_db.search('project')

    def view_all_projects(self):
        return self.project_table

    def check_pending_requests(self):
        pending_requests = self.advisor_requests.filter(
            lambda x: x['to_be_member'] == self.user_id).filter(lambda x: x["Response"] == "Pending")
        return pending_requests.table

    def accept_request(self, project_id):
        invited = self.project_table.filter(lambda x: x["Project_ID"] == project_id)
        for i in invited:
            if i["Advisor"] == "None":
                self.login_table.update('ID', self.user_id, 'role', 'advisor')
                self.project_table.update('Project_ID', project_id, 'Advisor', self.user_id)
                self.advisor_requests.update('ProjectID', project_id, 'Response', 'Accepted')
                self.advisor_requests.update('ProjectID', project_id, 'Response_date',
                                             datetime.date.today().strftime("%m/%d/%y"))
            else:
                print("This Project already has an advisor.")

    def deny_request(self, request_id):
        request = self.advisor_requests.filter(
            lambda r: r['request_id'] == request_id and r['to_be_advisor'] == self.user_id
        )
        if request:
            self.advisor_requests.update('to_be_advisor', request_id, 'Response', 'Denied')
            self.advisor_requests.update('to_be_advisor', request_id, 'Response_date',
                                        datetime.date.today().strftime("%m"
                                                                       "/%d/%y"))
        else:
            print(f"Request for be an advisor {request_id} not found.")

    def evaluate_projects(self):
        pass
    def faculty_menu(self, has_pending_requests):
        print("-" * 50)
        print("Faculty Menu:")
        print("1. Check Pending Requests")
        if has_pending_requests:
            print(" 2. Accept Request")
            print(" 3. Deny Request")
        print("4. Evaluate projects")
        print("5. Quit")

    def run_menu(self):
        while True:
            pending_requests = self.check_pending_requests()
            has_pending_requests = len(pending_requests.table) > 0

            self.faculty_menu(has_pending_requests)
            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                print("Pending Requests:")
                if len(pending_requests.table) == 0:
                    print("No pending requests.")
                else:
                    print(pending_requests)
            elif has_pending_requests and choice == '2':
                request_id = input("Enter the request project ID to accept: ")
                self.accept_request(request_id)
            elif has_pending_requests and choice == '3':
                request_id = input("Enter the request project ID to deny: ")
                self.deny_request(request_id)
            elif choice == '4':
                self.evaluate_projects()
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")




# class Advisor:
class Admin:
    def __init__(self, user_id, my_db):
        self.user_id = user_id
        self.member_requests = my_db.search('member_pending_request')
        self.login_table = my_db.search('login')
        self.project_table = my_db.search('project')
        self.advisor_requests = my_db.search('advisor_pending_request')


db = initializing()
print()
val = login()

# based on the return value for login, activate the code that performs activities according to the role defined for that person_id
if val[1] == 'admin':
    pass
elif val[1] == 'student':
    student = Student(val[0], db)
    student.run_menu()

# elif val[1] == 'member':
#     see and do member-related activities
elif val[1] == 'lead':
    lead = Lead(val[0], db)
    lead.run_menu()
# elif val[1] == 'faculty':
#     see and do faculty-related activities
# elif val[1] == 'advisor':
#     see and do advisor-related activities

# once everything is done, make a call to the exit function
exit_program(db)
