from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, name=None, role=None, is_active=True):
        if not username:
            raise ValueError("The Username field is required")
        user = self.model(
            username=username,
            name=name,
            role=role,
            is_active=is_active,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password,
            role='ADMIN',
            is_active=True,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


# Custom user model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('APPROVAL', 'Approval'),
        ('USER', 'User'),
    )

    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)  # Field to track if account is enabled/disabled
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='USER')

    # Fields required by PermissionsMixin
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'  # Field to use as login identifier
    REQUIRED_FIELDS = []  # Other required fields for superuser creation (besides username & password)

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        # Admins have all permissions
        if self.role == 'ADMIN':
            return True
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        return self.is_staff  # Define module-level permissions for this user
