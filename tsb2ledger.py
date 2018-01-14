#!/usr/local/bin/python3

import csv
import sys
from datetime import datetime
from decimal import Decimal

from itertools import islice


class Transaction:
    def __init__(self, row):
        self._date = datetime.strptime(row[0], "%d/%m/%Y").date()
        self._type = row[1]
        self._sort_code = row[2]
        self._account = row[3]
        self._description = row[4]
        self._debit = make_decimal(row[5])
        self._credit = make_decimal(row[6])
        self._balance = make_decimal(row[7])
        self._row = ', '.join(row)

    def formatted_date(self):
        return self._date.strftime("%Y/%m/%d")

    def to_ledger(self):
        result = "; " + self._row + "\n"
        result += self.formatted_date() + " " + self._description + "\n"
        result += "    " + "Unknown" + "    " + "£{0:3}".format(self._debit - self._credit) + "\n"
        result += "    " + "Assets:TSB      " + "£{0:3} = £{1:3}".format(self._credit - self._debit, self._balance) + "\n"

        return result


def make_decimal(value):
    return Decimal(value if len(value.strip()) else 0)


def main():
    if len(sys.argv) != 2:
        raise Exception('Syntax: tsb2ledger <file.csv>')

    with open(sys.argv[1], newline='') as csvFile:
        reader = csv.reader(csvFile, dialect='excel')

        for row in reversed(list(islice(reader, 1, None))):
            transaction = Transaction(row)
            print(transaction.to_ledger())


if __name__ == "__main__":
    main()
