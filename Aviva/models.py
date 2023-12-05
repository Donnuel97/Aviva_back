# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AllUsers(models.Model):
    userid = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=350)
    email = models.CharField(unique=True, max_length=350)
    phone = models.CharField(unique=True, max_length=11)
    state = models.CharField(max_length=122)
    facility = models.CharField(max_length=350)
    usercategory = models.CharField(max_length=65)
    password = models.CharField(max_length=364, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'all_users'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


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


class DashboardCustomuser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    email = models.CharField(unique=True, max_length=254)
    fullname = models.CharField(max_length=350)
    phone = models.CharField(unique=True, max_length=11)
    state = models.CharField(max_length=122)
    facility = models.CharField(max_length=350)
    usercategory = models.CharField(max_length=65)

    class Meta:
        managed = False
        db_table = 'dashboard_customuser'


class DashboardCustomuserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(DashboardCustomuser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dashboard_customuser_groups'
        unique_together = (('customuser', 'group'),)


class DashboardCustomuserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(DashboardCustomuser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dashboard_customuser_user_permissions'
        unique_together = (('customuser', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
