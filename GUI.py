import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview, TableColumn
from dbms_checker import call_all_funcs

# Вызываем и получаем данные из результирующих файлов
data = call_all_funcs()

# Создаём главное окно с параметрами
app = tb.Window(themename="minty", iconphoto=r".\ALTSlogo.png")
app.title("ALTS parser")
app.geometry("400x720")
app.resizable(False, False)

# Общая информация о БД
tb.Label(app).pack(side="top", anchor="w")
tb.Label(app, text=("СУБД: " + data["db_info"]["DBMS"]), font=("Arial", 10)).pack(side="top", anchor="w")
tb.Label(app, text=("Обновление: " + data["db_info"]["db_upd"]), font=("Arial", 10)).pack(side="top", anchor="w")
tb.Label(app, text=("Наименование: " + data["db_info"]["db_name"]), font=("Arial", 10)).pack(side="top", anchor="w")
tb.Label(app, text=("Владелец/Создатель: " + data["db_info"]["db_owner"]), font=("Arial", 10)).pack(side="top", anchor="w")
tb.Label(app, text=("Дата создания: " + data["db_info"]["db_created"]), font=("Arial", 10)).pack(side="top", anchor="w")
tb.Label(app).pack(side="top", anchor="w")
tb.Label(app, text=("Текущий Объём: " + data["db_size"]["db_size_current"]), font=("Arial", 10)).pack(side="top", anchor="w")
tb.Label(app, text=("Максимальный: " + data["db_size"]["db_size_max"]), font=("Arial", 10)).pack(side="top", anchor="w")
tb.Label(app, text=("Общее количество событий: " + data["db_total_events"]), font=("Roboto", 10)).pack(side="top", anchor="w", pady="20")

table_ev_cnt = Tableview(master=app,
                         coldata=["Наименование", "Количество"],
                         rowdata=list(data["db_events_counts"].items()),
                         searchable=True,
                         yscrollbar=True,
                         autofit=False,
                         )
TableColumn(table_ev_cnt, width=290, cid="0", text="Событие", anchor=W)
TableColumn(table_ev_cnt, width=100, cid="1", text="Количество", anchor=E)
table_ev_cnt.pack(fill="both", expand=False)

if hasattr(table_ev_cnt, "xscrollbar") and table_ev_cnt.xscrollbar:
    table_ev_cnt.xscrollbar.pack_forget()


table_ev_size = Tableview(master=app,
                          coldata=["Наименование", "Объём (МБ)"],
                          rowdata=list(data["db_tables_sizes"].items()),
                          searchable=True,
                          yscrollbar=True,
                          autofit=False
                          )
TableColumn(table_ev_size, width=290, cid="0", text="Таблица в базе", anchor=W)
TableColumn(table_ev_size, width=100, cid="1", text="Объём (МБ)", anchor=E)
table_ev_size.pack(fill="both", expand=False)

app.mainloop()
