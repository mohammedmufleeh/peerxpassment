from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from acme_support import settings

class Department(models.Model):
    name = models.CharField(max_length=255,unique=True)
    description = models.TextField(null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    def create_user(self, email_or_phone, password=None):
        if not email_or_phone:
            raise ValueError('Users must have an email or phone number')
        
        user = self.model(
            email_or_phone=self.normalize_email_or_phone(email_or_phone)
        )
        user.set_password(password)
        user.is_staff = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, phone=None, password=None, **extra_fields):
        if not email and not phone:
            raise ValueError('The Email or Phone field must be set')
        if not password:
            raise ValueError('The password field must be set')
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


    def authenticate(self, email_or_phone=None, password=None):
        try:
            user = User.objects.get(
                models.Q(email=email_or_phone) | models.Q(phone=email_or_phone)
            )

            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def normalize_email_or_phone(self, email_or_phone):
        if '@' in email_or_phone:
            return self.normalize_email(email_or_phone)
        return email_or_phone

class User(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )
    phone = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )
    user_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    role = models.CharField(max_length=255,null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __unicode__(self):
        return int(self.id)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def email_or_phone(self):
        if self.email:
            return self.email
        return self.phone
