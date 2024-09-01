from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Manager for CustomUser, providing helper methods to create regular users
    and superusers with email-based authentication.
    """
     
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        
        Parameters:
        - email: The email address of the user (required).
        - password: The password for the user (optional).
        - extra_fields: Additional fields to set on the user.

        Raises:
        - ValueError: If no email is provided.

        Returns:
        - user: The created user instance.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        
        Superusers have special permissions and should be marked as staff and
        superuser in the system.

        Parameters:
        - email: The email address of the superuser (required).
        - password: The password for the superuser (optional).
        - extra_fields: Additional fields to set on the superuser.

        Raises:
        - ValueError: If `is_staff` or `is_superuser` are not set to True.

        Returns:
        - user: The created superuser instance.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model extending AbstractBaseUser and PermissionsMixin
    to provide email-based authentication and user permissions.
    """

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        """
        Return the string representation of the user, which is the user's email.
        """
        return self.email

    def has_perm(self, perm, obj=None):
        """
        Check if the user has a specific permission. Superusers have all permissions.
        
        Parameters:
        - perm: The permission to check.
        - obj: Optional object for permission checking.

        Returns:
        - bool: True if the user is a superuser, False otherwise.
        """
        return self.is_superuser

    def has_module_perms(self, app_label):
        """
        Check if the user has permissions for a specific app. Superusers have 
        permissions for all apps.
        
        Parameters:
        - app_label: The label of the app to check permissions for.

        Returns:
        - bool: True if the user is a superuser, False otherwise.
        """
        return self.is_superuser
