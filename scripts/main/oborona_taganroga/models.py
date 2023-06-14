from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ValidationError
from rest_framework.authtoken.models import Token
from django.db import models
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
import secrets
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  

SEX_VALUES = (
    ("m", "Мужчина"),
    ("f", "Женщина")
)

SIDE_VALUES = (
    ('ru', 'Русские войска'),
    ('en', 'Англо-Французские войска')
)

class UserRegistrationModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class ParticipantManager(BaseUserManager):
	def create_user(self, firstname, lastname, sex, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not firstname:
			raise ValueError('Users must have a username')

		user = self.model(
			email=email,
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
	
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Participant(AbstractBaseUser):
    firstname     = models.CharField(max_length=100)#
    lastname      = models.CharField(max_length=100)#
    middlename    = models.CharField(max_length=100, null=True, blank=True, default=None)
    birthday      = models.DateField( null=True, blank=True, default=None)
    phonenumber   = PhoneNumberField(blank=True, null=True)
    # role          = models.CharField(max_length=120, blank=True, null=True, default=None)
    password      = models.CharField(max_length=120)#
    # events        = models.CharField(max_length = 240, blank=True, null=True, default=None)
    entrys        = models.ManyToManyField('Entry')
    sex           = models.CharField(choices=SEX_VALUES, max_length=1) #
    email         = models.EmailField(max_length = 100, unique=True)#
    is_admin      = models.BooleanField(default = False)
    is_sponsor        = models.BooleanField(default = False)
    is_active       = models.BooleanField(default=False)
    last_login          = models.DateTimeField(verbose_name="last login", auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    objects = ParticipantManager()


    def __str__(self):
        return self.firstname


class Event(models.Model):
    name = models.CharField(max_length=60)
    pic_url = models.URLField(blank=True, null=True)
    brief_disc = models.CharField(max_length=120)
    full_disc = models.CharField(max_length=500)
    adress = models.CharField(max_length=120, blank=True, null=True, default=None)
    time_start = models.DateTimeField(blank=True, null=True)
    time_end = models.DateTimeField(blank=True, null=True)
    roles = models.ManyToManyField('Role')
    coord_long = models.DecimalField(max_digits=16, decimal_places=6)
    coord_lat = models.DecimalField(max_digits=16, decimal_places=6)
    is_epic = models.BooleanField(default = False)
    phonenumber   = PhoneNumberField(null=True, default=None)

    class Meta:
        ordering = ['time_start']
    
    def __str__(self):
        return self.name

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


#MAKE FIELD'S ATTRIBUTES
# class Info(models.Model):
#     discription = models.CharField(max_length=240, null=True)
#     phonenumber   = PhoneNumberField(unique=True, null=True, default=None)
#     more_info = models.BooleanField(default = False)

#MAKE FIELD'S ATTRIBUTES
class Role(models.Model):
    role_name = models.CharField(max_length=60)
    verbose_name = models.CharField(max_length=60)
    discription = models.CharField(max_length=1024, null=True)
    phonenumber   = PhoneNumberField(null=True, default=None)
    more_info = models.BooleanField(default = False)
    # info = models.ManyToManyField('Info')


class Entry(models.Model):
    user = models.ForeignKey('Participant', on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    role = models.ForeignKey('Role', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user','event', 'role')
        ordering = ['event']


class AdditionalInfo(models.Model):
    user = models.ForeignKey(Participant, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    side = models.CharField(choices=SIDE_VALUES, max_length=2)
    any_weapon = models.BooleanField(default = False)
    any_costume = models.BooleanField(default = False)
    stay_in_barrack = models.BooleanField(default = False)
    chest = models.DecimalField(max_digits=16, decimal_places=6, null=True)
    waist = models.DecimalField(max_digits=16, decimal_places=6, null=True)
    hips = models.DecimalField(max_digits=16, decimal_places=6, null=True)
    height = models.DecimalField(max_digits=16, decimal_places=6, null=True)
    shoe_size = models.DecimalField(max_digits=16, decimal_places=6, null=True)


class HoReCa(models.Model):
    name = models.CharField(max_length = 64)
    discription = models.CharField(max_length = 256)
    coord_long = models.DecimalField(max_digits=16, decimal_places=6)
    coord_lat = models.DecimalField(max_digits=16, decimal_places=6)
    phonenumber = PhoneNumberField(null=True)


class PromoCodes(models.Model):
    code = models.CharField(max_length=8, unique=True)
    user = models.ForeignKey('Participant', on_delete=models.CASCADE, null = True, default = None)
    # is_active = models.BooleanField(default = False)
    class Meta:
        unique_together = ('user','code')

    @classmethod
    def create_code(self, number):
        code_alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
        promo_code = "".join(secrets.choice(code_alphabet) for i in range(8))
        print(promo_code)
        print(number)
        return promo_code


class InfoWindow(models.Model):
    name = models.CharField(max_length = 64)
    discription = models.CharField(max_length = 1000)
    pic_url = models.URLField(blank=True, null=True)
    phonenumber   = PhoneNumberField(blank=True, null=True)



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}".format(reset_password_token.key)

    send_mail(
        # title:
        "Восстановление пароля участника фестиваля \"Оборона Таганрога 1855 года\"",
        # message:
        email_plaintext_message,
        # from:
        "daniil-kochubey@yandex.ru",
        # to:
        [reset_password_token.user.email]
    )