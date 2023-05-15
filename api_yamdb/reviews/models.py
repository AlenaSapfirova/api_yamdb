from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
# SUPERUSER = 'superuser'

TYPE_MODELS = [
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN),
    # (SUPERUSER,SUPERUSER)
]



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, 
                              blank=False,
                              max_length=250)
    username = models.CharField(max_length=100, unique=True, blank=False, validators=[RegexValidator(regex='^[\w.@+-]+\Z')])
    first_name = models.CharField(blank=False, max_length=20)
    last_name = models.CharField(max_length=50, blank=False)
    role = models.CharField(max_length=15, choices=TYPE_MODELS)
    bio = models.TextField()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    @property
    def is_admin(self):
        return self.role == ADMIN
    
    @property
    def is_moderator(self):
        return self.role == MODERATOR
    
    @property
    def is_user(self):
        return self.role==USER
    
   
    def __str__(self):
        return f'{self.username} {self.email}'
    
    
    
