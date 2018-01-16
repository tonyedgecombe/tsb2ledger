#!/usr/local/bin/python3

import csv
import re
import sys
from collections import namedtuple
from datetime import datetime
from decimal import Decimal
from itertools import islice

Transaction = namedtuple("Transaction", "date, description, category, debit, credit, balance, row")


def read_categories():
    with open("categories.txt", newline='') as csv_file:
        reader = csv.reader(csv_file, dialect='excel')

        for row in reader:
            yield {
                "expression": row[0],
                "description": row[1],
                "category": row[2]
            }


categories = list(read_categories())


def lookup_category_details(description):
    for entry in categories:
        if re.match(entry["expression"], description):
            return entry["description"], entry["category"]

    raise Exception("Unknown description: {0}".format(description))


def make_decimal(value):
    return Decimal(value if len(value.strip()) else 0)


def to_ledger(transaction):
    result = "; {0}\n".format(transaction.row)
    result += "{0}, {1}\n".format(transaction.date, transaction.description)
    result += "    {0}        £{1:3}\n".format(transaction.category, transaction.debit - transaction.credit)
    result += "    Assets:TSB     £{0:3} = £{1:3}\n".format(transaction.credit - transaction.debit, transaction.balance)

    return result


def read_csv_file(path):
    with open(path, newline='') as csv_file:
        reader = csv.reader(csv_file, dialect='excel')

        for row in reversed(list(islice(reader, 1, None))):
            desc, category = lookup_category_details(row[4])
            yield Transaction(
                date=datetime.strptime(row[0], "%d/%m/%Y").strftime("%Y/%m/%d"),
                description=desc,
                category=category,
                debit=make_decimal(row[5]),
                credit=make_decimal(row[6]),
                balance=make_decimal(row[7]),
                row=', '.join(row)
            )


def main():
    if len(sys.argv) != 2:
        raise Exception('Syntax: tsb2ledger <file.csv>')

    for transaction in read_csv_file(sys.argv[1]):
        print(to_ledger(transaction))


if __name__ == "__main__":
    main()
