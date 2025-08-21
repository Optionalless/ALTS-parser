import xml.etree.ElementTree as Xml
import re


class MSSQL:

    directory = ""

    data = {
        "db_info": {
            "DBMS": "DBMS",  # result-11
            "db_upd": "Undefined",  # result-11
            "db_name": "db_name",  # result-7
            "db_owner": "Undefined",  # result-7
            "db_created": "Undefined",  # result-7
        },
        "db_size": {
            "db_size_max": "db_size_max",  # result-8
            "db_size_current": "db_size"  # result-7
        },
        "db_tables_sizes": {},
        "db_events_counts": {},
        "db_total_events": "db_total_events"  # result-3
    }

    # search .xml-files in current path
    def matcher(self, pattern, files_cur_path) -> str:
        directory = str(self.directory + "\\") if self.directory[-1] != "\\" else self.directory
        for i in files_cur_path:
            match = re.match(pattern, i)
            if match is None:
                continue
            else:
                match = match.group()
                result = directory + match
                return result

    # find from result-11: DBMS, db_upd
    def find_dmbs_upd(self, files_cur_path) -> None:
        pattern = r"^.*(?<!\d)11\.xml$"

        path = self.matcher(pattern, files_cur_path)

        if path == "":
            return None

        tree = Xml.parse(path)
        root = tree.getroot()
        field = root.find("record/field")
        field = field.get("value").split(" ")
        name, updates = " ".join(field[0:4]), " ".join(field[4:6])
        self.data["db_info"]["DBMS"] = name
        self.data["db_info"]["db_upd"] = updates

        return None

    # find from result-7: name, size current, owner, created
    def find_name_owner_created_size(self, files_cur_path) -> None:
        pattern = r"^.*(?<!\d)7\.xml$"

        path = self.matcher(pattern, files_cur_path)

        if path == "":
            return None

        tree = Xml.parse(path)
        root = tree.getroot()
        field = root.findall("record/field")

        for i in field:
            name, value = i.get("name"), i.get("value")
            if name == "name":
                self.data["db_info"]["db_name"] = value
            if name == "db_size":
                self.data["db_size"]["db_size_current"] = value.lstrip().split(" ")[0]
            if name == "owner":
                self.data["db_info"]["db_owner"] = value
            if name == "created":
                self.data["db_info"]["db_created"] = value

        return None

    # find from result-8: size max
    def find_maxsize(self, files_cur_path) -> None:
        pattern = r"^.*(?<!\d)8\.xml$"

        path = self.matcher(pattern, files_cur_path)

        if path == "":
            return None

        tree = Xml.parse(path)
        root = tree.getroot()
        field = root.findall("record/field")
        for i in field:
            if "maxsize" == i.get("name"):
                self.data["db_size"]["db_size_max"] = i.get("value")
                break

        return None

    # find from result-3: total events
    def find_total_events(self, files_cur_path) -> None:
        pattern = r"^.*(?<!\d)3\.xml$"

        path = self.matcher(pattern, files_cur_path)

        if path == "":
            return None

        tree = Xml.parse(path)
        root = tree.getroot()
        field = root.find("record/field").get("value")
        self.data["db_total_events"] = field

        return None

    # find from result-2: tables sizes
    def find_tables_sizes(self, files_cur_path) -> None:
        pattern = r"^.*(?<!\d)2\.xml$"

        path = self.matcher(pattern, files_cur_path)

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
                size = int(ii.split(" ")[0]) // 1024  # Transform KB to MB
                parse[name] = size

        self.data["db_tables_sizes"] = dict(sorted(parse.items(), key=lambda item: item[1], reverse=True))

        return None

    # find from result-4: events counts
    def find_tables_events_counts(self, files_cur_path) -> None:
        pattern = r"^.*(?<!\d)4\.xml$"

        path = self.matcher(pattern, files_cur_path)

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

        self.data["db_events_counts"] = dict(sorted(parse.items(), key=lambda item: item[1], reverse=True))

        return None

    # call all funcs and return data
    def call_all_fucs(self, listing) -> dict:
        self.find_name_owner_created_size(listing)
        self.find_dmbs_upd(listing)
        self.find_maxsize(listing)
        self.find_total_events(listing)
        self.find_tables_sizes(listing)
        self.find_tables_events_counts(listing)

        return self.data
