import requests
import datetime as dt
import json
import pandas as pd
from math import inf

url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
serviceKey = 'c2EtQlIYpThDFFRZclkoOmGaenwXMHJsGNg/sF49Oidra4IQo/s7moFPaGkJmTCzOZOPyfV/ByeQEnIjVIhvBA=='

'''
기온을 계산하는 함수
입력 파라미터 : DataFrame
출력 파라미터 : (평균기온, 최고기온, 최저기온, 기온고저)
'''


def calc_temp(data_frame, weather_dict):
    # 결과값을 저장할 임시 dict
    calc_dict = {'avg_temp': 0, 'max_temp': -inf, 'min_temp': inf, 'dif_temp': 0}

    # 기온 데이터 처리
    temp_df = data_frame[data_frame['category'].isin(['TMP', 'TMX', 'TMN'])]['fcstValue'].apply(pd.to_numeric)
    calc_dict['avg_temp'] = round(temp_df.mean(), 2)
    calc_dict['max_temp'] = round(temp_df.max(), 2)
    calc_dict['min_temp'] = round(temp_df.min(), 2)
    calc_dict['dif_temp'] = round(calc_dict['max_temp'] - calc_dict['min_temp'], 2)

    # 기온 데이터 저장
    for key in calc_dict.keys():
        weather_dict[key] = calc_dict[key]

    return


'''
습도 계산하는 함수
입력 파라미터 : DataFrame
출력 파라미터 : 평균습도
'''


def calc_reh(data_frame, weather_dict):
    REH = data_frame[data_frame['category'] == 'REH']['fcstValue'].apply(pd.to_numeric)
    avg_humidity = REH.mean()

    weather_dict['avg_humidity'] = avg_humidity

    return


'''
강수량 계산하는 함수
입력 파라미터 : DataFrame
출력 파라미터 : 강수량
'''


def calc_pcp(data_frame, weather_dict):
    PCP_df = data_frame[data_frame['category'] == 'PCP']

    condition = PCP_df[PCP_df['fcstValue'].str.contains('강수없음')].index

    PCP_df.drop(condition, inplace=True)

    # mm 제거하기
    PCP_df['fcstValue'].replace('mm', '')
    # str -> int
    PCP = PCP_df['fcstValue'].apply(pd.to_numeric)
    # 전부 더하기
    precipitation = PCP.sum()

    weather_dict['precipitation'] = precipitation

    return


'''
현재 날짜 반환하는 함수
입력 파라미터 : -
출력 파라미터 : 20220101 형식의 date
'''


def get_now():
    # 현재 시각 가져오기
    now = dt.datetime.now()

    # 20220101 형식으로 date 생성
    date = "%d%02d%02d" % (now.year, now.month, now.day-1)

    return date


'''
현재 날씨 반환하는 함수
입력 파라미터 : -
출력 파라미터 : 20220101 형식의 date
'''


def get_weather_request():
    date = get_now()

    # 요청 파라미터
    # TODO nx, ny 수정해야 함
    params = {'serviceKey': serviceKey, 'pageNo': '1', 'numOfRows': '289', 'dataType': 'JSON', 'base_date': date,
              'base_time': '0500', 'nx': '55', 'ny': '127'}

    # 요청하기
    response = requests.get(url, params=params)
    return json.loads(response.text)["response"]["body"]['items']['item']


'''
현재 날씨 데이터 정제하는 함수
입력 파라미터 : -
출력 파라미터 : [평균기온, 최고기온, 기온고저, 평균습도, 강수량]
'''


def weather_refine(data_frame):
    # df 컬럼 설정
    # 평균기온 TMP, TMX, TMN
    # 최고기온
    # 기온고저
    # 평균습도
    # 강수량

    weather_dict = {'avg_temp': 0, 'max_temp': -inf, 'min_temp': inf, 'dif_temp': 0, 'avg_humidity': 0,
                    'precipitation': 0}

    # 기온
    calc_temp(data_frame, weather_dict)
    # 평균습도
    calc_reh(data_frame, weather_dict)
    # 강수량
    calc_pcp(data_frame, weather_dict)

    return list(weather_dict.values())


def get_weather():
    # 날씨 요청 결과값
    result = get_weather_request()

    # 날씨 저장용 DataFrame 생성
    df = pd.DataFrame(result)

    # DataFrame 기반 날씨 정제된 데이터 추출
    weather_data = weather_refine(df)

    return weather_data
