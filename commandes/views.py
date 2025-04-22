from django.http import JsonResponse
from .models import Offer

def get_offer_price(request, offer_id):
    try:
        offer = Offer.objects.get(pk=offer_id)
        product_price = offer.idproduct.price
        return JsonResponse({'price': product_price})
    except Offer.DoesNotExist:
        return JsonResponse({'price': 0})
