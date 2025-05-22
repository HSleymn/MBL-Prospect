import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, UserManager
from django.db import models

from commandes.models import Offer


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        print("Extra fields reçus :", extra_fields)  # 🔍 Voilà le print

        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superuser doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superuser doit avoir is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Users(AbstractBaseUser, PermissionsMixin):
    iduser = models.AutoField(db_column='idUser', primary_key=True)  # Field name made lowercase.
    email = models.CharField(unique=True, max_length=50)

    lastname = models.CharField(db_column='lastName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='firstName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(max_length=255, blank=True, null=True)
    roles = models.JSONField(blank=True, null=True)
    userstatus = models.JSONField(db_column='userStatus', blank=True, null=True)  # Field name made lowercase.
    tokkenGoogle = models.CharField(db_column='tokkenGoogle', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mailbalance = models.IntegerField(db_column='mailBalance', blank=True, null=True,default=0)  # Field name made lowercase.

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    class Meta:
        db_table = 'Users'
        managed = True
        verbose_name_plural= "Users"
        verbose_name="User"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class Domain(models.Model):
    idDomain = models.AutoField(primary_key=True)
    domain_name = models.CharField(max_length=50)

    # Ajoute une méthode __str__ pour une représentation lisible
    def __str__(self):
        return self.domain_name

    # Définir une option Meta pour le nom de la table dans la base de données
    class Meta:
        managed = True  # Assure-toi que c'est bien `managed=True` pour que Django gère la table
        verbose_name_plural = "Domains"
        verbose_name = "Domain"
        db_table = 'Domains'

class Contact(models.Model):
    idcontact = models.AutoField(primary_key=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, null=True)
    email = models.CharField(unique=True, max_length=500)
    google_id = models.CharField(unique=True, max_length=50)
    name = models.CharField( max_length=50, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    postalcode = models.CharField( max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField( max_length=20, blank=True, null=True)
    site = models.CharField(max_length=255, blank=True, null=True)
    rating = models.FloatField( blank=True, null=True)  # Field name made lowercase.
    reviews = models.IntegerField( blank=True, null=True)  # Field name made lowercase.
    businessstatus = models.CharField(max_length=50, blank=True, null=True)
    location_link = models.CharField(max_length=255, blank=True, null=True)

    lastsend = models.DateTimeField( blank=True, null=True)
    category_text = None  # pas stocké en base
    class Meta:
        managed = True  # Assure-toi que c'est bien `managed=True` pour que Django gère la table
        db_table = 'Contact'

    def save(self, *args, **kwargs):
        if self.category_text:
            cleaned = self.category_text.strip().lower().capitalize()

            # Essaye de trouver le Domain correspondant (insensible à la casse)
            domain_obj = Domain.objects.filter(name__iexact=cleaned).first()

            self.domain = domain_obj

        super().save(*args, **kwargs)


class MailSent(models.Model):
    iduser = models.ForeignKey('Users', on_delete=models.CASCADE, db_column='idUser', related_name='mails_sent')
    idcontact = models.ForeignKey('Contact', on_delete=models.CASCADE, db_column='idContact', related_name='mails_received')
    send_date = models.DateTimeField(db_column='sendDate')
    opened = models.BooleanField(default=False)
    class Meta:
        db_table = 'MailSent'
        managed = True
        unique_together = ('iduser', 'idcontact')
        verbose_name_plural= "MailSent"
        verbose_name="MailSent"


class Cart(models.Model):

    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Cart'
        managed = True
        verbose_name_plural = "Carts"
        verbose_name = "Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'CartItem'
        managed = True
        unique_together = ('cart', 'offer')  # Pour éviter les doublons
        verbose_name_plural = "CartItems"
        verbose_name = "CartItem"



