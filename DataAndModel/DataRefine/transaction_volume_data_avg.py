import pandas as pd
import os


def get_transaction_volume_data_avg():
    read_path = "./transaction_volume_data/refined_files"
    save_path = "./transaction_volume_data/"
    products = os.listdir(read_path)

    names = []
    values = []
    for product in products:
        df = pd.read_csv(f"{read_path}/{product}")
        names.append(product.split(".")[0])
        values.append(df["transaction_volume_data"].mean())

    data = dict()
    data["name"] = names
    data["transaction_volume_data"] = values
    result = pd.DataFrame(data)
    result.to_csv(
        f"{save_path}/transaction_volume_data_avg.csv",
        encoding="utf-8-sig",
        index=False,
    )


if __name__ == "__main__":
    get_transaction_volume_data_avg()
