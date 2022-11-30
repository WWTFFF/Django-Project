import json
import requests

from django.http import HttpResponse

from product.src.get_weather import get_weather
from product.src.recommend_product import recommend_product


# Create your views here.

def get_recommended_products(request):
    result = []
    recommend_product_list = recommend_product(get_weather())

    # recommend_product_list = ["딸기", "수박"]

    # 키워드로 검색
    # 경로 설정
    request_url = "https://st6b5nlr52.execute-api.ap-northeast-2.amazonaws.com"
    path = "product/list/search"

    for product in recommend_product_list:
        request_path = f"{request_url}/{path}/{product}"

        # 요청
        response = requests.get(request_path)

        # 결과 반환
        result.extend(response.json()["result"])

    print(result)

    # 반환
    return HttpResponse(content_type="JSON", content=json.dumps({
        "result": True,
        "products": result
    }))
