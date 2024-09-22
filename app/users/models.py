from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.forms import ValidationError
from django.utils.text import slugify

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, name=None, role=None, is_active=True, created_by=None):
        user = self.model(
            username=username,
            name=name,
            role=role,
            is_active=is_active,
            created_by=created_by,
            slug=slugify(username),
        )
        user.set_password(password)
        user.full_clean()  # This will call the clean() method to validate the model
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, name=None, role='ADMIN'):
        user = self.create_user(
            username=username,
            password=password,
            name=name,
            role=role,
            is_active=True,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('APPROVAL', 'Approval'),
        ('USER', 'User'),
    )

    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='USER')
    is_staff = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='created_users' 
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'role']

    def clean(self):
        # Custom validation logic
        if not self.username:
            raise ValidationError("The Username field is required")
        if not self.name:
            raise ValidationError("The Name field is required")
        if not self.role:
            raise ValidationError("The Role field is required")

        # Ensure unique slug based on username
        if CustomUser.objects.filter(slug=slugify(self.username)).exclude(pk=self.pk).exists():
            raise ValidationError("A user with this slug already exists")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        # Admins have all permissions
        if self.role == 'ADMIN':
            return True
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        return self.is_staff  # Define module-level permissions for this user
