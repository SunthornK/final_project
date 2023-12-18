
# Final Project Repository

This repository contains the following files:

- `person.csv`: CSV file containing person data.
- `login.csv`: CSV file containing login data.
- `project.csv`: CSV file containing project data.
- `advisor_pending_request.csv`: CSV file for pending advisor requests.
- `member_pending_request.csv`: CSV file for pending member requests.
- `evaluations.csv`: CSV file for project evaluations.
- `database.py`: Python file containing the Database, Table, and Csv classes.
- `project_manage.py`: Python file containing the main functionalities for managing the project.
- `proposal.md`: Document detailing the project proposal.
- `TODO.md`: Document listing tasks and things to do.
- `README.md`: This file, providing an overview of the project structure.

## Database Classes

### `Database` Class

The `Database` class provides functionality for managing tables and data.

### `Table` Class

The `Table` class represents a table in the database and includes methods for querying and updating data.

### `Csv` Class

The `Csv` class handles reading data from CSV files.

## Project Management Classes

### `Admin` Class

The `Admin` class represents an administrative user with the ability to view users, modify user roles, and manage tables.

### `Student` Class

The `Student` class represents a student user with actions such as checking pending requests, accepting/denying requests, and creating projects.

### `Lead` Class

The `Lead` class represents a lead user with actions for viewing project status, sending member and advisor requests, and modifying project information.

### `Member` Class

The `Member` class represents a member user with actions for viewing project status, viewing responses to requests, and modifying project information.

### `Faculty` Class

The `Faculty` class represents a faculty user with actions for viewing all projects, checking pending requests, accepting/denying requests, and evaluating projects.

### `Advisor` Class

The `Advisor` class represents an advisor user with actions for viewing all projects, checking pending requests, accepting/denying requests, and evaluating projects.

## How to Compile and Run

1. Make sure you have Python installed on your system.
2. Open a terminal and navigate to the project directory.
3. Run the following command to execute the project:

   ```bash
   python project_manage.py

# Role Actions and Completion Percentage

| Role    | Action                     | Relevant Methods/Classes            | Completion (%) |
|---------|----------------------------|-------------------------------------|----------------|
| Admin   | View All Users             | `Admin.view_all_users`              | 90%            |
| Admin   | Modify User Role           | `Admin.modify_user_role`            | 80%            |
| Admin   | Update Row in Table        | `Admin.update_row_in_table`         | 70%            |
| Admin   | Append Row to Table        | `Admin.append_row_to_table`         | 60%            |
| Admin   | Update All Tables          | `Admin.update_all_tables`           | 95%            |
| Student | Check Pending Requests     | `Student.check_pending_requests`    | 95%            |
| Student | Accept Request             | `Student.accept_request`            | 95%            |
| Student | Deny Request               | `Student.deny_request`              | 95%            |
| Student | Create Project             | `Student.create_project_and_lead`   | 95%            |
| Student | View Project Status        | `Member.view_project_status`        | 95%            |
| Lead    | View Project Status        | `Lead.view_project_status`          | 95%            |
| Lead    | View Responses             | `Lead.view_responses`               | 95%            |
| Lead    | Modify Project Information | `Lead.modify_project_information`   | 95%            |
| Lead    | Send Advisor Request       | `Lead.send_advisor_request`         | 95%            |
| Lead    | Send Member Requests       | `Lead.send_member_requests`         | 95%            |
| Member  | View Project Status        | `Member.view_project_status`        | 95%            |
| Member  | View Responses             | `Member.view_responses`             | 95%            |
| Member  | Modify Project Information | `Member.modify_project_information` | 95%            |
| Faculty | View All Projects          | `Faculty.view_all_projects`         | 90%            |
| Faculty | Check Pending Requests     | `Faculty.check_pending_requests`    | 90%            |
| Faculty | Accept Request             | `Faculty.accept_request`            | 90%            |
| Faculty | Deny Request               | `Faculty.deny_request`              | 90%            |
| Faculty | Evaluate Projects          | `Faculty.evaluate_project`          | 90%            |
| Advisor | View All Projects          | `Advisor.view_all_projects`         | 90%            |
| Advisor | Check Pending Requests     | `Advisor.check_pending_requests`    | 90%            |
| Advisor | Accept Request             | `Advisor.accept_request`            | 90%            |
| Advisor | Deny Request               | `Advisor.deny_request`              | 90%            |
| Advisor | Evaluate Projects          | `Advisor.evaluate_project`          | 90%            |

# Missing Features and Outstanding Bugs

## Missing Features

- Student: Request to leave a project.
- Lead: Remove a member from a project.
- Faculty: Edit evaluation scores after submission.
- Advisor: Edit evaluation scores after submission.
- Admin: Ability to delete users.

## Outstanding Bugs

- admin.update_all_tables() does not work properly.
- admin.modify_user_role() does not work properly.
- admin.update_row_in_table() does not work properly.
- admin.append_row_to_table() does not work properly.
- don't have enough time to test all the methods so completeness percentage may not be accurate.