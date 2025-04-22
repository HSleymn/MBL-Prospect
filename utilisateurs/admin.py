from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.urls import reverse

from .models import Users, Contact, MailSent


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
    class Meta:
        model = Contact
        exclude = ( 'idcontact', 'lastsend')
        import_id_fields = ()

@admin.register(Contact)
class TonModelAdmin(ImportExportModelAdmin):
    resource_class = ContactResource
    list_display = ('idcontact','email','google_id','name','phone','city','rating','reviews','lastsend',)

    search_fields = ('name', 'email', 'city', 'google_id')
    list_filter = ('city', 'businessstatus')

    #ordering = ('-lastsend',)

@admin.register(MailSent)
class MailSentAdmin(admin.ModelAdmin):
    list_display = [ 'iduser', 'idcontact', 'send_date', 'opened']




