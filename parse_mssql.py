import xml.etree.ElementTree as Xml

data = {
    "db_info": {
        "DBMS": "DBMS",  # result-11
        "db_upd": "db_upd",  # result-11
        "db_name": "db_name",  # result-7
        "db_owner": "db_owner",  # result-7
        "db_created": "db_created",  # result-7
    },
    "db_size": {
        "db_size_max": "db_size_max",  # result-8
        "db_size_current": "db_size"  # result-7
    },
    "db_tables_sizes": {},
    "db_total_events": "db_total_events"  # result-3
}


# find from result-11: DBMS, db_upd
def find_dmbs_upd() -> None:
    tree = Xml.parse('all_tables_sizes/result-11.xml')
    root = tree.getroot()

    field = root.find("record/field")
    field = field.get("value").split(" ")
    name, updates = " ".join(field[0:3]), " ".join(field[4:6])
    data["db_info"]["DBMS"] = name
    data["db_info"]["db_upd"] = updates

    return None


# find from result-7: name, size current, owner, created
def find_name_owner_created_size() -> None:
    tree = Xml.parse("all_tables_sizes/result-7.xml")
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
def find_maxsize() -> None:
    tree = Xml.parse("all_tables_sizes/result-8.xml")
    root = tree.getroot()
    field = root.findall("record/field")
    for i in field:
        if "maxsize" == i.get("name"):
            data["db_size"]["db_size_max"] = i.get("value")
            break

    return None


# find from result-3: total events
def find_total_events() -> None:
    tree = Xml.parse("all_tables_sizes/result-3.xml")
    root = tree.getroot()
    field = root.find("record/field").get("value")
    data["db_total_events"] = field
    return None


# find from result-2: tables sizes
def find_tables_sizes() -> None:
    tree = Xml.parse("all_tables_sizes/result-2.xml")
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


find_tables_sizes()
print(data)
