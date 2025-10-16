from django.db import models
from ConferenceApp.models import Conference
from django.core.validators import RegexValidator


# Create your models here.
class Session(models.Model):
    session_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    topic=models.CharField(max_length=255)
    session_day=models.DateField
    start_time=models.TimeField
    end_time=models.TimeField
    room=models.CharField(max_length=255)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)

    conference = models.ForeignKey("ConferenceApp.Conference", on_delete=models.CASCADE , related_name="sessions")


# travail personnel
def clean(self):
       
        if self.conference:
            validate_session_day(self.session_day, self.conference)
        validate_session_times(self.start_time, self.end_time)  


def validate_session_day(session_day, conference):
    """Vérifie que la date de session est comprise entre les dates de la conférence."""
    if conference.start_date and conference.end_date:
        if not (conference.start_date <= session_day <= conference.end_date):
            raise ValidationError(
                f"La date de la session ({session_day}) doit être comprise entre "
                f"{conference.start_date} et {conference.end_date}."
            )


def validate_session_times(start_time, end_time):
    """Vérifie que l'heure de fin est supérieure à l'heure de début."""
    if start_time and end_time:
        if end_time <= start_time:
            raise ValidationError(
                "L'heure de fin doit être strictement supérieure à l'heure de début."
            )


room_validator = RegexValidator(
    regex=r'^[A-Za-z0-9\s]+$',
    message="Le nom de la salle ne doit contenir que des lettres et des chiffres (pas de caractères spéciaux)."
)
