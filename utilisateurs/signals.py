from allauth.socialaccount.models import SocialToken
from allauth.socialaccount.signals import social_account_added
from django.dispatch import receiver

@receiver(social_account_added)
def save_google_token(request, sociallogin, **kwargs):
    if sociallogin.account.provider == 'google':
        token = SocialToken.objects.get(account=sociallogin.account)
        user = sociallogin.user
        user.tokkenGoogle = token.token
        user.save()
