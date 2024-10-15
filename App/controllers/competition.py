from App.models import Competition
from App.database import db

class Competition(db.Model):
    competitionId = db.Column(db.Integer, primary_key=True)
    organizerId = db.Column(db.Integer, db.ForeignKey('competitionorganizer.organizerId'), nullable=False)
    studentID = db.Column(db.Integer, db.ForeignKey('student.studentId'), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(80), nullable=False)
    startDate = db.Column(db.DateTime, nullable=False)
    endDate = db.Column(db.DateTime, nullable=False)
    student = db.relationship('Student', backref='competition_ref', viewonly=True)
    results = db.relationship('Results', backref='competition', lazy=True)

    def __init__(self, competitionId, organizerId, title, status, details, start_date, end_date):
        self.competitionId = competitionId
        self.organizerId = organizerId
        self.title = title
        self.status = status
        self.startDate = startDate
        self.endDate = endDate


    def __repr__(self):
        return f"Competition(id={self.competitionId}, title={self.title}, startDate={self.startDate}, endDate={self.endDate})"

    @classmethod
    def create_competition(cls, competitionId, organizerId, title, status, startDate, endDate):
        """Create a new competition."""
        print(f"Creating Competition with Title: {title}")
        competition = cls(competitionId=competitionId, organizerID=organizerId, title=title, status=status, startDate=startDate, endDate=endDate)
        db.session.add(competition)
        db.session.commit()
        return competition