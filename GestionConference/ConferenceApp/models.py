from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import FileExtensionValidator
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid
import random
import string


conference_validator = RegexValidator(r'^[a-zA-Z\s]+$', 'Only alphabetic characters, spaces, are allowed.')



class Conference(models.Model):
    conference_id=models.AutoField(primary_key=True,editable=False)
    name=models.CharField(max_length=255,validators=[conference_validator]) #to validate conference name
    description=models.TextField(validators=[MinLengthValidator(limit_value=30 , message='the description must have at least 30 characters')]) #minimum 50 characters
    location=models.CharField(max_length=255)
    start_date=models.DateField()
    end_date=models.DateField()
    THEME =[
        ("CS&AI","Computer Science & Artificial Intelligence"),
        ("SC&E","Science & Engineering"),
        ("SSC&ED","Social Science & Education"),
        ("Interdisciplinary","Interdisciplinary Themes"),
        
    ]
    theme=models.CharField(max_length=255,choices=THEME)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def clean(self):
        if self.start_date > self.end_date :
            raise ValidationError('start date must be before end date')
        
    
    def __str__(self):
        return self.name
        
 
    
paper_validator = FileExtensionValidator(allowed_extensions=['pdf'],message='Only PDF files are allowed.')

def generate_submission_id():
    """Génère un ID au format SUB_ABCDEFGH"""
    random_chars = ''.join(random.choices(string.ascii_uppercase, k=8))
    return f"SUB_{random_chars}"



class Submission(models.Model):
    submission_id=models.CharField(max_length=50,primary_key=True,editable=False,unique=True)
    title=models.CharField(max_length=255)
    keywords=models.TextField()
    abstract=models.TextField()
    paper=models.FileField(upload_to='papers/',validators=[paper_validator]) #file will be uploaded to media/papers
    user_id=models.ForeignKey('UserApp.User',on_delete=models.CASCADE,related_name='submissions')
    # OR user_id = models.ForeignKey(User)
    conference_id = models.ForeignKey('ConferenceApp.Conference',on_delete=models.CASCADE,related_name='submissions')
    payed = models.BooleanField(default=False)
    submission_date=models.DateTimeField(auto_now_add=True)
    STATUS=[
        ("Submitted","Submitted"),
        ("Under Review","Under Review"),
        ("Accepted","Accepted"),
        ("Rejected","Rejected"),
    ]
    status=models.CharField(max_length=50,choices=STATUS)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
   
    MAX_KEYWORDS = 10
    MAX_SUBMISSIONS_PER_DAY = 3
    
    def validate_keywords(self):
        keyword_list = [kw.strip() for kw in self.keywords.split(',') if kw.strip()]
        if len(keyword_list) > self.MAX_KEYWORDS:
            raise ValidationError({
                'keywords':f'You can specify up to {self.MAX_KEYWORDS} keywords.'})
  
    def validate_conference_dates(self):
        """Validation: submissions only allowed for upcoming conferences"""
        if self.conference_id:
            today = timezone.now().date()
            
            # Check if conference has already started
            if self.conference_id.start_date < today:
                raise ValidationError({
                    'conference_id': 'Submissions are only allowed for conferences that have not started yet.'
                })
            
            # Check if conference has already ended
            if self.conference_id.end_date < today:
                raise ValidationError({
                    'conference_id': 'Submissions are only allowed for upcoming conferences.'
                })

    def validate_submission_limit(self):
        """Validation: limit of 3 submissions per day per user"""
        if self.user_id and self.conference_id:
            today = timezone.now().date()
            today_submissions_count = Submission.objects.filter(
                user_id=self.user_id,
                submission_date__date=today
            ).exclude(pk=self.pk).count()
            
            if today_submissions_count >= self.MAX_SUBMISSIONS_PER_DAY:
                raise ValidationError({
                    'user_id': f'Maximum {self.MAX_SUBMISSIONS_PER_DAY} submissions per day allowed. You have {today_submissions_count} today.'
                })
        
    def clean(self):
        self.validate_keywords()
        self.validate_conference_dates()
        self.validate_submission_limit()
        
    def __str__(self):
        return self.title
   
    
    
    def save(self, *args, **kwargs):
           
            if not self.submission_id:
                max_attempts = 100  
                attempts = 0
                
                new_id = generate_submission_id()
                while Submission.objects.filter(submission_id=new_id).exists():
                    new_id = generate_submission_id()  
                    attempts += 1
                    if attempts >= max_attempts:
                        
                        new_id = f"SUB_{uuid.uuid4().hex[:8].upper()}"
                        break
                
                self.submission_id = new_id
            super().save(*args, **kwargs)