import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import (User, Student, Results, Competition, CompetitionOrganizer,Competed)
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)

'''
Student Commands
'''

student_cli = AppGroup('student', help='Student object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@app.cli.command("create-student", help="Creates a student")
@click.argument("name", default="rob")
@click.argument("email", default= "rob@mail.com")
@click.argument("password", default="robpass")
def create_student_command(name, email, password):
    existing_username = Student.query.filter_by(name=name).first()
    if existing_username:
        print(f"Error: Username '{username}' is already taken.")
        return

    existing_email = Student.query.filter_by(email=email).first()
    if existing_email:
        print(f"Error: Email '{email}' is already registered.")
        return

    student = Student.create_student(name, email, password)
    print(f'Student {student.name} has been created!')

@app.cli.command("login", help="Logs in students")
@click.argument("name", default="rob")
@click.argument("password", default="robpass")
def login_student_command(name, password):
    res = login_student(name, password)
    if res:
        print(f'{name} logged in!')
    else:
        print('login unsuccessful!')


@app.cli.command("view-competitions", help="List all competitions available")
@with_appcontext
def view_competitions_command():
    competitions = Student.view_all_competitions()
    #click.echo([competition.title for competition in competitions])
    if competitions:
        click.echo("Competitions:")
        for competition in competitions:
            click.echo(f"ID: {competition.competitionId}, Title: {competition.title}, Status: {competition.status}")
    else:
        click.echo("No competitions found.")


@app.cli.command("update-info", help="Update a student's info")
@click.argument("student_id")
@click.option("--name", default=None, help="New name for the student")
@click.option("--email", default=None, help="New email for the student")
@with_appcontext
def update_student_command(student_id, name, email):
    student = Student.query.get(student_id)
    if student:
        message = student.update_student_info(name, email)
        print(message)
    else:
        print(f"Student with id {student_id} not found.")


@app.cli.command("delete", help="Deletes a student by ID")
@click.argument("student_id", type=int)
@with_appcontext
def delete_student_command(student_id):
    """Deletes a student by ID."""
    student = Student.query.get(student_id)
    if not student:
        print("Student not found.")
        return
    db.session.delete(student)
    db.session.commit()
    print(f'Student with ID {student_id} has been deleted')


@app.cli.command("get-all", help="Get all students")
@with_appcontext
def get_all_students_command():
    """Get all students."""
    #students = Student.get_all_students()
    students=Student.query.all()
    if students:
        print("List of Students:")
        for student in students:
            print(f"ID: {student.studentId}, Name: {student.name}, Email: {student.email}")
    else:
        print("No students found.")
    
    #print(students)


@app.cli.command("get-by-id", help="Get a student by ID")
@click.argument("student_id", type=int)
@with_appcontext
def get_student_by_id_command(student_id):
    """Get a student by ID."""
    student = Student.query.get(student_id)
    if student:
        print(f"ID: {student.studentId}, Name: {student.name}, Email: {student.email}")
    else:
        print("Student not found.")

app.cli.add_command(student_cli)

'''
Competition Organizer Commands
'''

competitionOrganizer_cli = AppGroup('competitionOrganizer', help='Competition Organizer object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@app.cli.command("create-comporg", help="Creates a Competition Organizer user")
@click.argument("organizer_id", type=int)
@click.argument("username", default="bob")
@click.argument("email", default= "bob@mail.com")
@click.argument("password", default="bobpass")
def create_competitionOrganizer_command(organizer_id, username, email, password):
    existing_organizer = CompetitionOrganizer.query.filter_by(organizerId=organizer_id).first()
    if existing_organizer:
        print(f"Error: Organizer ID {organizer_id} is already in use.")
        return

    existing_username = CompetitionOrganizer.query.filter_by(username=username).first()
    if existing_username:
        print(f"Error: Username '{username}' is already taken.")
        return

    existing_email = CompetitionOrganizer.query.filter_by(email=email).first()
    if existing_email:
        print(f"Error: Email '{email}' is already registered.")
        return

    compOrganizer=CompetitionOrganizer.create_comporg(organizer_id, username, email, password)
    print(f'{username} has been created!')

@app.cli.command("list-all-org", help="Lists the Competition Organizers in the database")
@with_appcontext
def list_competitionOrganizer_command():
    """Get all Competition Organizers."""
    compOrgs=CompetitionOrganizer.query.all()
    if compOrgs:
        print("List of Competition Organizers")
        for compOrg in compOrgs:
            print(f"ID: {compOrg.organizerId}, Name: {compOrg.name}, Email: {compOrg.email}")
    else:
        print("No Competition Organizers found.")

@app.cli.command("view-org", help="View details of a specific Competition Organizer")
@click.argument("organizer_id", type=int)
@with_appcontext
def view_competitionOrganizer_command(organizer_id):
    """Get a competition organizer by ID."""
    organizer = CompetitionOrganizer.query.get(organizer_id)  # Implement this function
    if organizer:
        print(f"Organizer ID: {organizer.organizerId}, Username: {organizer.name}, Email: {organizer.email}")
    else:
        print("Organizer not found.")

@app.cli.command("delete-org", help="Deletes a Competition Organizer by ID")
@click.argument("organizer_id", type=int)
@with_appcontext
def delete_competitionOrganizer_command(organizer_id):
    """Deletes a Competition Organizer by ID."""
    compOrg = CompetitionOrganizer.query.get(organizer_id)
    if not compOrg:
        print("Competition Organizer not found.")
        return
    db.session.delete(compOrg)
    db.session.commit()
    print(f'Competition Organizer with ID {organizer_id} has been deleted')

app.cli.add_command(competitionOrganizer_cli)

'''
Competition Commands
'''

competition_cli = AppGroup('competition', help='Competition object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@competition_cli.command("create", help="Creates a competition")
@click.argument("title", default="CodeStitch")
@click.argument("organizer", default="Teamscode")
@click.argument("status", default="Completed")
@click.argument("startDate", default="01/01/2000")
@click.argument("endDate", default="01/02/2000")
def create_competition_command(title, status, startDate, endDate):
    create_competition(title, status, startDate, endDate)
    print(f'{title} created!')

@competition_cli.command("list", help="Lists competitions in the database")
def list_competitions_command():
    print(get_all_competitiions())


app.cli.add_command(competition_cli)



'''
Results Commands
'''

results_cli = AppGroup('results', help='Results object commands') 

@app.cli.command("import-results", help="Imports results from a CSV file")
@click.argument('csv_file')  # This expects a single argument for the CSV file
@with_appcontext
def import_results(csv_file):
    """Load results from a CSV file."""
    message = Results.import_from_csv(csv_file)
    print(message)

@app.cli.command("delete-results", help="Deletes results based on a CSV file")
@click.argument('csv_file')
@with_appcontext
def delete_results(csv_file):
    """Delete results based on a CSV file."""
    message = Results.delete_from_csv(csv_file)
    print(message)

app.cli.add_command(results_cli)

'''
Competed Commands
'''

competed_cli = AppGroup('competed', help='Competed object commands') 

@competed_cli.command("list-competitions", help="List all competitions for a student")
@click.argument("student_id")
@with_appcontext
def list_competitions_for_student(student_id):
    competitions = get_student_competitions(student_id)
    if competitions:
        print(f"Student {student_id} is registered for: {', '.join(competitions)}")
    else:
        print(f"Student {student_id} is not registered for any competitions.")

@competed_cli.command("list-students", help="List all students registered for a competition")
@click.argument("competition_id")
@with_appcontext
def list_students_for_competition(competition_id):
    students = get_competition_students(competition_id)
    if students:
        print(f"Students registered for competition {competition_id}: {', '.join(students)}")
    else:
        print(f"No students are registered for competition {competition_id}.")

        
app.cli.add_command(competed_cli)