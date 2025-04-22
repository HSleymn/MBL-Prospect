from django.contrib import admin
from .models import Product, Offer, Orderdata, Invoice, Productorder

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('idproduct', 'title', 'price', 'active')
    search_fields = ('title',)

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['idoffer','title','idproduct', 'quantity', 'price']  # Affiche ces colonnes dans la liste des offres
    search_fields = ['idoffer', 'title']  # Permet de rechercher par idoffer ou title dans l'admin

    fields = ['title','idproduct', 'quantity']
    def save_model(self, request, obj, form, change):
        # Avant de sauvegarder, on met à jour le prix de l'offre
        if obj.quantity and obj.idproduct:
            # Calcul du prix en fonction du produit lié et de la quantité
            obj.price = obj.idproduct.price * obj.quantity
        super().save_model(request, obj, form, change)  # Enregistre l'objet dans la base de données


@admin.register(Orderdata)
class OrderdataAdmin(admin.ModelAdmin):
    list_display = ('idorder', 'orderdate','iduser')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('idinvoice','idorder')

@admin.register(Productorder)
class ProductorderAdmin(admin.ModelAdmin):
    list_display = ['idorder', 'idoffer','customer' , 'quantity' ,'price', 'description', 'productorderstatus']
    search_fields = ['idproduct__title', 'customer']  # Recherche dans le titre du produit et de la commande
    readonly_fields = ['price']  # Le champ 'price' est calculé automatiquement, donc il est en lecture seule

    # Enregistrer la classe d'administration


