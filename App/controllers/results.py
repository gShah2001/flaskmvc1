from App.models import Results
from App.database import db

def import_results_from_csv(csv_file):
    return Results.import_from_csv(csv_file)