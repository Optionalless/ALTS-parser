import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview, TableColumn
from ttkbootstrap.dialogs import Messagebox
from dbms_checker import checker, find_alts_files_in_curpath, find_alts_files_on_path
import threading
import webbrowser
import random


def on_cell_click(event):
    tv = event.widget
    region = tv.identify_region(event.x, event.y)
    if region != "cell":
        return

    row_iid = tv.identify_row(event.y)
    if not row_iid:
        return

    row_values = tv.item(row_iid, "values")

    headers = [col.headertext for col in table_ev_size.tablecolumns]

    try:
        volume_idx = headers.index("Volume (MB)")
    except ValueError:
        return

    cell_value = row_values[volume_idx]

    try:
        age_value = int(float(cell_value))
        db_size = int(data["db_size"]["db_size_current"].split(".")[0])
        percent = int((age_value / db_size) * 100)
        food.configure(amountused=percent)
    except ValueError:
        pass


def gh():
    url = r"https://github.com/Optionalless/ALTS-parser"
    webbrowser.open(url)


def ksc():
    url = r"https://support.kaspersky.com/ksc/"
    webbrowser.open(url)


def btn():
    path = entry.get()
    bar.configure(value=random.randint(20, 80))
    threading.Thread(target=worker, args=(path,), daemon=True).start()


def worker(path):
    try:
        data_local = checker(find_alts_files_on_path(path))
    except FileNotFoundError:
        app.after(0, lambda: (bar.stop(), Messagebox.show_warning(message="The specified catalog was not found", title="Warning", bootstyle="warning")))
        return

    msg_values_local = f"""{data_local["db_info"]["DBMS"]}
{data_local["db_info"]["db_upd"]}
{data_local["db_info"]["db_name"]}
{data_local["db_info"]["db_owner"]}
{data_local["db_info"]["db_created"]}
{data_local["db_size"]["db_size_current"]} MB
{data_local["db_size"]["db_size_max"]}
{data_local["db_total_events"]}"""

    app.after(0, lambda: update_ui(data_local, msg_values_local))


def update_ui(data_local, msg_values_local):
    global data, msg_values
    data = data_local
    msg_values = msg_values_local

    label2.configure(text=msg_values)
    label1.configure(text=msg_keys)

    table_ev_size.delete_rows()
    table_ev_cnt.delete_rows()

    table_ev_size.insert_rows(index='end', rowdata=list(data["db_tables_sizes"].items()))
    table_ev_cnt.insert_rows(index='end', rowdata=list(data["db_events_counts"].items()))

    table_ev_size.sort_column_data(cid=1, sort=1)
    table_ev_cnt.sort_column_data(cid=1, sort=1)

    # останавливаем "крутилку"
    bar.stop()
    bar.configure(value=100)


def reset():
    entry.delete(0, 1000)


# Call and get all data from ALTS files in current path
data = checker(find_alts_files_in_curpath())

# --Text block--
msg_keys = f"""DB Type:
Updates:
DB Name: 
Creator:
Creation date:
Current Volume:
Maximal Volume:
Events count:"""

msg_values = f"""{data["db_info"]["DBMS"]}
{data["db_info"]["db_upd"]}
{data["db_info"]["db_name"]}
{data["db_info"]["db_owner"]}
{data["db_info"]["db_created"]}
{data["db_size"]["db_size_current"]} MB
{data["db_size"]["db_size_max"]}
{data["db_total_events"]}"""

# --Application with paremeters--
app = tb.Window(themename="superhero", iconphoto=r"ALTSlogo.png")
app.title("ALTS parser")
app.geometry("690x305")
app.resizable(False, False)

# --Text block--
root1 = tb.Labelframe(master=app, text="General", style="primary", labelanchor="n", width=278, height=150)
root1.grid(row=0, column=0, padx=5, pady=5, ipadx=2, ipady=3)
root1.grid_propagate(False)
label1 = tb.Label(master=root1, text=msg_keys, font=("Roboto", 10))
label2 = tb.Label(master=root1, text=msg_values, font=("Roboto", 10))
label1.grid(row=0, column=0, padx=5, pady=3)
label2.grid(row=0, column=1)

# ----FRAME----
EntryFrame = tb.Labelframe(app, text="Enter absolute path to catalogue with files", style="primary", width=250, height=300)
EntryFrame.grid(row=1, column=0, sticky="N")
# --Path entry--
entry = tb.Entry(master=EntryFrame, font=("Roboto", 10), name="entry_path", width=27)
entry.grid(row=0, column=0, padx=5, sticky="NW")
# --Button--
button = tb.Button(master=EntryFrame, text="Parse", command=btn, bootstyle="success-outline")
button.grid(row=0, column=1, padx=8, sticky="NE")
button_reset = tb.Button(master=EntryFrame, text="    reset    ", command=reset, padding=(0, 0), bootstyle="success-outline")
button_reset.grid(row=1, column=1)

# --Progressbar--
bar = tb.Progressbar(EntryFrame, orient="horizontal", length=203, value=0)
bar.grid(row=1, column=0, pady=5)
# ----FRAME----

# --Links--
# image_gh = tb.PhotoImage(file=r".\img\github.png").subsample(350, 350)
# image_ksc = tb.PhotoImage(file=r".\img\KSC.png").subsample(45, 45)
root2 = tb.Labelframe(master=app, text="Links", style="info", labelanchor="n")
root2.grid(row=1, column=0, padx=5, pady=70, ipadx=2, ipady=3, rowspan=2, sticky="SW")
tb.Button(master=root2, text="GitHub", style="info", command=gh).grid(row=0, column=0, padx=5)
tb.Button(master=root2, text="Support", style="info", command=ksc).grid(row=0, column=1)

# --Size table--
table_ev_size = Tableview(master=app,
                          coldata=["Table", "Volume (MB)"],
                          rowdata=list(data["db_tables_sizes"].items()),
                          bootstyle="primary",
                          searchable=True,
                          # yscrollbar=True,
                          autofit=False,
                          height=5
                          )
tbl1 = TableColumn(table_ev_size, width=180, cid="0", text="Table", anchor=W, stretch=False)
tbl2 = TableColumn(table_ev_size, width=83, cid="1", text="Volume (MB)", anchor=E, stretch=False)
table_ev_size.grid(row=0, column=1, padx=5, pady=5, sticky="W")

# --Events table--
table_ev_cnt = Tableview(master=app,
                         coldata=["Event", "Count"],
                         rowdata=list(data["db_events_counts"].items()),
                         bootstyle="primary",
                         # yscrollbar=True,
                         autofit=False,
                         height=5
                         )
TableColumn(table_ev_cnt, width=320, cid="0", text="Event", anchor=W)
TableColumn(table_ev_cnt, width=60, cid="1", text="Count", anchor=E)
table_ev_cnt.grid(row=1, column=1, padx=5, sticky="N")

# --Percentage circle--
food = tb.Meter(master=app,
                metertype="full",
                textright="%",
                textleft="Gnrl<",
                textfont="-family 18 -size 18 -weight bold",
                amounttotal=100,
                amountused=0,
                metersize=120,
                interactive=False,
                bootstyle="info")
food.grid(row=0, column=1, sticky="E")


table_ev_size.view.bind("<ButtonRelease-1>", on_cell_click)

app.mainloop()
