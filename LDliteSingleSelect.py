import psycopg2 as postgres
import tkinter as tk
from tkinter import scrolledtext as st
import json
import sys


class Querier:
    def __init__(self, config_name):
        print("Initializing Querier...")
        try:
            with open(config_name, "r") as c:
                config = json.load(c)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config File \"{config_name}\" not found")

        dbname = config["dbname"]
        user = config["user"]
        host = config["host"]
        password = config["password"]
        self.query_name = config["query_file"]

        try:
            with open(self.query_name, "r") as q:
                query = ""
                for line in q:
                    query += line
                self.query = query
        except FileNotFoundError:
            raise FileNotFoundError(f"Query File:\n{self.query_name}\nnot found")

        try:
            self.connection = postgres.connect(f"dbname={dbname} user={user} password={password} host={host}")
            self.cursor = self.connection.cursor()
        except Exception as e:
            raise e


    def runQuery(self):
        try:
            self.cursor.execute(self.query)
        except Exception as e:
            raise e
        return 0

    def saveResults(self, outfile_name):
        try:
            with open(outfile_name, 'w') as out:
                for column in self.cursor.description:
                    out.write(column[0]+',')
                out.write('\n')
                for line in self.cursor.fetchall():
                   out.write((str(line)[1:-1]+'\n').replace('\'', ''))
        except Exception as e:
            raise e


# Popup Windows to give alert notices
class PopupWindow:
    def __init__(self, text):
        self.popup = tk.Tk()
        self.popup.wm_title("Popup Notice")
        self.popup.columnconfigure(0, minsize=100)
        self.popup.rowconfigure([0, 1], minsize=25)


        self.text_label = tk.Label(master=self.popup, text=text)
        self.text_label.grid(row=0, column=0)
        self.close_button = tk.Button(master=self.popup, text="OK", command=self.close)
        self.close_button.grid(row=1, column=0)

        self.popup.mainloop()

    def close(self):
        self.popup.destroy()


# Config File Selection Menu
# File Menu includes and option to exit
class ConfigMenu:
    def __init__(self):
        self.config_menu = tk.Tk()
        self.config_menu.wm_title("LDPlite Querier - Config Menu")
        self.config_menu.columnconfigure([0, 1], minsize=100)
        self.config_menu.rowconfigure([0, 1, 2], minsize=10)

        self.config_prompt = tk.Label(master=self.config_menu, text="Please select a config file to use:\n")
        self.config_prompt.grid(row=0, column=0, columnspan=3)

        self.config_input_prompt = tk.Label(master=self.config_menu, text="Input File Name:")
        self.config_input_prompt.grid(row=1, column=0)

        self.config_input_box = tk.Entry(master=self.config_menu, text="configUMass.json")
        self.config_input_box.insert(0, "config.json")
        self.config_input_box.grid(row=1, column=1)

        self.config_input_submit = tk.Button(master=self.config_menu, text="Submit", command=self.launch)
        self.config_input_submit.grid(row=1, column=2, padx=2)

        self.extra_line = tk.Label(master=self.config_menu, text="")
        self.extra_line.grid(row=2, column=1)

        self.config_menu_bar = tk.Menu(master=self.config_menu)
        self.config_file = tk.Menu(master=self.config_menu_bar, tearoff=0)
        self.config_file.add_command(label="Exit", command=sys.exit)
        self.config_menu_bar.add_cascade(label="File", menu=self.config_file)
        self.config_menu.config(menu=self.config_menu_bar)

        self.config_menu.bind("<Return>", self.return_pressed)

        self.config_menu.mainloop()

    def return_pressed(self, event):
        self.launch()

    def launch(self):
        global querier
        global configName
        configName = self.config_input_box.get()
        try:
            querier = Querier(configName)
        except Exception as e:
            print(e)
            PopupWindow(e)
            return
        self.config_menu.destroy()
        ParameterMenu()


# Provides query name
# Includes buttons to open the query display and to run the query
# File Menu includes an option to reselect config and one to exit
class ParameterMenu:
    def __init__(self):
        self.act_menu = tk.Tk()
        self.act_menu.wm_title("LDPlite Querier - Actions Menu")
        self.act_menu.columnconfigure([0, 1, 2], minsize=150)
        self.act_menu.rowconfigure([0, 1, 2, 3, 4, 5], minsize=10)

        # Selected Query Label
        self.query_desc = tk.Label(master=self.act_menu, text="Selected Query: ", font='TkDefaultFont 10 bold')
        self.query_desc.grid(row=0, column=0, columnspan=3)

        # Selected Query Name
        self.query_title = tk.Label(master=self.act_menu, text=querier.query_name, font='TkDefaultFont 10')
        self.query_title.grid(row=1, column=0, columnspan=3)

        # Output File Name Prompt
        self.file_desc = tk.Label(master=self.act_menu, text="Output File Name:", font='TkDefaultFont 10')
        self.file_desc.grid(row=3, column=0, columnspan=1)

        # Output File Name Field
        # Defaults to the name of the query file
        self.file_prompt = tk.Entry(master=self.act_menu, font='TkDefaultFont 10')
        self.file_prompt.insert(0, querier.query_name[:-4]+".csv")
        self.file_prompt.grid(row=3, column=1, columnspan=1)

        # Run Query Button
        self.run = tk.Button(master=self.act_menu, text="Run Query", command=self.run_query, font='TkDefaultFont 10')
        self.run.grid(row=3, column=2, columnspan=1)

        # View Full Query Text Button
        self.view_query = tk.Button(master=self.act_menu, text="View Full Query Text", font='TkDefaultFont 10',
                                    command=self.display_query)
        self.view_query.grid(row=4, column=0, columnspan=3, rowspan=2)

        # Menu Bar
        # File>Exit and File>Reconfigure
        self.main_menu_bar = tk.Menu(master=self.act_menu)
        self.file_menu = tk.Menu(master=self.main_menu_bar, tearoff=0)
        self.file_menu.add_command(label="Reselect Config", command=self.re_config)
        self.file_menu.add_command(label="Exit", command=sys.exit)
        self.main_menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.act_menu.config(menu=self.main_menu_bar)

        self.act_menu.mainloop()

    def re_config(self):
        self.act_menu.destroy()
        ConfigMenu()

    def run_query(self):
        file = self.file_prompt.get()
        try:
            querier.runQuery()
            querier.saveResults(file)
        except Exception as e:
            print(e)
            PopupWindow(e)
            return
        PopupWindow(f"Query Results Saved as:\n{file}")

    def display_query(self):
        self.act_menu.destroy()
        QueryDisplay()


# Displays the full text of the query
# Includes Button to return to the Parameter Menu
# File Menu includes and option to exit
class QueryDisplay:
    def __init__(self):
        self.disp_q = tk.Tk()
        self.disp_q.wm_title("LDPlite Querier - Actions Menu")
        self.disp_q.columnconfigure([0, 1], minsize=150, weight=1)
        self.disp_q.rowconfigure([0, 1, 2], minsize=10, weight=1)

        self.q = tk.Text(master=self.disp_q)
        self.q.insert('end', querier.query)
        self.q.grid(row=0, column=0, sticky='nsew', columnspan=2)
        self.q.config(state='disabled')

        self.qs = st.Scrollbar(master=self.disp_q, orient='vertical')
        self.qs.config(command=self.q.yview)

        self.b = tk.Button(master=self.disp_q, text='Return To Previous Screen', command=self.go_back)
        self.b.grid(row=1, column=0, columnspan=2)

        self.main_menu_bar = tk.Menu(master=self.disp_q)
        self.file_menu = tk.Menu(master=self.main_menu_bar, tearoff=0)
        self.file_menu.add_command(label="Exit", command=sys.exit)
        self.main_menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.disp_q.config(menu=self.main_menu_bar)

    def go_back(self):
        self.disp_q.destroy()
        ParameterMenu()


def config_launch():
    ConfigMenu()


def default_launch():
    global querier
    global configName
    configName = "config.json"
    try:
        querier = Querier(configName)
    except Exception as e:
        print(e)
        PopupWindow(e)
        return
    ParameterMenu()


if __name__ == "__main__":
    default_launch()