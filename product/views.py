import json

from django.http import HttpResponse

from django.conf import settings

from product.src.get_weather import get_weather
from product.src.recommend_product import recommend_product


# Create your views here.

def get_recommended_products(request):
    recommend_product_list = recommend_product(get_weather())

    print(recommend_product_list)

    # 반환
    return HttpResponse(content_type="JSON", content=json.dumps({
        "result": True,
        "products": recommend_product_list
    }))
