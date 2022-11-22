from django.conf import settings
import pandas as pd
import numpy as np


def recommend_product(weather_list):
    result = []

    # TODO 1. 학습된 모델 호출
    print(settings.PRODUCT_MODEL_DICT)

    # TODO 2. 추천 가능한 물품 목록(전체) 추출
    print(settings.PRODUCT_LIST)

    # TODO 4. 학습된 모델로 오늘 날씨에 대한 추천 목록 추출
    df = pd.read_csv(f"DataAndModel/DataRefine/transaction_volume_data/transaction_volume_data_avg.csv")
    for index, product in enumerate(settings.PRODUCT_LIST):
        model = settings.PRODUCT_MODEL_DICT[product]
        # print(model.summary())
        avg_value = df.iloc[index]['transaction_volume_data']
        print('평균 판매량', avg_value)
        predict_value = model.predict([weather_list])[0]
        print(weather_list)
        print('예측 판매량', predict_value)

        if avg_value<= predict_value:
            result.append(product)

    return result
