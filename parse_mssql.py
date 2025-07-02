import xml.etree.ElementTree as Xml
import re


# find from result-11: DBMS, db_upd
def find_dmbs_upd(data, files_cur_path) -> None:
    pattern = r"^.*(?<!\d)11\.xml$"
    path = ""

    for i in files_cur_path:
        path = re.match(pattern, i)
        if path is None:
            continue
        else:
            path = path.group()
            break

    if path == "":
        return None

    tree = Xml.parse(path)
    root = tree.getroot()

    field = root.find("record/field")
    field = field.get("value").split(" ")
    name, updates = " ".join(field[0:4]), " ".join(field[4:6])
    data["db_info"]["DBMS"] = name
    data["db_info"]["db_upd"] = updates

    return None


# find from result-7: name, size current, owner, created
def find_name_owner_created_size(data, files_cur_path) -> None:
    pattern = r"^.*(?<!\d)7\.xml$"
    path = ""

    for i in files_cur_path:
        path = re.match(pattern, i)
        if path is None:
            continue
        else:
            path = path.group()
            break

    if path == "":
        return None

    tree = Xml.parse(path)
    root = tree.getroot()
    field = root.findall("record/field")

    for i in field:
        name, value = i.get("name"), i.get("value")
        if name == "name":
            data["db_info"]["db_name"] = value
        if name == "db_size":
            data["db_size"]["db_size_current"] = value.strip(" ")
        if name == "owner":
            data["db_info"]["db_owner"] = value
        if name == "created":
            data["db_info"]["db_created"] = value

    return None


# find from result-8: size max
def find_maxsize(data, files_cur_path) -> None:
    pattern = r"^.*(?<!\d)8\.xml$"
    path = ""

    for i in files_cur_path:
        path = re.match(pattern, i)
        if path is None:
            continue
        else:
            path = path.group()
            break

    if path == "":
        return None

    tree = Xml.parse(path)
    root = tree.getroot()
    field = root.findall("record/field")
    for i in field:
        if "maxsize" == i.get("name"):
            data["db_size"]["db_size_max"] = i.get("value")
            break

    return None


# find from result-3: total events
def find_total_events(data, files_cur_path) -> None:
    pattern = r"^.*(?<!\d)3\.xml$"
    path = ""

    for i in files_cur_path:
        path = re.match(pattern, i)
        if path is None:
            continue
        else:
            path = path.group()
            break

    if path == "":
        return None

    tree = Xml.parse(path)
    root = tree.getroot()
    field = root.find("record/field").get("value")
    data["db_total_events"] = field
    return None


# find from result-2: tables sizes
def find_tables_sizes(data, files_cur_path) -> None:
    pattern = r"^.*(?<!\d)2\.xml$"
    path = ""

    for i in files_cur_path:
        path = re.match(pattern, i)
        if path is None:
            continue
        else:
            path = path.group()
            break

    if path == "":
        return None

    tree = Xml.parse(path)
    root = tree.getroot()
    field = root.findall("record/field")
    parse = {}
    name, size = "", ""

    for i in field:
        i, ii = i.get("name"), i.get("value")
        if i == "Name":
            name = ii
        elif i == "reserved":
            size = int(ii.split(" ")[0]) // 1024
            parse[name] = size

    data["db_tables_sizes"] = dict(sorted(parse.items(), key=lambda item: item[1], reverse=True))

    return None


# find from result-4: events counts
def find_tables_events_counts(data, files_cur_path) -> None:
    pattern = r"^.*(?<!\d)4\.xml$"
    path = ""

    for i in files_cur_path:
        path = re.match(pattern, i)
        if path is None:
            continue
        else:
            path = path.group()
            break

    if path == "":
        return None

    tree = Xml.parse(path)
    root = tree.getroot()
    field = root.findall("record/field")
    parse = {}
    event_name, event_count = "", ""

    for i in field:
        i, ii = i.get("name"), i.get("value")
        if i == "":
            event_name = ii
        elif i == "cnt":
            event_count = ii
            parse[event_name] = int(event_count)

    data["db_events_counts"] = dict(sorted(parse.items(), key=lambda item: item[1], reverse=True))

    return None
