import xml.etree.ElementTree as Xml
import re
import os

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
    value = field.get("value")
    name = "MySQL" if value[-3:] == "log" else "MariaDB"

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
