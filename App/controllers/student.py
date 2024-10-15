from App.models import Student
from App.database import db


@classmethod
def create_student(cls, name, email, password):
    """Create a new student."""
    print(f"Creating student with Name: {name}, Email: {email}")
    student = cls(name=name, email=email, password=password)
    db.session.add(student)
    db.session.commit()
    return student

@classmethod
def view_all_competitions(cls):
    """Return all competitions uploaded by any organizer."""
    return Competition.query.all()

def update_student_info(self, studentId, name=None, email=None):
    if name:
        self.name = name
    if email:
        self.email = email
    db.session.commit()
    return f"Student {self.name}'s information updated!"