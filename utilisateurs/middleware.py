# accounts/middleware.py
import logging

logger = logging.getLogger(__name__)

class DebugSocialLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/accounts/google/"):
            logger.info(f"🔍 Request PATH: {request.path}")
            logger.info(f"🔍 Method: {request.method}")
            logger.info(f"🔍 POST Data: {request.POST}")
            logger.info(f"🔍 Session: {request.session.items()}")
        return self.get_response(request)
