import xml.etree.ElementTree as Xml
import re
import os
from parse_mssql import MSSQL
from parse_mysql import MySQL
from parse_postgresql import PostgreSQL

mssql = MSSQL()
mysql = MySQL()
postgresql = PostgreSQL()

# Finding ALTS_files in current directory and adding this in [listing]
dir_files = os.listdir()
pattern = r"^.*\d{1}\.xml$"
listing = []
for i in dir_files:
    listing = [f for f in dir_files if re.match(pattern, f)]


def check_mssql() -> str | None:
    pattern = r"^.*(?<!\d)11\.xml$"
    path = ""

    for i in listing:
        path = re.match(pattern, i)
        if path is None:
            continue
        else:
            path = path.group()
            break

    if path == "":
        return "Не обнаружено результирующих файлов MSSQL"

    tree = Xml.parse(path)
    root = tree.getroot()

    field = root.find("record/field")
    field = field.get("value").split(" ")
    name = " ".join(field[0:2])

    return name


def check_mysql() -> str | None:
    pattern = r"^.*(?<!\d)7\.xml$"
    path = ""

    for i in listing:
        path = re.match(pattern, i)
        if path is None:
            continue
        else:
            path = path.group()
            break

    if path == "":
        return "Не обнаружено результирующих файлов MySQL"

    tree = Xml.parse(path)
    root = tree.getroot()

    field = root.find("record/field")
    name = field.get("name")
    if name == "VERSION()":
        value = field.get("value")
        checker = value.split("-")[1]
        name = "MySQL" if value[-3:] == "log" else checker
    else:
        return None

    return name


def check_postgresql() -> str | None:
    pattern = r"^.*(?<!\d)8\.xml$"
    path = ""

    for i in listing:
        path = re.match(pattern, i)
        if path is None:
            continue
        else:
            path = path.group()
            break

    if path == "":
        return "Не обнаружено результирующих файлов PostgreSQL"

    tree = Xml.parse(path)
    root = tree.getroot()

    field = root.find("record/field")
    field = field.get("value").split(" ")
    name = " ".join(field[0:2])

    return name


def call_all_funcs():
    result_mysql = check_mysql()
    if result_mysql == "MySQL" or result_mysql == "MariaDB":
        # MySQL parser
        data = mysql.call_all_fucs(listing)
        return data
    else:
        result_mssql = check_mssql()
        if result_mssql[0:9] == "Microsoft":
            # MSSQL parser
            data = mssql.call_all_fucs(listing)
            return data
        else:
            result_postgresql = check_postgresql()
            if result_postgresql[0:10] == "PostgreSQL":
                data = postgresql.call_all_fucs(listing)
                return data
