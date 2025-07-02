import parse_mssql
import parse_mysql
import parse_postgresql
import dmbs_checker


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
    "db_events_counts": {},
    "db_total_events": "db_total_events"  # result-3
}


result_mysql = dmbs_checker.check_mysql()
if result_mysql == "MySQL" or result_mysql == "MariaDB":
    # MySQL parser
    parse_mysql.find_name_size(data, dmbs_checker.listing)
    parse_mysql.find_total_events(data, dmbs_checker.listing)
    parse_mysql.find_dmbs_upd(data, dmbs_checker.listing)
    parse_mysql.find_tables_events_counts(data, dmbs_checker.listing)
    parse_mysql.find_tables_sizes(data)
else:
    result_mssql = dmbs_checker.check_mssql()
    if result_mssql[0:9] == "Microsoft":
        # MSSQL parser
        parse_mssql.find_name_owner_created_size(data, dmbs_checker.listing)
        parse_mssql.find_dmbs_upd(data, dmbs_checker.listing)
        parse_mssql.find_total_events(data, dmbs_checker.listing)
        parse_mssql.find_maxsize(data, dmbs_checker.listing)
        parse_mssql.find_tables_events_counts(data, dmbs_checker.listing)
        parse_mssql.find_tables_sizes(data, dmbs_checker.listing)
    else:
        result_postgresql = dmbs_checker.check_postgresql()
        if result_postgresql[0:10] == "PostgreSQL":
            # PostgreSQL parser
            parse_postgresql.find_tables_sizes(data, dmbs_checker.listing)
            parse_postgresql.find_maxsize(data, dmbs_checker.listing)
            parse_postgresql.find_tables_events_counts(data, dmbs_checker.listing)
            parse_postgresql.find_dmbs_upd(data, dmbs_checker.listing)
            parse_postgresql.find_total_events(data, dmbs_checker.listing)
            parse_postgresql.find_name_size(data, dmbs_checker.listing)

print(data)
