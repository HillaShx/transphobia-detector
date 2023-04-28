from typing import Any


class CSVWriter:
    def __init__(self, data_class: Any):
        self.data_class = data_class

    def write(self, body: list, target_filename: str):
        with open(target_filename, "w", newline="") as f:
            f.write(f"{','.join(self.data_class.CSV_HEADER)}\n")
            for post in body:
                f.write(f"{post.to_csv_line()}\n")

