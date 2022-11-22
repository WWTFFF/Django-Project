import pandas as pd
import os
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

columns = [
    "average_temperature",
    "highest_temperature",
    "lowest_temperature",
    "daily_temperature_range",
    "average_humidity",
    "precipitation",
]


class PrintDot(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs):
        if epoch % 100 == 0:
            print("")
        print(".", end="")


def norm(x, train_stats):
    return (x - train_stats["mean"]) / train_stats["std"]


def build_model():
    model = tf.keras.Sequential(
        [
            layers.Dense(64, activation="relu", input_shape=[len(columns)]),
            layers.Dense(64, activation="relu"),
            layers.Dense(1),
        ]
    )

    optimizer = tf.keras.optimizers.RMSprop(0.001)

    model.compile(loss="mse", optimizer=optimizer, metrics=["mae", "mse"])
    return model


def create_save_model():
    # 컬럼명
    read_path = "../DataRefine/transaction_volume_data/refined_files"
    products = os.listdir(read_path)

    # CSV 불러오기
    for product in products:
        df = pd.read_csv(f"{read_path}/{products[0]}")

        # 데이터 input/output 분리
        df_x_data = df.drop(["transaction_volume_data"], axis=1)
        df_y_data = df["transaction_volume_data"]

        # 훈련/테스트 데이터 분리
        df_x_train, df_x_test, df_y_train, df_y_test = train_test_split(
            df_x_data, df_y_data, test_size=0.3, random_state=20221004
        )

        # 데이터 통계량 요약
        train_stats = df_x_train.describe()

        # 데이터 행/열 전환
        train_stats = train_stats.transpose()

        # 데이터 정규화
        normed_train_data = norm(df_x_train, train_stats)
        normed_test_data = norm(df_x_test, train_stats)

        # 모델 생성
        model = build_model()

        # 모델 학습
        EPOCHS = 3500
        history = model.fit(
            normed_train_data,
            df_y_train,
            epochs=EPOCHS,
            validation_split=0.2,
            verbose=0,
            callbacks=[PrintDot()],
        )

        # 모델 저장
        model.save(f'./saved_model/{product.split(".")[0]}')


if __name__ == "__main__":
    create_save_model()
