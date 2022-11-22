import pandas as pd
import os


# 거래물량 데이터 정제하는 함수
def data_refine():
    # 컬럼명
    columns = [
        "average_temperature",
        "highest_temperature",
        "lowest_temperature",
        "daily_temperature_range",
        "average_humidity",
        "precipitation",
    ]

    # 경로 설정
    read_path = "./transaction_volume_data/read_files"
    save_path = "./transaction_volume_data/refined_files"
    products = os.listdir(read_path)

    # 데이더 정제
    for product in products:
        path = f"{read_path}/{product}"
        result_dict = dict()
        for column in columns:
            # csv 읽어오기
            df = pd.read_csv(f"{path}/{column}.csv")

            # 컬럼명 변경
            df.columns = (
                ["date"]
                + [column + str(i) for i in range(2013, 2023)]
                + ["transaction_volume_data" + str(i) for i in range(2013, 2023)]
            )
            new_df = pd.concat([df[column + str(i)] for i in range(2013, 2022)], axis=0)
            result_dict[column] = new_df

        # 거래물량 따로 추가
        tons = pd.concat(
            [df[f"transaction_volume_data{i}"] for i in range(2013, 2022)], axis=0
        )
        result_dict["transaction_volume_data"] = tons

        # 결과를 데이터 프레임으로 변환하기
        result = pd.DataFrame(result_dict)

        # NaN값이 있는 행 제거 및 인덱스 초기화
        result = result.dropna()
        result = result.reset_index(drop=True)

        # 추출
        result.to_csv(
            f"{save_path}/{product.split()[0]}.csv", encoding="utf-8-sig", index=False
        )


if __name__ == "__main__":
    data_refine()
