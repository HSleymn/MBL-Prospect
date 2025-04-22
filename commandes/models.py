from django.db import models
from django.template.defaultfilters import title


class Product(models.Model):
    idproduct = models.AutoField(db_column='idProduct', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=12, blank=False, null=False)
    description = models.CharField(max_length=50, blank=True, null=True)
    price = models.IntegerField(blank=False, null=False)
    active = models.BooleanField(default=True)
    class Meta:
        managed = True
        db_table = 'Product'
    def __str__(self):
        return self.title



class Invoice(models.Model):
    idinvoice = models.AutoField(db_column='idInvoice', primary_key=True)  # Field name made lowercase.
    idorder = models.OneToOneField('Orderdata', models.DO_NOTHING, db_column='idOrder')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Invoice'

class Orderdata(models.Model):
    idorder = models.AutoField(db_column='idOrder', primary_key=True)  # Field name made lowercase.
    orderdate = models.DateTimeField(db_column='orderDate', blank=False, null=False)  # Field name made lowercase.
    iduser = models.ForeignKey('utilisateurs.Users', models.DO_NOTHING, db_column='idUser')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'OrderData'
    def __str__(self):
        return str(self.idorder)
    def save(self, *args, **kwargs):
        print(f'Nom de l\'utilisateur : {self.iduser.firstname} {self.iduser.lastname}')

        super().save(*args, **kwargs)


class Offer(models.Model):
    title = models.CharField(max_length=12, blank=False, null=False)
    idproduct = models.ForeignKey('Product', models.DO_NOTHING, db_column='idProduct', blank=False, null=False)  # Field name made lowercase.
    idoffer = models.AutoField(db_column='idOffer', primary_key=True, blank=False, null=False)  # Field name made lowercase.
    quantity = models.IntegerField(blank=False, null=False)
    price = models.IntegerField(blank=False, null=False)

    offerstatus = models.BooleanField(default=True)
    class Meta:
        managed = True
        db_table = 'Offer'
    def __str__(self):
        return self.title



class Productorder(models.Model):
    idorder = models.ForeignKey(Orderdata, models.DO_NOTHING, db_column='idOrder')  # Field name made lowercase.
    idoffer = models.ForeignKey(Offer, models.DO_NOTHING, db_column='idOffer', related_name='productorder_idoffer_set')  # Field name made lowercase.
    customer = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(blank=False, null=False)
    price = models.IntegerField(blank=False, null=False)
    description = models.CharField(max_length=50, blank=True, null=True)
    productorderstatus = models.JSONField(db_column='productOrderStatus', blank=True, null=True)  # Field name made lowercase.



    def save(self, *args, **kwargs):
        if self.idorder:
            self.customer  = self.idorder.iduser
        if self.idoffer.idproduct and self.quantity:
            self.price = self.idoffer.price * self.quantity
        super().save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'ProductOrder'
        unique_together = (('idorder', 'idoffer'),)

