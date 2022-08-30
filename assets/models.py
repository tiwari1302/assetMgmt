from django.db import models
import uuid
from django.contrib.auth.models import User
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager

# Create your models here.

class User_manager(BaseUserManager):
    def create_user(self, username, email, gender, nickname, password):
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, gender=gender, nickname=nickname)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, email, gender, password, nickname=None):
        user = self.create_user(username=username, email=email, gender=gender, nickname=nickname, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(PermissionsMixin, AbstractBaseUser):
    username = models.CharField(max_length=32, unique=True, )
    email = models.EmailField(max_length=32)
    gender_choices = [("M", "Male"), ("F", "Female"), ("O", "Others")]
    gender = models.CharField(choices=gender_choices, default="M", max_length=1)
    nickname = models.CharField(max_length=32, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    REQUIRED_FIELDS = ["email", "gender"]
    USERNAME_FIELD = "username"
    objects = User_manager()

    def __str__(self):
        return self.username

class assetType(models.Model):
    title = models.CharField(max_length=150)

    # @property
    # def get_type(self):
    #     return asset.objects.filter(asset_type=self.id)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name_plural = 'Asset Types'

def get_superuser():
    su_user = User.objects.filter(is_superuser=True).first()
    if su_user:
        return su_user.pk
    raise DoesNotExist('Please add Super User')

class asset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)
    asset_type = models.ForeignKey('assetType', on_delete=models.CASCADE, null=True)
    asset_name = models.CharField(max_length=30, null=True) #unique=True
    location = models.CharField(max_length=30, null=True)
    brand = models.CharField(max_length=30, null=True)
    purchase_year = models.PositiveIntegerField(blank=True, null=True)
    isActive = models.BooleanField(default=True, null=True)
    currentOwner = models.ForeignKey(User, default=get_superuser, null=False, on_delete=models.SET_DEFAULT) #User.objects.get(is_superuser=True).id