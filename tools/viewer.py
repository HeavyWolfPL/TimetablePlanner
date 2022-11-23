# Tables
from tabulate import tabulate

# Misc Tools
from tools.tools import MiscTools
from tools.tools import LoggingTools
from sys import _getframe

# Database Stuff
from tools.tools import DatabaseTools
import mysql.connector
from mysql.connector import errorcode

class Viewer():
    def __init__(self):
        self.self = self

    def main(self):
        MiscTools.cls()

        temp = input("""
    Które dane chcesz wyświetlić?

    1 - Klasy
    2 - Nauczyciele
    3 - Przedmioty
    4 - Sale
    E - Wyjście z Przeglądu danych.
        
    Wybór: """)

        if temp == "1":
            temp = input("Podaj klasę lub wychowawcę klasy, którą chcesz wyświetlić (lub pozostaw puste, aby wyświetlić wszystkie klasy): ")
            Viewer.show_classes(self, temp)
        elif temp == "2":
            temp = input("Podaj przedmiot, którego nauczycieli chcesz wyświetlić (lub pozostaw puste, aby wyświetlić wszystkich nauczycieli): ")
            Viewer.show_teachers(self, temp)
        elif temp == "3":
            Viewer.show_subjects()
        elif temp == "4":
            #TODO
            #Viewer.show_rooms()
            return
        elif temp == "5":
            #TODO
            #Viewer.show_timetable()
            return
        elif temp.lower() in ["e", "exit", "q", "quit"]:
            exit()
            # Restart.rerun() #TODO ImportError: cannot import name 'Viewer' from partially initialized module 'tools.viewer' (most likely due to a circular import)

    def show_classes(self, filtr = None):
        rows = []
        headers = ["Klasa", "Nauczyciel", "Sala", "Uczniowie"]

        if filtr.lstrip().rstrip():
            query = DatabaseTools.databaseQuery(self, f"SELECT * FROM klasy WHERE {filtr} IN (klasa, wychowawca)", Viewer)
        else:
            query = DatabaseTools.databaseQuery(self, "SELECT * FROM klasy", Viewer)

        if not query:
            print("Nie znaleziono klasy zgodnej z podanym filtrem.")
            input("Naciśnij Enter, aby wrócić do menu głównego.")
            LoggingTools.log(self, f"Nie znaleziono klasy zgodnej z podanym filtrem: '{filtr}'", "debug")
            Viewer.main(self)

        for school_class in query:
            class_name = school_class[0]
            teacher = school_class[2]
            room = school_class[3]
            students = school_class[1]
            rows.append([class_name, teacher, room, students])

        table = tabulate(rows, headers, tablefmt="orgtbl", stralign="center")

        print(table)
        LoggingTools.log(self, f"Wyświetlono listę klas zgodnych z filtrowaniem: '{filtr}'")

        input("Naciśnij Enter, aby wrócić do menu głównego.")
        Viewer.main(self)

    
    def show_teachers(self, filtr = None): 
        rows = []
        headers = ["Imię i Nazwisko", "Przedmiot", "Wychowawstwo", "Godziny"]

        if filtr.lstrip().rstrip():
            query = DatabaseTools.databaseQuery(self, f"SELECT * FROM nauczyciele WHERE '{filtr}' in (IMIENAZWISKO, SKROT, PRZEDMIOT)", Viewer)
        else:
            query = DatabaseTools.databaseQuery(self, "SELECT * FROM nauczyciele", Viewer)

        if not query:
            print("Nie znaleziono klasy zgodnej z podanym filtrem.")
            input("Naciśnij Enter, aby wrócić do menu głównego.")
            LoggingTools.log(self, f"Nie znaleziono klasy zgodnej z podanym filtrem: '{filtr}'", "debug")
            Viewer.main(self)

        for teacher in query:
            teacher_name = f"{teacher[1]} ({teacher[0]})"
            teacher_subject = teacher[2]
            teacher_headteaching = teacher[3]
            teacher_hours = teacher[4]
            rows.append([teacher_name, teacher_subject, teacher_headteaching, teacher_hours])

        table = tabulate(rows, headers, tablefmt="orgtbl", stralign="center")

        print(table)
        LoggingTools.log(self, f"Wyświetlono listę nauczycieli zgodnych z filtrowaniem: '{filtr}'")

        input("Naciśnij Enter, aby wrócić do menu głównego.")
        Viewer.main(self)

    def show_subjects(self, filtr = None):
        rows = []
        headers = ["Przedmiot", "Typ sali", "Przedmiot wychowawcy", "I Klasa / Godziny", "II Klasa / Godziny", "III Klasa / Godziny"]

        if filtr.lstrip().rstrip():
            query = DatabaseTools.databaseQuery(self, f"SELECT * FROM przedmioty WHERE {filtr} in (Nazwa, godziny_klasa_1, godziny_klasa_2, godziny_klasa_3)", Viewer)
        else:
            query = DatabaseTools.databaseQuery(self, "SELECT * FROM przedmioty", Viewer)

        if not query:
            print("Nie znaleziono klasy zgodnej z podanym filtrem.")
            input("Naciśnij Enter, aby wrócić do menu głównego.")
            LoggingTools.log(self, f"Nie znaleziono klasy zgodnej z podanym filtrem: '{filtr}'", "debug")
            Viewer.main(self)
        
        for subject in query:
            name = subject[0]
            classroom_type = subject[1]
            headteacher_subject = subject[2]
            class1_hours = subject[3]
            class2_hours = subject[4]
            class3_hours = subject[5]
            rows.append([name, classroom_type, headteacher_subject, class1_hours, class2_hours, class3_hours])

        table = tabulate(rows, headers, tablefmt="orgtbl", stralign="center")

        print(table)
        LoggingTools.log(self, f"Wyświetlono listę przedmiotów zgodnych z filtrowaniem: '{filtr}'")

        input("Naciśnij Enter, aby wrócić do menu głównego.")
        Viewer.main(self)

        


