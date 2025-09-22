import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview, TableColumn
from ttkbootstrap.dialogs import Messagebox
from checker import checker, find_alts_files_in_curpath, find_alts_files_on_path
import threading
import webbrowser
import random
import os


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
{data_local["db_info"]["host_name"]}
{data_local["db_info"]["db_created"]}
{data_local["db_size"]["db_size_current"]} MB
{data_local["db_size"]["db_size_max"]}
{data_local["db_size"]["unallocated_space"]} MB
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

    bar.stop()
    bar.configure(value=100)


def reset():
    entry.delete(0, 1000)


def create_log_file():
    if data["db_info"]["DBMS"] == "N/D" and data["db_size"]["db_size_max"] == "N/D":
        Messagebox.show_warning(message="Data is not collected", title="Warning", bootstyle="warning")
    else:
        try:
            with open(".\\data.txt", mode="w", encoding="utf-8") as file:
                file.writelines("------------------------------\n")
                for i, ii in data["db_info"].items():
                    file.writelines(str(i) + ": " + str(ii) + "\n")
                file.writelines("------------------------------\n")
                for i, ii in data["db_size"].items():
                    file.writelines(str(i) + ": " + str(ii) + "\n")
                file.writelines("------------------------------\n")
                file.writelines("db_total_events: " + str(data["db_total_events"]))
                file.writelines("\n------------------------------\n")
                for i, ii in data["db_tables_sizes"].items():
                    file.writelines(str(i) + ": " + str(ii) + "\n")
                file.writelines("------------------------------\n")
                for i, ii in data["db_events_counts"].items():
                    file.writelines(str(i) + ": " + str(ii) + "\n")
                file.writelines("------------------------------\n")
        finally:
            Messagebox.show_info(message=f"Success! Data saved! \nPath: {os.getcwd()}\\data.txt", title="Info", bootstyle="warning")


# Call and get all data from ALTS files in current path
data = checker(find_alts_files_in_curpath())

# --Text block--
msg_keys = f""" DB Type:
 Updates:
 DB Name:
 Owner:
 Host:
 Created:
 Volume:
 Limite:
 UnlctSpce:
 Evt cnt:"""

msg_values = f"""{data["db_info"]["DBMS"]}
{data["db_info"]["db_upd"]}
{data["db_info"]["db_name"]}
{data["db_info"]["db_owner"]}
{data["db_info"]["host_name"]}
{data["db_info"]["db_created"]}
{data["db_size"]["db_size_current"]} MB
{data["db_size"]["db_size_max"]}
{data["db_size"]["unallocated_space"]} MB
{data["db_total_events"]}"""

# --Application with paremeters--
app = tb.Window(themename="superhero", iconphoto=r"img\logo.png")
app.title("[ALTS] Parser")
app.geometry("690x317")
app.resizable(False, False)

# --Text block--
root1 = tb.Labelframe(master=app, text="General", style="primary", labelanchor="n", width=278, height=185)
root1.grid(row=0, column=0, padx=5, pady=0, ipadx=2, ipady=0)
root1.grid_propagate(False)
label1 = tb.Label(master=root1, text=msg_keys, font=("Roboto", 10))
label2 = tb.Label(master=root1, text=msg_values, font=("Roboto", 10))
label1.grid(row=0, column=0, padx=5, pady=0)
label2.grid(row=0, column=1)
# --Text createdby--
tb.Label(master=app, text="   CreatedBy\n@Optionalles", font=("Roboto", 8)).grid(column=1, row=0, sticky="NE", padx=30, pady=17)

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
bar.grid(row=1, column=0, pady=5, sticky="N")
# ----FRAME----

# --Options--
root2 = tb.Labelframe(master=app, text="Options", style="info", labelanchor="n")
root2.grid(row=1, column=0, padx=5, pady=70, ipadx=1, ipady=3, rowspan=2, sticky="N")
tb.Button(master=root2, text="GitHub", style="info", command=gh, padding=(0, 0)).grid(row=0, column=0, padx=7)
tb.Button(master=root2, text="Support", style="info", command=ksc, padding=(0, 0)).grid(row=0, column=1)
# --DataOutputButton--
tb.Button(master=root2, text="Save data in current catalogue", style="info", command=create_log_file, padding=(0, 0)).grid(row=0, column=2, padx=7)

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
table_ev_size.grid(row=0, column=1, padx=5, pady=10, ipady=10, sticky="W")

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
table_ev_cnt.grid(row=1, column=1, padx=5, pady=5, sticky="N")

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
food.grid(row=0, column=1, ipady=5, sticky="SE")


table_ev_size.view.bind("<ButtonRelease-1>", on_cell_click)

if __name__ == "__main__":
    app.mainloop()
