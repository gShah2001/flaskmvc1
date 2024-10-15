import csv
from App.database import db

class Results(db.Model):
    resultsId = db.Column(db.Integer, primary_key=True)
    competitionId = db.Column(db.Integer, db.ForeignKey('competition.competitionId'), nullable=False)
    studentId = db.Column(db.Integer, db.ForeignKey('student.studentId'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __init__(self, competitionId, studentId, score):
        self.competitionId = competitionId
        self.studentId = studentId
        self.score = score

    @classmethod
    def import_from_csv(cls, csv_file):
            """Import results from a CSV file."""
            try:
                with open(csv_file, newline='') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        result = cls(
                            competitionId=int(row['competitionId']),
                            studentId=int(row['studentId']),
                            score=float(row['score']),
                        )
                        db.session.add(result)

                    # Commit all added results at once
                    db.session.commit()
                    return f"Results successfully imported from {csv_file}"

            except Exception as e:
                db.session.rollback()  # Rollback in case of any errors
                return f"Error importing results: {e}"

    def delete_from_csv(cls, csv_file):
        """Delete results based on competitionId and studentId from a CSV file."""
        try:
            with open(csv_file, newline='') as file:
                reader = csv.DictReader(file)
                deleted_count = 0
                for row in reader:
                    result = cls.query.filter_by(
                        competitionId=int(row['competitionId']),
                        studentId=int(row['studentId'])
                    ).first()
                    if result:
                        db.session.delete(result)
                        deleted_count += 1

                # Commit all deletions at once
                db.session.commit()
                return f"Successfully deleted {deleted_count} results from {csv_file}"

        except Exception as e:
            db.session.rollback()  # Rollback in case of any errors
            return f"Error deleting results: {e}"