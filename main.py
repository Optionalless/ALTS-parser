from dbms_checker import checker, find_alts_files_in_curpath, find_alts_files_on_path
import ctypes


ctypes.windll.kernel32.SetConsoleTitleW("ALTS PARSER")
print("Check the current catalog? [y/n]")
_ = input("Input: ")
if _ == "y" or _ == "Y" or _ == "yes" or _ == "YES" or _ == "Yes":
    data = checker(find_alts_files_in_curpath())
else:
    print("Enter the absolute path to the catalog: ")
    _ = input("Input: ")
    data = checker(find_alts_files_on_path(_))


def out_data(data):
    print("""
                 ┏┓┓ ┏┳┓┏┓ @Optionalles          
                 ┣┫┃  ┃ ┗┓  ┏┓┏┓┏┓┏┏┓┏┓
                 ┛┗┗┛ ┻ ┗┛  ┣┛┗┻┛ ┛┗ ┛ 
                            ┛""")  # by Optionalles

    print(f"""――――――――――――――――――――――――――――――――――――――――――――
│ DBMS: {data["db_info"]["DBMS"]}
│ Updates: {data["db_info"]["db_upd"]}
│ DB Name: {data["db_info"]["db_name"]}
│ Creator: {data["db_info"]["db_owner"]}
│ Creation date: {data["db_info"]["db_created"]}
│――――――――――――――――――――――――――――――――――――――――――――
│ Current Volume: {data["db_size"]["db_size_current"]} MB
│ Maximal Volume: {data["db_size"]["db_size_max"]}
│――――――――――――――――――――――――――――――――――――――――――――
│ Events count: {data["db_total_events"]}
―――――――――――――――――――――――――――――――――――――――――――――\n""")

    cnt = 0
    if data["db_tables_sizes"] != {}:
        print("           TOP-10 Tables (MB)")
        for i, ii in data["db_tables_sizes"].items():
            cnt += 1
            print(f"""―――――――――――――――――――――――――――――――――――――――――――――\n│ {i} │ {ii}""")
            if cnt == 10:
                print("―――――――――――――――――――――――――――――――――――――――――――――\n")
                break

    cnt = 0
    if data["db_events_counts"] != {}:
        print("             TOP-10 Events")
        for i, ii in data["db_events_counts"].items():
            cnt += 1
            print(f"""―――――――――――――――――――――――――――――――――――――――――――――\n│ {i} │ {ii}""")
            if cnt == 10:
                print("―――――――――――――――――――――――――――――――――――――――――――――")  # 45
                break

    input("\nInput any key for exit: ")


if __name__ == "__main__":
    out_data(data)
