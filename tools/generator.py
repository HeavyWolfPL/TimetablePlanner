# Tables
from tabulate import tabulate

# Dataclasses
from data.dataclasses import *

# Misc Tools
from tools.tools import MiscTools
from tools.tools import LoggingTools
from sys import _getframe

# Database Stuff
from tools.tools import DatabaseTools
import mysql.connector
from mysql.connector import errorcode

class Generator():
    def __init__(self):
        self.self = self

    def main(self):
        MiscTools.cls()
        print("Generator work in progress")

        temp = input("""
    Wybierz element danych, który chcesz wygenerować:

    1 - Przydzielenie nauczycieli do klas
    2 - Wygenerowanie planu lekcji dla klas(y)
    3 - Obie powyższe opcje
    E(xit) - Wyjście z Przeglądu danych.

    Wybór: """)

        database = DatabaseTools.databaseGet(self)

        if temp == "1":
            Generator.assign_teachers(self)
        elif temp == "2":
            temp = input("Podaj przedmiot, którego nauczycieli chcesz wyświetlić (lub pozostaw puste, aby wyświetlić wszystkich nauczycieli): ")
            Generator.generate_timetable(self, temp)
        elif temp == "3":
            Generator.show_subjects()
        elif temp.lower() in ["e", "exit", "q", "quit"]:
            DatabaseTools.databaseClose(self)
            exit()
            # Restart.rerun() #TODO: ImportError: cannot import name 'Generator' from partially initialized module 'tools.Generator' (most likely due to a circular import)

    def assign_teachers(self):
        query = DatabaseTools.databaseQuery(self, f"SELECT klasa FROM klasy", Generator)

        if not query:
            print("Nie znaleziono klas w bazie danych.")
            input("Naciśnij Enter, aby wrócić do menu głównego.")
            LoggingTools.log(self, f"Nie znaleziono żadnej klasy w bazie danych.", "info")
            Generator.main(self)

        query = sorted(query)

        for classs in query:
            print(classs)
        print(query)

        query = DatabaseTools.databaseQuery(self, f"SELECT * FROM przedmioty", Generator)

        przedmioty = []
        for przedmiot in query:
            przedmioty.append(Subject(
                name = przedmiot[0],
                first_class_hr = int(przedmiot[1]),
                second_class_hr = int(przedmiot[2]),
                third_class_hr = int(przedmiot[3]),
            ))

        print(przedmioty)

        query = DatabaseTools.databaseQuery(self, f"SELECT * FROM nauczyciele", Generator)

        nauczyciele = []
        for nauczyciel in query:
            nauczyciele.append(Teacher(
                short_name = nauczyciel[0],
                name = nauczyciel[1],
                subjects = nauczyciel[2],
            ))


        

        # INSERT INTO `przydzieleni_nauczyciele` (`Przedmiot`, `Nauczyciel`, `Klasy`) VALUES ('Edukacja wczesnoszkolna', 'Paulina Cukierman', '1A');