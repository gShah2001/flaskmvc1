from App.models import CompetitionOrganizer
from App.database import db

@classmethod
def create_comporg(cls, organizerId, username, email, password):
    """Creates a new Competition Organizer."""
    print(f"Creating student with Name: {username}, Email: {email}")
    new_organizer = CompetitionOrganizer(organizerId=organizerId, username=username, email=email, password=password )
    db.session.add(new_organizer)
    db.session.commit()
    return new_organizer
