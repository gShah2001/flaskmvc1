from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from App.models.competition import Competition

class Student(db.Model):
    studentId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True,nullable=False)
    password = db.Column(db.String(128), nullable=False)
    competition = db.relationship('Competition', backref='student_ref', lazy=True)

    def __init__(self, name, email,password):
        self.name = name
        self.email=email
        self.set_password(password)

    def __repr__(self):
        return f"Student(id={self.studentId}, name={self.name}, email={self.email})"
            
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

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