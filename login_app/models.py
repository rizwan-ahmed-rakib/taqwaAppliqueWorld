from django.db import models
# to create a customer user model and adnin panel
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy

# to autometically create one to one objects
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class MyUserManager(BaseUserManager):  # for handling user
    """a custom manager to deak with emails as unique identifoer"""

    def _create_user(self, email, password, **extra_fields):  # for use email and password for creatong user
        """""create and save a user with a given enail and password"""

        if not email:
            raise ValueError("the email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is staff')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is superuser=True')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(
        gettext_lazy('staff status'),  #
        default=False,
        help_text=gettext_lazy('desegnet whether the user can login this site')  # )
    )
    is_active = models.BooleanField(
        gettext_lazy('active'),  #
        default=True,
        help_text=gettext_lazy(
            'desegnation wheather this user should be terated as active.unselect this instead of deleting accounts')
        # '
        # '
    )
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profilePicture/', blank=True)
    """hwre we have created one to one model relationship with User & Profile"""
    username = models.CharField(max_length=264, blank=True)
    full_name = models.CharField(max_length=264, blank=True)
    address_1 = models.TextField(max_length=300, blank=True)
    city = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    date_joined = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username + "'s profile"

    def is_fully_filled(self):
        fields_names = [f.name for f in self._meta.get_fields()]
        for field_name in fields_names:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()  # if any change goes on User model then effect goes on Profile model,related_name=profile
