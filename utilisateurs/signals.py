from allauth.socialaccount.models import SocialToken
from allauth.socialaccount.signals import social_account_added
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.signals import request_started
from django.contrib.sessions.models import Session
from django.dispatch import receiver
import os

@receiver(social_account_added)
def save_google_token(request, sociallogin, **kwargs):
    if sociallogin.account.provider == 'google':
        token = SocialToken.objects.get(account=sociallogin.account)
        user = sociallogin.user
        user.tokkenGoogle = token.token
        user.save()

