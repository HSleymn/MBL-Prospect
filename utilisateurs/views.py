from datetime import timedelta

import stancer
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from commandes.models import Offer, Productorder, Orderdata, Invoice
from .forms import SignupForm, CustomAuthenticationForm
from .models import MailSent, Cart, CartItem, Domain, Contact
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import logout
from .templates.payments.payments import create_card, create_payment
from .templates.utils.geography import get_cities_from_geo_zone, get_department_codes
from .utils import send_mail_to_contacts, fetch_contacts


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            list(messages.get_messages(request))
            messages.success(request, "Bienvenue, vous êtes connecté !")
            if user.is_superuser:  # ou user.is_staff
                return redirect('/admin/')  # Redirige vers le panel admin Django
            else:
                return redirect('user_panel')  # Redirige vers la page d'accueil ou une page spécifique
        else:
            messages.error(request, "Identifiants invalides.")
    else:
        form = AuthenticationForm()
    # print(request.user)
    return render(request, 'users/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            role_choisi = form.cleaned_data['roles']
            request.user = form.save()
            request.user.roles = role_choisi
            request.user.save()
            return redirect('login')  # redirige vers la page de login
    else:
        form = SignupForm()

    return render(request, 'users/signup.html', {'form': form})
# Vue de déconnexion
@login_required
def logout_view(request):
    logout(request)  # déconnecte l'utilisateur
    return redirect('login')  # redirige vers la page de login (ou autre)
# Pas besoin de créer une vue manuelle, Django le fait déjà avec LogoutView
@login_required
def panel(request):
    user = request.user  # Récupère l'utilisateur connecté
    return render(request, 'users/panel.html', {'user': user})

@login_required
def user_panel(request):
    if not request.headers.get('HX-Request'):
        return redirect('panel')
    user = request.user  # Récupère l'utilisateur connecté
    return render(request, 'users/user_panel.html', {'user': user})

@login_required
def offer_panel(request):
    if not request.headers.get('HX-Request'):
        return redirect('panel')
    user = request.user  # Récupère l'utilisateur connecté
    offers = Offer.objects.all()  # ou 'user=user' selon ton modèle

    return render(request, 'users/offer_panel.html', {'user': user, 'offers':offers})
# Dictionnaire de correspondance texte → code postal
DEPARTEMENT_CODES = {
    "val d'oise": "95",
    "paris": "75",
    "hauts de seine": "92",
    "seine saint denis": "93",
    "yvelines": "78",
    "seine et marne": "77",
    "essonne": "91",
    "val de marne": "94",
    "france": "",  # Vide pour inclure tout
}
@login_required
def mailsent_panel(request):
    if not request.headers.get('HX-Request'):
        return redirect('panel')
    user = request.user

    if user.mailbalance == 0:
        return render(request, 'users/solde_insuffisant.html')

    domains = Domain.objects.all()
    mails = MailSent.objects.filter(iduser=user.iduser)
    print(request.method == "POST")
    if request.method == "POST":
        subject= request.POST.get('subject')
        body= request.POST.get('message')
        geo_zone = request.POST.get('geo_zone', '').lower().strip()
        quantity = int(request.POST.get('quantity'))
        domain = request.POST.get('domain')
        contacts_query = Contact.objects.all()

        # Si une zone géographique a été renseignée
        if geo_zone:
            matched = False
            for dept_name, dept_code in DEPARTEMENT_CODES.items():
                if dept_name in geo_zone:
                    if dept_code:
                        contacts_query = contacts_query.filter(postalcode__startswith=dept_code)
                    matched = True
                    break
            if not matched:
                # Sinon essayer un filtre ville direct
                contacts_query = contacts_query.filter(city__icontains=geo_zone)

            # Récupération du fichier
        attachment = request.FILES.get('attachment')  # <-- voilà le fichier



        contacts_list, a = fetch_contacts(Contact.objects.all(), quantity, domain, )
        # for contacta in Contact.objects.all():
        #     print(contacta.email + " numero 1 2 3")
        print(contacts_list)

        # Ici tu peux utiliser `contacts_query` pour envoyer des mails
        # for c in contacts_list:
        #     print(f"Mail à envoyer à : {c.email} et comme sujet {subject}")
    # print(user.roles)
    if user.roles == "student":
        return render(request, 'users/mailsent_panel_student.html', {
        'user': user,
        'mails': mails,
        'domains': domains,
        # Optionnel : 'contacts': contacts_query
    })
    elif user.roles == "business":
        return render(request, 'users/mailsent_panel_business.html', {
        'user': user,
        'mails': mails,
        'domains': domains,
        # Optionnel : 'contacts': contacts_query
    })



@login_required
def dashboard_panel(request):
    if not request.headers.get('HX-Request'):
        return redirect('panel')
    user = request.user  # Récupère l'utilisateur connecté
    return render(request, 'users/dashboard_panel.html', {'user': user})

@login_required
def payment_view(request, cart_id):

    user = request.user  # Récupère l'utilisateur connecté

    try:
        cart = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        return redirect('view_cart')  # Redirige si l'offre n'existe pas
    items = cart.items.select_related('offer')
    total = sum(item.offer.price * item.quantity for item in items)
    for item in items:
        item.total_price = item.offer.price * item.quantity
    return render(request, 'users/payment.html', {
        'user': user,
        'cart': cart,
        'total': total,
        'items': items,

    })

@login_required
def confirm_payment_view(request, cart_id):
    user = request.user  # Récupère l'utilisateur connecté
    cart = Cart.objects.get(id=cart_id)
    items = cart.items.select_related('offer')
    total = sum(item.offer.price * item.quantity for item in items)


    if request.method == "POST":

        number = request.POST.get('number', '').replace(' ', '')
        # print("NUMERO DE CARTE" , str(number))
        exp_month = request.POST.get('exp_month')
        exp_year = request.POST.get('exp_year')
        cvc = request.POST.get('cvc')
        amount = total*100
        conf = stancer.Config()
        conf.keys = ('ptest_Z6oOz6reywqE3kMaWnGoX', 'stest_Jpys47oEnlenCZ5CPIUoD')
        card = stancer.Card()
        card.number = '5555555555554444'
        card.cvc = '123'
        card.exp_month = 2
        card.exp_year = 2023

        customer = stancer.Customer()
        customer.email = 'david@example.net'
        customer.mobile = '+33639980102'
        customer.name = 'David Coaster'

        payment = stancer.Payment()
        payment.description = 'Test Payment Company'
        payment.amount = 100
        payment.currency = 'eur'
        payment.card = card
        payment.customer = customer

        print(payment.send())

        card_response = create_card(number, exp_month, exp_year, cvc)
        card_id = card_response.get('id')
        print(card_id)
        if card_id:

            payment_response = create_payment(amount, card_id)
            print(payment_response.get('status') == 'to_process')

            if not (payment_response.get('status') == 'to_process'):
                return render(request, 'paiement_erreur.html', {"erreur": payment_response})

        orderData = Orderdata.objects.create(
                iduser=user,
                orderdate=timezone.now()
        )
        for item in items:
            productOrder = Productorder.objects.create(
                    idorder=orderData,
                    idoffer=item.offer,
                    customer= user.iduser,
                    quantity=item.quantity,
                    price=item.offer.price * item.quantity,
            )
            # print(item.offer.idproduct.idproduct == settings.MAIL_ID_PRODUCT)
            # print("--------------")
        #Si le produit est un mail il augmente son solde
        if (item.offer.idproduct.idproduct == settings.MAIL_ID_PRODUCT):
                    user.mailbalance += item.offer.quantity * item.quantity
                    user.save()

        invoice = Invoice.objects.create(
                idorder = orderData
        )


        # Ici tu pourrais créer une commande, envoyer un mail, etc.
        messages.success(request, "Votre commande a été validée avec succès !")
        return redirect('panel')
    else:
        return redirect('offers')


@login_required
def view_cart(request):
    if not request.headers.get('HX-Request')    :
        return redirect('panel')

    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('offer')
    total = sum(item.offer.price * item.quantity for item in items)

    return render(request, 'users/cart.html', {
        'items': items,
        'total': total,
        'cart': cart
    })

@login_required
def add_to_cart(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(cart=cart, offer=offer)
    if not created:
        item.quantity += 1
        item.save()

    return
@login_required
def remove_from_cart(request, offer_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, cart=cart, offer_id=offer_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('view_cart')


@login_required
def update_cart(request):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        items = cart.items.all()

        for item in items:
            input_name = f'quantities_{item.id}'
            new_quantity = request.POST.get(input_name)

            if new_quantity is not None:
                try:
                    new_quantity = int(new_quantity)
                    if new_quantity > 0:
                        item.quantity = new_quantity
                        item.save()
                    else:
                        item.quantity = 0
                        item.save()
                        item.delete()
                except ValueError:
                    pass  # ignore les entrées invalides
    total = sum(item.offer.price * item.quantity for item in items)

    return render(request, 'users/cart.html', {
        'items': cart.items.select_related('offer'),
        'total': total,
        "cart": cart,  # ← ajoute bien ceci
    })

def tracking_pixel(request, mail_id):
    mail = get_object_or_404(MailSent, id=mail_id)
    mail.opened = True
    mail.save(update_fields=['opened'])

    # Pixel 1x1 transparent GIF en binaire
    pixel = (
        b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00'
        b'\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00'
        b'\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01'
        b'\x00;'
    )
    return HttpResponse(pixel, content_type='image/gif')
