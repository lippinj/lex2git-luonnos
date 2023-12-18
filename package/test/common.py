import os


TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(TEST_DIR, "data")


def data_path(filename: str) -> str:
    return DATA_DIR + "/" + filename


def read_data(filename: str) -> str:
    with open(data_path(filename), "r", encoding="utf-8") as f:
        return f.read()
