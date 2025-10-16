from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import uuid


# Create your models here.
class Conference(models.Model):
    conference_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(
    validators=[
        MinLengthValidator(
            limit_value=30,
            message="La description doit contenir au minimum 30 caractères"
        )
    ]
)
    location = models.CharField(max_length=255)

    THEME = [
        ("CS&IA", "Computer science & IA"),
        ("CS", "Social science"),
        ("SE", "Science and Engineering"),
    ]
    theme = models.CharField(max_length=255, choices=THEME)

    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError ("la date de debut doit etre anterieur a la date de fin de la conference")
        

def validate_keywords(value):
    keywords_list = [k.strip() for k in value.split(',') if k.strip()]
    if len(keywords_list) > 10:
        raise ValidationError("erreur plus de 10 mots")
 


def generate_submission_id():
    return "SUB" + uuid.uuid4().hex[:8].upper()


class Submission(models.Model):
    submission_id = models.CharField (
    primary_key=True,
    max_length=255,
    unique=True,
    editable=False
    )

    user = models.ForeignKey(
        "UserApp.User",
        on_delete=models.CASCADE,
        related_name="submissions"
    )
    conference = models.ForeignKey(
        Conference,
        on_delete=models.CASCADE,
        related_name="submissions"
    )
    title = models.TextField()
    abstract = models.TextField()
    keywords = models.TextField(validators=[validate_keywords])
    paper = models.FileField(upload_to="papers/",validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
 
def clean(self):

    if self.conference.date <=  self.conference.start_date:
        raise ValidationError("conference a venur :erreur")

    
    same_day_submissions = Submission.objects.filter(
        author=self.author,
        submission_date__date=self.submission_date.date()
    ).exclude(pk=self.pk).count()

    if same_day_submissions >= 3:
        raise ValidationError("plus que 3 soumission par jour:erreur ")


    CHOICES = [
        ("submitted", "submitted"),
        ("under review", "under review"),
        ("accepted", "accepted"),
        ("rejected", "rejected"),
    ]
    status = models.CharField(max_length=255, choices=CHOICES)

    payed = models.BooleanField(default=False)
    submission_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.status}"
