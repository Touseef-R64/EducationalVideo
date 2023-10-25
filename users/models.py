from django.db import models
import uuid
from users.utils import Util
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, email, first, last, payment_picture, is_agent=False, password=None,):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first,
            last_name=last,
            payment_picture=payment_picture,
            is_agent=is_agent
        )
     
        user.set_password(password)
        user.save(using=self._db)
       
        return user

    

    def create_superuser(self, email, first, last, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first,
            last_name=last
        )
        
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    contact = models.CharField(max_length=20, unique=True)
    has_paid = models.BooleanField(default=False)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    from_agent = models.ForeignKey('self', related_name='signed_Users',on_delete=models.SET_NULL,  blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_picture = models.ImageField(upload_to=Util.custom_image_filename,null=True, blank=True)
    cnic_front = models.ImageField(upload_to=Util.custom_image_filename,null=True, blank=True)
    cnic_back = models.ImageField(upload_to=Util.custom_image_filename,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have the specific permission?"
        return self.is_admin
    
    def has_module_perms(self, app_label):
        "Does the user have permission to view the app `app_label`? "
        return True
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin