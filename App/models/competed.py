from App.database import db


class Competed(db.Model):
    __tablename__= 'competed'
    id = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer, db.ForeignKey('student.studentId'), nullable=False)
    competitionId = db.Column(db.Integer, db.ForeignKey('competition.competitionId'), nullable=False)

    def __init__(self, id, studentId, competitionId):
        self.competedId = id
        self.studentId = studentId
        self.competitionId=competitionId 

    #def __repr__(self):
    #    return {
    #        'studentId':self.studentId,
    #        'competitionId':self.competitionId
    #    } 

    def __repr__(self):
        return f"Competed(id={self.id}, studentId={self.studentId}, competitionId={self.competitionId})"

    def get_student_competitions(student_id):
        competitions = Competition.query.join(Competed).filter_by(studentId=student_id).all()
        return [competition.title for competition in competitions]

    def get_competition_students(competition_id):
        students = Student.query.join(Competed).filter_by(competitionId=competition_id).all()
        return [student.name for student in students]