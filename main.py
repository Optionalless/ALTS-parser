from dbms_checker import call_all_funcs
import ctypes

ctypes.windll.kernel32.SetConsoleTitleW("ALTS PARSER")
data = call_all_funcs()


def out_data(data):
    print("""
                 ┏┓┓ ┏┳┓┏┓ @Optionalles          
                 ┣┫┃  ┃ ┗┓  ┏┓┏┓┏┓┏┏┓┏┓
                 ┛┗┗┛ ┻ ┗┛  ┣┛┗┻┛ ┛┗ ┛ 
                            ┛""")  # by Optionalles

    print(f"""――――――――――――――――――――――――――――――――――――――――――――
    │ СУБД: {data["db_info"]["DBMS"]}
    │ Обновления/версия: {data["db_info"]["db_upd"]}
    │ Наименование: {data["db_info"]["db_name"]}
    │ Владелец: {data["db_info"]["db_owner"]}
    │ Создано: {data["db_info"]["db_created"]}
    │――――――――――――――――――――――――――――――――――――――――――――
    │ Текущий Объём: {data["db_size"]["db_size_current"]}
    │ Максимальнный: {data["db_size"]["db_size_max"]}
    │――――――――――――――――――――――――――――――――――――――――――――
    │ Общее количество событий: {data["db_total_events"]}
    ―――――――――――――――――――――――――――――――――――――――――――――\n""")

    cnt = 0
    if data["db_tables_sizes"] != {}:
        print("           Топ-10 таблиц (MB)")
        for i, ii in data["db_tables_sizes"].items():
            cnt += 1
            print(f"""―――――――――――――――――――――――――――――――――――――――――――――\n│ {i} │ {ii}""")
            if cnt == 10:
                print("―――――――――――――――――――――――――――――――――――――――――――――\n")
                break

    cnt = 0
    if data["db_events_counts"] != {}:
        print("             Топ-10 событий")
        for i, ii in data["db_events_counts"].items():
            cnt += 1
            print(f"""―――――――――――――――――――――――――――――――――――――――――――――\n│ {i} │ {ii}""")
            if cnt == 10:
                print("―――――――――――――――――――――――――――――――――――――――――――――")  # 45
                break

    input("\nInput any key for exit: ")


if __name__ == "__main__":
    out_data(data)
