from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group, Permission 


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=350)
    phone = models.CharField(unique=True, max_length=11)
    state = models.CharField(max_length=122)
    facility = models.CharField(max_length=350)
    usercategory = models.CharField(max_length=65)

    # Add other custom fields if needed
    groups = models.ManyToManyField(Group, verbose_name='Groups', blank=True, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, verbose_name='User permissions', blank=True, related_name='customuser_set')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


# Create your models here.
class AllUsers(models.Model):
    userid = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=350)
    email = models.CharField(unique=True, max_length=350)
    phone = models.CharField(unique=True, max_length=11)
    state = models.CharField(max_length=122)
    facility = models.CharField(max_length=350)
    usercategory = models.CharField(max_length=65)
    password = models.CharField(max_length=364, blank=True, null=True)
    last_login = None  # Disable the last_login field

   

    class Meta:
        managed = False
        db_table = 'all_users'

class CervicData(models.Model):
    patient_id = models.CharField(max_length=25, blank=True, null=True)
    age = models.CharField(max_length=3, blank=True, null=True)
    mode = models.CharField(max_length=45, blank=True, null=True)
    image_base64 = models.TextField()
    imagetype1 = models.CharField(max_length=25, blank=True, null=True)
    aceticacid_base64 = models.TextField(blank=True, null=True)
    imagetype2 = models.CharField(max_length=25, blank=True, null=True)
    lugolsiodine_base64 = models.TextField(blank=True, null=True)
    imagetype3 = models.CharField(max_length=25, blank=True, null=True)
    initial_diagnosis = models.CharField(max_length=45, blank=True, null=True)
    initial_diagnosis_other = models.CharField(max_length=1000, blank=True, null=True)
    initial_diagnosis_by = models.CharField(max_length=100, blank=True, null=True)
    final_diagnosis = models.CharField(max_length=45, blank=True, null=True)
    final_diagnosis_other = models.CharField(max_length=1000, blank=True, null=True)
    final_diagnosis_by = models.CharField(max_length=125, blank=True, null=True)
    treatment_options = models.CharField(max_length=95, blank=True, null=True)
    comment = models.CharField(max_length=1000, blank=True, null=True)
    final_diag_comment = models.CharField(max_length=1000, blank=True, null=True)
    timestamp_id = models.CharField(max_length=65, blank=True, null=True)
    state = models.CharField(max_length=25, blank=True, null=True)
    facility = models.CharField(max_length=125, blank=True, null=True)
    date_submitted = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cervic_data'


class CervicTreatment(models.Model):
    patient_id = models.CharField(max_length=30)
    received_treatment = models.CharField(max_length=30)
    date_trtmt_rec = models.DateField(blank=True, null=True)
    reg_date = models.DateTimeField(blank=True, null=True)
    cervic_data_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cervic_treatment'


class Chattabox(models.Model):
    chat_id = models.AutoField(primary_key=True)
    from_user = models.CharField(max_length=655, blank=True, null=True)
    to_user = models.CharField(max_length=655, blank=True, null=True)
    message = models.CharField(max_length=350, blank=True, null=True)
    msg_status = models.CharField(max_length=25, blank=True, null=True)
    chat_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chattabox'
