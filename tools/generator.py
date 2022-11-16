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

    def assign_headteachers(self):
        pass # N/A for 1-3 years of school

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

        query = DatabaseTools.databaseQuery(self, f"SELECT * FROM `przedmioty` ORDER BY `Nazwa` ASC", Generator)
        przedmioty = []
        for przedmiot in query:
            przedmioty.append(Subject(
                name = przedmiot[0],
                teacher_preference = int(przedmiot[1]),
                first_class_hr = int(przedmiot[2]),
                second_class_hr = int(przedmiot[3]),
                third_class_hr = int(przedmiot[4])
            ))
        print(przedmioty)

        query = DatabaseTools.databaseQuery(self, f"SELECT * FROM `nauczyciele` ORDER BY `Skrot` ASC", Generator)
        nauczyciele = []
        for nauczyciel in query:
            nauczyciele.append(Teacher(
                short_name = nauczyciel[0],
                name = nauczyciel[1],
                subjects = nauczyciel[2],
                headteacher = int(nauczyciel[3]),
                hours = int(nauczyciel[4])
            ))
        nauczyciele.append(Teacher(name="", short_name="", subjects="", headteacher=0, hours=0)) 
        # This is done to prevent teacher not being assigned to a subject, when he/she is headteacher, and subject is taught by headteacher
        print(nauczyciele)

        query = DatabaseTools.databaseQuery(self, f"SELECT * FROM `klasy` ORDER BY `Klasa` ASC", Generator)
        klasy = []
        for klasa in sorted(query):
            klasy.append(Class(
                name = klasa[0],
                students = klasa[1],
                headteacher = klasa[2]
            ))

        print()
        
        rows = []
        teachers_not_found = []
        for przedmiot in sorted(przedmioty, reverse = True, key=attrgetter('teacher_preference', 'name')): # Reverse = True - teacher_preference in descending order
            for klasa in klasy:
                query = DatabaseTools.databaseQuery(self, f"SELECT * from przydzieleni_nauczyciele WHERE (przedmiot = '{przedmiot.name}') AND (klasa = '{klasa.name}')", Generator) # klasy musi być w nawiasie, bruh?
                if query:
                    print(f"Nauczyciel przydzielony dla {klasa.name} | {przedmiot.name}:")
                    print(f"\t{query}")
                    print("------------------------")
                else:
                    for nauczyciel in sorted(nauczyciele, key=attrgetter('subjects', 'hours')):
                        if nauczyciel.subjects == przedmiot.name:
                            if (przedmiot.teacher_preference == 1) and (nauczyciel.name != klasa.headteacher):
                                continue

                            if klasa.name[0] == "1":
                                nauczyciel.hours += przedmiot.first_class_hr
                            elif klasa.name[0] == "2":
                                nauczyciel.hours += przedmiot.second_class_hr
                            elif klasa.name[0] == "3":
                                nauczyciel.hours += przedmiot.third_class_hr
                            if nauczyciel.hours > 18:
                                LoggingTools.log(self, f"Nauczyciel {nauczyciel.short_name} ({przedmiot.name}) nie może zostać przydzielony do klasy {klasa.name} z powodu przekroczenia limitu godzin.", "debug")
                                teachers_not_found.append(f"{klasa.name} | {przedmiot.name} | Brak wolnego etatu")
                                pass
                            
                            query = DatabaseTools.databaseModify(self, f"INSERT INTO `przydzieleni_nauczyciele` (`Lp`, `Przedmiot`, `Nauczyciel`, `Klasa`) VALUES (0, '{przedmiot.name}', '{nauczyciel.name}', '{klasa.name}')", Generator)
                            if query == 0:
                                print(f"Nie udało się przydzielić nauczyciela {nauczyciel.name} do klasy {klasa.name} na przedmiot {przedmiot.name}.")
                                LoggingTools.log(self, f"Nie udało się przydzielić nauczyciela {nauczyciel.name} do klasy {klasa.name} na przedmiot {przedmiot.name}.", "error", _getframe().f_lineno)

                            query = DatabaseTools.databaseModify(self, f"UPDATE `nauczyciele` SET `Godziny` = '{nauczyciel.hours}' WHERE `Skrot` = '{nauczyciel.short_name}'", Generator)
                            if query == 0:
                                print(f"Nie udało się zaktualizować godzin nauczyciela {nauczyciel.name} ({nauczyciel.short_name}).")
                                LoggingTools.log(self, f"Nie udało się zaktualizować godzin nauczyciela {nauczyciel.name} ({nauczyciel.short_name}).", "error", _getframe().f_lineno)

                            print(f"Przydzielono nauczyciela dla {klasa.name} | {przedmiot.name}:")
                            print(f"\t{nauczyciel.name} | Godziny: {nauczyciel.hours}")
                            print("------------------------")
                            rows.append([klasa.name, przedmiot.name, nauczyciel.name])
                            break # break the "for nauczyciel in nauczyciele" loop

                        else:
                            pass # Executes if teacher doesn't teach the subject
                    else:
                        if przedmiot.teacher_preference == 1:
                            teachers_not_found.append(f"{klasa.name} | {przedmiot.name} | Wychowawca nie może zostać nauczycielem przedmiotu")
                        else:
                            teachers_not_found.append(f"{klasa.name} | {przedmiot.name} | Brak nauczyciela przedmiotu")
            else:
                rows.append(["---------", "---------", "---------"] ) # Separating line between subjects
                pass # Executes after the "for klasa in klasy" loop
        else:
            pass # Executes after the "for przedmiot in przedmioty" loop

        rows.pop() # Removes the last separating line, as it somehow doubles
        headers = ["Klasa", "Przedmiot", "Nauczyciel"]
        print(tabulate(rows, headers, tablefmt="orgtbl", stralign="center"))
        print("Nie znaleziono nauczycieli dla klas: \n\t{}".format(', \n\t'.join(teachers_not_found)))