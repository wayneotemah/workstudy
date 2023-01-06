import uuid
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin)
from django.utils.translation import gettext_lazy  as _

class CustomUserManager(BaseUserManager):

    def create_user(self, email,phone_number,password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        if not phone_number:
            raise ValueError(_('The phone number must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password,phone_number, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        if not phone_number:
            raise ValueError(_('The phone number must be set'))

        user = self.create_user(email,phone_number, password, **extra_fields)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser,PermissionsMixin):
    """
    priamry table to authentication with email/phone number
    """
    email = models.EmailField(_('email address'),max_length=255,unique=True,)
    phone_number = PhoneNumberField(_('phone number'),blank=True,null = False,unique=True)
    date_joined      = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login       = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin         = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=True)
    is_staff         = models.BooleanField(default=False)
    is_superuser     = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('phone_number',)  # type: ignore

    objects = CustomUserManager()

    def get_email_address(self):
        # The user is identified by their email address
        return self.email

    def get_phone_number(self):
        # The user is identified by their phone address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @staticmethod
    def user_exists(x):
            result = CustomUser.objects.filter(email = x)
            return False if not result else True
        


class Account(models.Model):
    """
    table for user details linked to the primary user table
    """
    account_uuid = models.UUIDField(_("User ID"),primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, verbose_name=_("Account's credentials"), on_delete=models.CASCADE)
    first_name = models.CharField(_('First name'),blank = True, null =True,max_length = 100)
    last_name = models.CharField(_('Last name'),blank = True, null = True,max_length = 100)
    is_supervisor = models.BooleanField(_('supervisor'),default = False)
    
    def __str__(self):
        return self.first_name
    
    def supervisor_status(self):
        return self.is_supervisor

    @staticmethod
    def get_account(x):
        account = Account.objects.get(user = x)
        return account
    
    
