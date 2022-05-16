from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
# Create your models here.

class UserManager(BaseUserManager):    
   
   use_in_migrations = True    
   
   def create_user(self, email, nickname, password):        
       
       if not email:            
           raise ValueError('must have user email')
       if not password:            
           raise ValueError('must have user password')

       user = self.model(            
           email=self.normalize_email(email),
           nickname=nickname              
       )        
       user.set_password(password)        
       user.save(using=self._db)        
       return user

   def create_superuser(self, email, nickname, password):        
   
       user = self.create_user(            
           email = self.normalize_email(email),
           nickname=nickname,                       
           password=password        
       )
       user.is_admin = True
       user.is_superuser = True
       user.save(using=self._db)
       return user 

class Token(models.Model):
    token = models.CharField('토큰', max_length=400, unique=True)
    piece = models.CharField('토큰조각', default='', max_length=100)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('아이디(이메일)', max_length=255, unique=True)
    nickname = models.CharField('닉네임', max_length=20, unique=True)
    password = models.CharField('비밀번호', max_length=100)
    is_active = models.BooleanField('활동여부', default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self) -> str:
        return self.email

    
    @property
    def is_staff(self) -> bool:
        return self.is_admin
    
    objects = UserManager()

