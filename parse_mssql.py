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
    "db_total_events": "db_total_events"  # result-3
}


# find: DBMS, db_upd
def find_dmbs_upd() -> None:
    tree = Xml.parse('all_tables_sizes/result-11.xml')
    root = tree.getroot()

    field = root.find("record/field")
    field = field.get("value").split(" ")
    name, updates = " ".join(field[0:3]), " ".join(field[4:6])
    data["db_info"]["db_name"] = name
    data["db_info"]["db_upd"] = updates

    return None


def find_name_owner_created_size() -> None:



find_dmbs_upd()
print(data)
