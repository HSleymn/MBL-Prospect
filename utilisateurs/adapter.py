from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
import logging

logger = logging.getLogger(__name__)

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Log pour vérifier ce qui arrive dans sociallogin
        logger.info("Données de sociallogin : %s", sociallogin)

        token = getattr(sociallogin, 'token', None)
        account = sociallogin.account

        if account:
            logger.info(f"Compte trouvé avec ID : {account.id}")
            if account.pk:
                logger.info("Le compte est sauvegardé.")
                if token:
                    token.account = account
                    token.save()
                    logger.info("✅ Token sauvegardé avec succès.")
                else:
                    logger.warning("❌ Aucun token trouvé.")
            else:
                logger.warning("❌ Le compte n'est pas encore sauvegardé.")
        else:
            logger.warning("❌ Aucun compte trouvé dans le sociallogin.")
