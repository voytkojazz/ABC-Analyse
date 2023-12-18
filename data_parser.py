import csv
from typing import NamedTuple

class Product(NamedTuple):
    name: str
    amount: int
    unitprice: float

def parse_csv(file_path: str) -> list[Product]:
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header
        return [Product(name, int(amount), float(unitprice)) for name, amount, unitprice in reader]
