from allauth.socialaccount.models import SocialToken
from allauth.socialaccount.signals import social_account_added
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Cart
from allauth.account.signals import user_logged_in, user_signed_up


@receiver(social_account_added)
def save_google_token(request, sociallogin, **kwargs):
    if sociallogin.account.provider == 'google':
        token = SocialToken.objects.get(account=sociallogin.account)
        user = sociallogin.user
        user.tokkenGoogle = token.token
        user.save()

User = get_user_model()


@receiver(user_signed_up)
def populate_user_social_data(request, user, **kwargs):
    social_account = user.socialaccount_set.first()
    if social_account:
        data = social_account.extra_data
        user.firstname = data.get('given_name', '')
        user.lastname = data.get('family_name', '')
        user.save()

@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)

@receiver(user_logged_in)
def debug_token(sender, request, user, **kwargs):
    token = SocialToken.objects.filter(account__user=user).first()
    if token:
        print("Token trouvé :", token.token)
    else:
        print("Aucun token trouvé pour", user)