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
    X - Plan lekcji
    E - Wyjście z Przeglądu danych.
        
    Wybór: """)

        if temp == "1":
            temp = input("Podaj klasę lub wychowawcę klasy, którą chcesz wyświetlić (lub pozostaw puste, aby wyświetlić wszystkie klasy): ")
            Viewer.show_classes(self, temp)
            Viewer.main(self)
        elif temp == "2":
            temp = input("Podaj przedmiot, którego nauczycieli chcesz wyświetlić (lub pozostaw puste, aby wyświetlić wszystkich nauczycieli): ")
            Viewer.show_teachers(self, temp)
            Viewer.main(self)
        elif temp == "3":
            Viewer.show_subjects(self)
            Viewer.main(self)
        elif temp == "4":
            Viewer.show_rooms(self)
            Viewer.main(self)
        # elif temp == "5":
        #     #Viewer.show_timetable()
        #     return
        elif temp.lower() in ["e", "exit", "q", "quit"]:
            exit()
            # Restart.rerun() #TODO ImportError: cannot import name 'Viewer' from partially initialized module 'tools.viewer' (most likely due to a circular import)

    def show_classes(self, filtr = None):
        rows = []
        headers = ["Klasa", "Nauczyciel", "Sala", "Uczniowie"]

        if filtr.lstrip().rstrip():
            query = DatabaseTools.databaseQuery(self, f"SELECT * FROM klasy WHERE {filtr} IN (`klasa`, `wychowawca`)", Viewer)
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

    
    def show_teachers(self, filtr = None): 
        rows = []
        headers = ["Imię i Nazwisko", "Przedmiot", "Wychowawstwo", "Godziny"]

        if filtr.lstrip().rstrip():
            query = DatabaseTools.databaseQuery(self, f"SELECT * FROM nauczyciele WHERE '{filtr}' in (`IMIENAZWISKO`, `SKROT`, `PRZEDMIOT`)", Viewer)
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

    def show_subjects(self):
        rows = []
        headers = ["Przedmiot", "Typ sali", "Przedmiot wychowawcy", "I Klasa / Godziny", "II Klasa / Godziny", "III Klasa / Godziny"]

        query = DatabaseTools.databaseQuery(self, "SELECT * FROM przedmioty", Viewer)

        if not query:
            print("Nie znaleziono przedmiotów.")
            input("Naciśnij Enter, aby wrócić do menu głównego.")
            LoggingTools.log(self, f"Nie znaleziono przedmiotów.", "debug")
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
        LoggingTools.log(self, f"Wyświetlono listę przedmiotów.")

        input("Naciśnij Enter, aby wrócić do menu głównego.")

    def show_rooms(self):
        rows = []
        headers = ["Sala", "Rodzaj", "Miejsca"]

        query = DatabaseTools.databaseQuery(self, "SELECT * FROM sale", Viewer)

        if not query:
            print("Nie znaleziono sal.")
            input("Naciśnij Enter, aby wrócić do menu głównego.")
            LoggingTools.log(self, f"Nie znaleziono sal.", "debug")
            Viewer.main(self)
        
        for classroom in query:
            name = classroom[0]
            classroom_type = classroom[1]
            seats = classroom[2]
            rows.append([name, classroom_type, seats])

        table = tabulate(rows, headers, tablefmt="orgtbl", stralign="center")

        print(table)
        LoggingTools.log(self, f"Wyświetlono listę sal.")

        input("Naciśnij Enter, aby wrócić do menu głównego.")

    def show_timetable(self, filtr = None):
        rows = []
        headers = ["Dzień", "Godzina", "Przedmiot", "Nauczyciel", "Sala"]

        # ['1C', 1, '5', 'Edukacja wczesnoszkolna', 'AK']
        # TODO Dokończyć

        if filtr:
            query = DatabaseTools.databaseQuery(self, f"SELECT * FROM plan_lekcji WHERE {filtr.lstrip().rstrip()} IN `Klasa` ORDER BY `plan_lekcji`.`Klasa` ASC", Viewer)
        else:
            query = DatabaseTools.databaseQuery(self, "SELECT * FROM `plan_lekcji` ORDER BY `plan_lekcji`.`Klasa` ASC", Viewer)

        if not query:
            print("Nie znaleziono planu zgodnego z podanym filtrem.")
            input("Naciśnij Enter, aby wrócić do menu głównego.")
            LoggingTools.log(self, f"Nie znaleziono planu zgodnego z podanym filtrem: '{filtr}'", "debug")
            Viewer.main(self)

        for lesson in query:
            day = lesson[0]
            hour = lesson[1]
            school_class = lesson[2]
            subject = lesson[3]
            teacher = lesson[4]
            room = lesson[5]
            rows.append([day, hour, school_class, subject, teacher, room])

        table = tabulate(rows, headers, tablefmt="orgtbl", stralign="center")

        print(table)
        LoggingTools.log(self, f"Wyświetlono plan zgodny z filtrowaniem: '{filtr}'")

        input("Naciśnij Enter, aby wrócić do menu głównego.")

        


