from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class CompetitionOrganizer(db.Model):
    __tablename__ = 'competitionorganizer'
    organizerId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    competitions = db.relationship('Competition', backref='organizer', lazy=True)

    def __init__(self, organizerId, username, password, email):
        self.organizerId = organizerId
        self.username = username
        self.set_password(password)
        self.email = email
 
    def __repr__(self):
        return f"CompetitionOrganizer(id={self.organizerId}, username={self.username}, email={self.email})"

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    @classmethod
    def create_comporg(cls, organizerId, username, email, password):
        """Creates a new Competition Organizer."""
        print(f"Creating competition organizer with Name: {username}, Email: {email}")
        new_organizer = CompetitionOrganizer(organizerId=organizerId, username=username, email=email, password=password )
        db.session.add(new_organizer)
        db.session.commit()
        return new_organizer

