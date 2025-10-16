from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Create your models here.
import uuid
def generate_user_id():
    return "USER"+ uuid.uuid4().hex[:4].upper()
def verify_email(email):
    domaine=["esprit.tn","sesame.com","tek.tn","central.com"]
    if email.split("@")[1] not in domaine:
        raise ValidationError("l'email est invalide et doit appartenir a un domain universitaire prive ")
    

name_validator = RegexValidator(
    regex=r'^[A-Za-z\s-]+$',
    message="ce champs ne doit contenir que des lettres, des espaces et des tirets"
)





class User(AbstractUser):
    user_id = models.CharField(
        max_length=8,
        primary_key=True,
        unique=True,
        editable=False
    )
    first_name = models.CharField(max_length=100,validators=[name_validator])
    last_name = models.CharField(max_length=100 ,validators=[name_validator])
    email = models.EmailField(unique=True, validators=[verify_email])
    affiliation = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)

    ROLE = [
        ("participant", "Participant"),
        ("committee", "Organizing committee member"),
    ]
    role = models.CharField(
        max_length=255,
        choices=ROLE,
        default="participant"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self,*args,**kwargs):
        if not self .user_id:
            new_id=generate_user_id()
            while User.objects.filter(user_id=new_id).exists():
                new_id=generate_user_id()
            self.user_id=new_id
        super().save(*args,**kwargs)


    #submissions=models.ManyToManyField("ConferenceApp.Conference", through="Submissions" )
    #organizingCommiteeList=models.ManyToManyField("ConferenceApp.Conference",through="Organizing")



class OrganizingCommittee(models.Model):
    user = models.ForeignKey(
        "UserApp.User",
        on_delete=models.CASCADE,
        related_name="committees"
    )
    conference = models.ForeignKey(
        "ConferenceApp.Conference",
        on_delete=models.CASCADE,
        related_name="committees"
    )

    ROLES = (
        ("chair", "Chair"),
        ("member", "Member"),
        ("co-chair", "Co-chair"),
    )
    committee_role = models.CharField(max_length=255, choices=ROLES)

    date_join = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.committee_role}"

