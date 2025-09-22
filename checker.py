import xml.etree.ElementTree as Xml
import re
import os
from classes import MSSQL
from classes import MySQL
from classes import PostgreSQL


mssql = MSSQL()
mysql = MySQL()
postgres = PostgreSQL()
directory = ".\\"


# Finding ALTS_files in current directory and adding this in [listing]
def find_alts_files_in_curpath():
    # check curpath
    dir_files = os.listdir()
    MSSQL.directory = str(os.getcwd() + "\\")
    MySQL.directory = str(os.getcwd() + "\\")
    PostgreSQL.directory = str(os.getcwd() + "\\")
    pattern = r"^.*\d{1}\.xml$"
    list_of_alts_files = []
    for _ in dir_files:
        list_of_alts_files = [f for f in dir_files if re.match(pattern, f)]
    if len(list_of_alts_files) > 0:
        return list_of_alts_files
    else:
        return None


def find_alts_files_on_path(path):
    dir_files = os.listdir(path=path)
    global directory
    directory = str(path + "\\")
    MSSQL.directory = directory
    MySQL.directory = directory
    PostgreSQL.directory = directory
    pattern = r"^.*\d{1}\.xml$"
    list_of_alts_files = []
    for _ in dir_files:
        list_of_alts_files = [f for f in dir_files if re.match(pattern, f)]
    if len(list_of_alts_files) > 0:
        return list_of_alts_files


def check_mssql(alts_files) -> str | None:
    pattern = r"^.*(?<!\d)11\.xml$"
    result = ""

    for i in alts_files:
        match = re.match(pattern, i)

        if match is None:
            continue
        else:
            result = match.group()
            break

    if result == "":
        return "Не обнаружено результирующих файлов MSSQL"

    tree = Xml.parse(directory + result)
    root = tree.getroot()

    field = root.find("record/field")
    field = field.get("value").split(" ")
    name = " ".join(field[0:2])

    return name


def check_mysql(alts_files) -> str | None:

    pattern = r"^.*(?<!\d)7\.xml$"
    result = ""

    for i in alts_files:
        match = re.match(pattern, i)
        if match is None:
            continue
        else:
            result = match.group()
            break

    if result == "":
        return "Не обнаружено результирующих файлов MySQL"
    tree = Xml.parse(directory + result)
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


def check_postgresql(alts_files) -> str | None:
    pattern = r"^.*(?<!\d)8\.xml$"
    result = ""

    for i in alts_files:
        match = re.match(pattern, i)
        if match is None:
            continue
        else:
            result = match.group()
            break

    if result == "":
        return "Не обнаружено результирующих файлов PostgreSQL"

    tree = Xml.parse(directory + result)
    root = tree.getroot()

    field = root.find("record/field")
    field = field.get("value").split(" ")
    name = " ".join(field[0:2])

    return name


def checker(list_of_alts_files):
    if list_of_alts_files is not None:
        result_mysql = check_mysql(list_of_alts_files)
        if result_mysql == "MySQL" or result_mysql == "MariaDB":
            # MySQL parser
            data = mysql.call_all_fucs(list_of_alts_files)
            return data
        else:
            result_mssql = check_mssql(list_of_alts_files)
            if result_mssql[0:9] == "Microsoft":
                # MSSQL parser
                data = mssql.call_all_fucs(list_of_alts_files)
                return data
            else:
                result_postgresql = check_postgresql(list_of_alts_files)
                if result_postgresql[0:10] == "PostgreSQL":
                    data = postgres.call_all_fucs(list_of_alts_files)
                    return data
    else:
        data = MSSQL.data
        return data


if "__main__" == __name__:
    checker(find_alts_files_in_curpath())
