#!/usr/local/bin/python3

import csv
import sys
from datetime import datetime
from decimal import Decimal


class Transaction:
    def __init__(self, row):
        self.date = datetime.strptime(row[0], "%d/%m/%Y").date()
        self.type = row[1]
        self.sort_code = row[2]
        self.account = row[3]
        self.description = row[4]
        self.debit = make_decimal(row[5])
        self.credit = make_decimal(row[6])
        self.amount = make_decimal(row[7])
        self.row = ', '.join(row)

    def formatted_date(self):
        return self.date.strftime("%Y/%m/%d")

    def to_ledger(self):
        result = "; " + self.row + "\n"
        result += self.formatted_date() + " " + self.description + "\n"
        result += "    " + "Unknown" + "    " + "£{0:3}".format(self.debit - self.credit) + "\n"
        result += "    " + "Assets:TSB" + "\n"

        return result


def make_decimal(value):
    return Decimal(value if len(value.strip()) else 0)


def main():
    if len(sys.argv) != 2:
        raise Exception('Syntax: tsb2ledger <file.csv>')

    with open(sys.argv[1], newline='') as csvFile:
        reader = csv.reader(csvFile, dialect='excel')

        next(reader)  # Skip past title

        for row in reader:
            transaction = Transaction(row)
            print(transaction.to_ledger())


if __name__ == "__main__":
    main()
