from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, nombre, rol, password=None):
        if not email:
            raise ValueError("El usuario debe tener un email")
        email = self.normalize_email(email)
        user = self.model(email=email, nombre=nombre, rol=rol)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, nombre, rol='admin', password=None):
        user = self.create_user(email, nombre, rol, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
class User(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('admin', 'Administrador'),
        ('cliente', 'Cliente'),
        ('camarero', 'Camarero'),
        ('cocinero', 'Cocinero'),
    )

    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=20, choices=ROLES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'rol']

    def __str__(self):
        return self.email
