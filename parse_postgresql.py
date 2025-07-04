import xml.etree.ElementTree as Xml
import re


class PostgreSQL:

    data = {
        "db_info": {
            "DBMS": "DBMS",
            "db_upd": "Undefined",
            "db_name": "db_name",
            "db_owner": "Undefined",
            "db_created": "Undefined",
        },
        "db_size": {
            "db_size_max": "db_size_max",
            "db_size_current": "db_size"
        },
        "db_tables_sizes": {},
        "db_events_counts": {},
        "db_total_events": "db_total_events"
    }

    # search .xml-files in current path
    @staticmethod
    def find_files_in_cur_path(pattern, files_cur_path) -> str:
        for i in files_cur_path:
            path = re.match(pattern, i)
            if path is None:
                continue
            else:
                path = path.group()
                return path

    # find from result-8: DBMS, version
    def find_dmbs_upd(self, files_cur_path) -> None:
        pattern = r"^.*(?<!\d)8\.xml$"

        path = self.find_files_in_cur_path(pattern, files_cur_path)

        if path == "":
            return None

        tree = Xml.parse(path)
        root = tree.getroot()

        field = root.find("record/field")
        field = field.get("value").split(" ")
        name = " ".join(field[0:2][:1])
        self.data["db_info"]["DBMS"] = name

        return None

    # find from result-6: name size
    def find_name_size(self, files_cur_path) -> None:
        pattern = r"^.*(?<!\d)6\.xml$"

        path = self.find_files_in_cur_path(pattern, files_cur_path)

        if path == "":
            return None

        tree = Xml.parse(path)
        root = tree.getroot()
        field = root.findall("record/field")

        for i in field:
            name, value = i.get("name"), i.get("value")

            if name == "database_name":
                self.data["db_info"]["db_name"] = value
            elif name == "database_size":
                self.data["db_size"]["db_size_current"] = value.split(".")[0]

        self.data["db_size"]["db_size_max"] = "Unlimited"

        return None

    # find from result-8: size max
    def find_maxsize(self, files_cur_path) -> None:
        pattern = r"^.*(?<!\d)8\.xml$"

        path = self.find_files_in_cur_path(pattern, files_cur_path)

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

    # find from result-2: total events
    def find_total_events(self, files_cur_path) -> None:
        pattern = r"^.*(?<!\d)2\.xml$"

        path = self.find_files_in_cur_path(pattern, files_cur_path)

        if path == "":
            return None

        tree = Xml.parse(path)
        root = tree.getroot()
        field = root.find("record/field").get("value")
        self.data["db_total_events"] = field
        return None

    # find from result-1: tables sizes
    def find_tables_sizes(self, files_cur_path) -> None:
        pattern = r"^.*(?<!\d)1\.xml$"

        path = self.find_files_in_cur_path(pattern, files_cur_path)

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

        self.data["db_tables_sizes"] = dict(sorted(parse.items(), key=lambda item: item[1], reverse=True))

        return None

    # find from result-3: events counts
    def find_tables_events_counts(self, files_cur_path) -> None:
        pattern = r"^.*(?<!\d)3\.xml$"

        path = self.find_files_in_cur_path(pattern, files_cur_path)

        if path == "":
            return None

        tree = Xml.parse(path)
        root = tree.getroot()
        field = root.findall("record/field")
        parse = {}
        event_name, event_count = "", ""

        for i in field:
            i, ii = i.get("name"), i.get("value")
            if i == "max":
                event_name = ii
            elif i == "cnt":
                event_count = ii
                parse[event_name] = int(event_count)

        self.data["db_events_counts"] = dict(sorted(parse.items(), key=lambda item: item[1], reverse=True))

    # call all funcs and return data
    def call_all_fucs(self, listing) -> dict:
        self.find_name_size(listing)
        self.find_dmbs_upd(listing)
        self.find_maxsize(listing)
        self.find_total_events(listing)
        self.find_tables_sizes(listing)
        self.find_tables_events_counts(listing)
        return self.data
