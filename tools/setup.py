# Tables
from tabulate import tabulate

# Dataclasses
from data.dataclasses import *
from operator import attrgetter

# Misc Tools
from tools.tools import MiscTools
from tools.tools import LoggingTools
from sys import _getframe

# Database Stuff
from tools.tools import DatabaseTools

# Database Setup
import json

class Setup():
    def __init__(self):
        self.self = self

    def main(self):
        MiscTools.cls()
        print("Generator work in progress")

        temp = input("""
    Wybierz element danych, który chcesz skonfigurować:

    1 - Bazy danych
    2 - Przykładowe dane
    3 - Obie powyższe opcje
    E(xit) - Wyjście z konfiguratora

    Wybór: """)

        if temp == "1":
            Setup.database_setup(self)
        elif temp == "2":
            Setup.data_setup(self)
        elif temp == "3":
            Setup.database_setup(self)
            Setup.data_setup(self)
        elif temp.lower() in ["e", "exit", "q", "quit"]:
            #TODO DatabaseTools.databaseClose(self)
            exit()
            # Restart.rerun() #TODO ImportError: cannot import name 'Generator' from partially initialized module 'tools.Generator' (most likely due to a circular import)

    def database_setup(self):
        with open("data/SetupData.json", "r") as file:
            data = json.load(file)
            sql_commands = data["sql_commands"]

        for cmd in sql_commands:
            print(f"Tworzenie tabelki {cmd}")
            DatabaseTools.databaseModify(self, sql_commands[cmd], Setup)

    def data_setup(self):
        with open("data/SetupData.json", "r", encoding="UTF-8") as file:
            data = json.load(file)
        
        data = data["placeholder_data"]


        text = ""
        for datatype in data:
            print(f"Tworzenie danych {datatype}")
            for item in data[datatype]:
                columns = ""
                values = ""
                for key in item:
                    if columns == "":
                        columns = f"`{key}`"
                    else:
                        columns = columns + ", `" + key + "`"
                    if values == "":
                        values = f"'{item[key]}'"
                    else:
                        values = values + ", '" + item[key] + "'"
                
                sql = f"INSERT INTO `{datatype}` ({columns}) VALUES ({values})"
                query = DatabaseTools.databaseModify(self, sql, Setup)
                if query == 0:
                    LoggingTools.log(self, f"Błąd przy dodawaniu danych w tabeli {datatype}. Item: \n{item} \nSQL: {sql}", "error", _getframe().f_code.co_name)