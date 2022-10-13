from msilib.schema import ComboBox
import psycopg2 as postgres
import tkinter as tk
from tkinter import ttk
import json
import sys
import os
from datetime import datetime

# Object for executing queries
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
        port = config["port"]
        self.query_filepath = config["query_filepath"]
        self.output_filepath = config["output_filepath"]
        self.log_file_output_filepath = config["log_file_output_filepath"]
        self.query_name = ''

        try:
            self.connection = postgres.connect(f"dbname={dbname} user={user} password={password} host={host} port={port}")
            self.cursor = self.connection.cursor()
        except Exception as e:
            raise e
        print("Querier Initialized Successfully.\n")

    def selectQuery(self, queryName):
        print(f"Loading query: \"{queryName}\"...")
        self.query_name = queryName
        try:
            with open(f"{self.query_filepath}/{self.query_name}", "r") as q:
                query = ""
                for line in q:
                    query += line
                self.query = query
        except FileNotFoundError:
            raise FileNotFoundError(f"Query File:\n{self.query_name}\nnot found")
        print(f"Query: \"{queryName}\" Loaded.\n")

    def runQuery(self):
        print("Excecuting Query...")
        try:
            self.cursor.execute(self.query)
        except Exception as e:
            raise e
        print("Query Excecuted Successfully.\n")
        return 0

    def saveResults(self, outfile_name):
        print("Saving Query Results...")
        try:
            with open(f"{self.output_filepath}/{outfile_name}", 'w', encoding="utf-8") as out:
                for column in self.cursor.description:
                    out.write(column[0]+',')
                out.write('\n')
                for line in self.cursor.fetchall(): 
                    newline = ""
                    for item in line:
                        if newline != "":
                            newline += ", "
                        newline += str(item).replace(',',' ')
                    out.write((newline+'\n').replace('\'', ''))
        except Exception as e:
            raise e
        print(f"Query Results Saved Sucessfully as \"{outfile_name}.\"\n")


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

# Allows query selection
# Includes buttons to open the query display and to run the query
# File Menu includes an option to reselect config and one to exit
class ParameterMenu:
    def __init__(self):
        print("Initializing Action Menu...")
        self.act_menu = tk.Tk()
        self.act_menu.wm_title("LDPlite Querier - Actions Menu")
        self.act_menu.columnconfigure([0, 1, 2, 3], minsize=20, pad=10)
        self.act_menu.rowconfigure([0, 1, 2, 3, 4, 5], minsize=10, pad=10)

        # General Title
        self.title = tk.Label(master=self.act_menu, text="Select a query and input a file name.", font='TkDefaultFont 12 bold')
        self.title.grid(row=0, column=0, columnspan=3)
        
        # Selected Query Label
        self.query_desc = tk.Label(master=self.act_menu, text="Query Name: ", font='TkDefaultFont 10')
        self.query_desc.grid(row=1, column=0)

        # Query Select Dropdown
        options = []
        for file in os.listdir("./Queries"):
            if file.endswith('.sql'):
                options.append(file)
        self.config_input_options = ttk.Combobox(self.act_menu, value=options, width=45)
        self.config_input_options.bind("<<ComboboxSelected>>", self.selected)
        self.config_input_options.grid(row=1, column=1, columnspan=2)

        # Output File Name Prompt
        self.file_desc = tk.Label(master=self.act_menu, text="Output File Name:", font='TkDefaultFont 10')
        self.file_desc.grid(row=3, column=0, columnspan=1)

        # Output File Name Field
        # Defaults to the name of the query file
        self.file_prompt = tk.Entry(master=self.act_menu, font='TkDefaultFont 10', width=41)
        self.file_prompt.insert(0, querier.query_name)
        self.file_prompt.grid(row=3, column=1, columnspan=2)

        # Run Query Button
        self.run = tk.Button(master=self.act_menu, text="Run Query", command=self.run_query, font='TkDefaultFont 10')
        self.run.grid(row=4, column=1, columnspan=1)

        # Menu Bar
        # File>Exit and File>Reconfigure
        self.main_menu_bar = tk.Menu(master=self.act_menu)
        self.file_menu = tk.Menu(master=self.main_menu_bar, tearoff=0)
        self.file_menu.add_command(label="Exit", command=sys.exit)
        self.main_menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.act_menu.config(menu=self.main_menu_bar)

        print("Action Menu Initialized.\n")

        self.act_menu.mainloop()
        

    def selected(self, *args):
        print(f"Query: {self.config_input_options.get()} selected.")
        try:
            querier.selectQuery(self.config_input_options.get())
        except Exception as e:
            print(e)
            PopupWindow(e)
        self.file_prompt.delete(0,len(self.file_prompt.get()))
        self.file_prompt.insert(0, querier.query_name[:-4]+'.csv')

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

def generateLog(filepath):
    start = datetime.now()
    logfile = f"{filepath}/{start.year}-{start.month}-{start.day}--{start.hour}-{start.minute}-{start.second}.log"
    print("Saving Log to: " + logfile)
    sys.stdout = open(logfile, "w")
    print("Log Start time: " + str(start) + "\n")
    return start

def launch():
    global querier
    global configName
    configName = "config.json"
    try:
        with open(configName, 'r') as c:
            config = json.load(c)
            log = config["generate_log"]    
            log_location = config["log_file_output_filepath"]
        if log:
            generateLog(log_location)
        else:
            print("Logging Disabled")
    except Exception as e:
        print(e)
        PopupWindow(e)
        return

    try:
        querier = Querier(configName)
    except Exception as e:
        print(e)
        PopupWindow(e)
        return
    
    ParameterMenu()


if __name__ == "__main__":
    launch()