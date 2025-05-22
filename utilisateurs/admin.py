from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from import_export import fields, resources
from django.urls import reverse
from import_export.widgets import ForeignKeyWidget

from .models import Users, Contact, MailSent, Domain


admin.site.site_header = 'Mon Admin'
admin.site.site_title = 'Administration'
admin.site.index_title = format_html(
    'Tableau de bord <a style="float:right; font-size:14px;" href="../../">>🏠 Accueil</a>'
    )


@admin.register(Users)
class UsersAdmin(BaseUserAdmin):
    list_display = ('email','iduser',  'firstname', 'lastname','tokkenGoogle','mailbalance', 'roles','userstatus', 'is_staff', 'is_superuser')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Infos personnelles', {'fields': ('firstname', 'lastname','mailbalance', 'tokkenGoogle')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'roles', 'userstatus')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'firstname', 'lastname', ),
        }),
    )




class ContactResource(resources.ModelResource):
    # Champ personnalisé qui lit la colonne Excel "catégorie"
    categorie = fields.Field(column_name='category')

    class Meta:
        model = Contact
        exclude = ('idcontact', 'lastsend')
        import_id_fields = ()

    def before_import_row(self, row, **kwargs):
        # Nettoie la catégorie : minuscule + majuscule sur première lettre
        if "category" in row and row["category"]:
            original = row["category"].strip()
            formatted = original.lower().capitalize()

            # Cherche ou crée le Domain correspondant
            domain_obj, _ = Domain.objects.get_or_create(domain_name=formatted)
            print(domain_obj.idDomain)
            # Remplace le texte par le nom exact (pour le widget ForeignKey)
            row["domain"] = domain_obj.pk

@admin.register(Contact)
class TonModelAdmin(ImportExportModelAdmin):
    resource_class = ContactResource
    list_display = ('idcontact', 'domain' , 'email','google_id','name','phone','city','rating','reviews','lastsend',)

    search_fields = ('name', 'email', 'city', 'google_id')
    list_filter = ('city', 'businessstatus')

    #ordering = ('-lastsend',)

@admin.register(MailSent)
class MailSentAdmin(admin.ModelAdmin):
    list_display = [ 'iduser', 'idcontact', 'send_date', 'opened']


from import_export import resources
from .models import Domain

class DomainResource(resources.ModelResource):
    class Meta:
        model = Domain
        import_id_fields = []  # Vide, très important
        fields = ()            # Aucun champ lu depuis le fichier
        skip_unchanged = True
        report_skipped = True

    def before_import_row(self, row, **kwargs):
        category = row.get("category", "").strip().capitalize()
        if category:
            Domain.objects.get_or_create(domain_name=category)


@admin.register(Domain)
class DomainAdmin(ImportExportModelAdmin):
    resource_class = DomainResource
    list_display = ('idDomain', 'domain_name')





