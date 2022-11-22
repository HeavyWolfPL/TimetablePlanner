# Tables
from tabulate import tabulate

# Dataclasses
from data.dataclasses import *
from operator import attrgetter

# Misc Tools
from tools.tools import MiscTools
from tools.tools import LoggingTools
import json
from sys import _getframe

# Database Stuff
from tools.tools import DatabaseTools

# GeneratorTools
from math import ceil # calculate_average_hours

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

        if temp == "1":
            Generator.assign_teachers(self)
        elif temp == "2":
            temp = input("Podaj przedmiot, którego nauczycieli chcesz wyświetlić (lub pozostaw puste, aby wyświetlić wszystkich nauczycieli): ")
            Generator.generate_timetable(self, temp)
        elif temp == "3":
            Generator.assign_teachers(self)
            day = input("Podaj dzień, dla którego chcesz wygenerować plan (lub pozostaw puste, aby wygenerować go dla całego tygodnia): ")
            school_class = input("Podaj klasę, dla której chcesz wygenerować plan (lub pozostaw puste, aby wygenerować go dla wszystkich): ")
            Generator.generate_timetable(self)
        elif temp.lower() in ["e", "exit", "q", "quit"]:
            #TODO DatabaseTools.databaseClose(self)
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

        query = DatabaseTools.databaseQuery(self, f"SELECT * FROM `przedmioty` ORDER BY `Nazwa` ASC", Generator)
        przedmioty = []
        for przedmiot in query:
            przedmioty.append(Subject(
                name = przedmiot[0],
                classroom_type = przedmiot[1],
                teacher_preference = int(przedmiot[2]),
                first_class_hr = int(przedmiot[3]),
                second_class_hr = int(przedmiot[4]),
                third_class_hr = int(przedmiot[5])
            ))

        query = DatabaseTools.databaseQuery(self, f"SELECT * FROM `nauczyciele` ORDER BY `Skrot` ASC", Generator)
        nauczyciele = []
        for nauczyciel in query:
            nauczyciele.append(Teacher(
                short_name = nauczyciel[0],
                name = nauczyciel[1],
                subject = nauczyciel[2],
                headteacher = int(nauczyciel[3]),
                hours = int(nauczyciel[4])
            ))
        nauczyciele.append(Teacher(name="", short_name="", subject = "", headteacher=0, hours=0)) 
        # This is done to prevent teacher not being assigned to a subject, when he/she is headteacher, and subject is taught by headteacher

        query = DatabaseTools.databaseQuery(self, f"SELECT * FROM `klasy` ORDER BY `Klasa` ASC", Generator)
        klasy = []
        for klasa in sorted(query):
            klasy.append(ClassTeam(
                name = klasa[0],
                students = klasa[1],
                headteacher = klasa[2],
                classroom = klasa[3],
            ))

        rows = []
        teachers_not_found = []
        for przedmiot in sorted(przedmioty, reverse = True, key=attrgetter('teacher_preference', 'name')): # Reverse = True - teacher_preference in descending order
            for klasa in klasy:
                query = DatabaseTools.databaseQuery(self, f"SELECT * from przydzieleni_nauczyciele WHERE (przedmiot = '{przedmiot.name}') AND (klasa = '{klasa.name}')", Generator) # klasy musi być w nawiasie, bruh?
                if query:
                    print(f"Nauczyciel przydzielony dla {klasa.name} | {przedmiot.name}:")
                    print(f"\t{query[0][2]}") # First assigned teacher, third column which is name
                    print("------------------------")
                else:
                    for nauczyciel in sorted(nauczyciele, key=attrgetter('subject', 'hours')):
                        if nauczyciel.subject == przedmiot.name:
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
                                continue
                            
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
                        if f"{klasa.name} | {przedmiot.name}" not in teachers_not_found:
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
        if any(row != ['---------', '---------', '---------'] for row in rows):
            headers = ["Klasa", "Przedmiot", "Nauczyciel"]
            print(tabulate(rows, headers, tablefmt="orgtbl", stralign="center"))
        if teachers_not_found:
            print("Nie znaleziono nauczycieli dla klas: \n\t{}".format(', \n\t'.join(teachers_not_found)))
        Generator.main(self)

    def generate_timetable(self, day = None, school_class = None):
        print("Generowanie planu lekcji... \n")

        data = GeneratorTools.get_data(self, True, False)

        days = [[1, "Poniedzialek"], [2, "Wtorek"], [3, "Sroda"], [4, "Czwartek"], [5, "Piatek"]] # No polish chars due to them not being in the database as columns

        # print(data)
        # print()
        for class_team in data.classes:
            lesson_hours = GeneratorTools.calculate_average_hours(self, data.subjects, class_team)
            if lesson_hours > len(data.lesson_hours):
                print(f"Klasa {class_team.name} ma więcej godzin lekcyjnych niż przewiduje plan lekcji. Nie można wygenerować planu lekcji.")
                LoggingTools.log(self, f"Klasa {class_team.name} ma więcej godzin lekcyjnych niż przewiduje plan lekcji. Nie można wygenerować planu lekcji.", "error", _getframe().f_lineno)
                return False

            total_lessons = []
            for day in days:
                lessons = []
                for lesson_hour in range(1, lesson_hours):
                    for subject in data.subjects:
                        assigned_teacher = MiscTools.find(self, lambda AssignedTeacher: ((AssignedTeacher.subject == subject) and (AssignedTeacher.assigned_class == class_team)), data.assigned_teachers)
                        lessons.append(Lesson(
                            assigned_class = class_team.name,
                            hour = lesson_hour, 
                            classroom = GeneratorTools.find_classroom(self, subject.classroom_type, day, lesson_hour),
                            subject = subject.name,
                            teacher = assigned_teacher.teacher.short_name,
                    ))
                total_lessons.append(lessons)
            print(total_lessons)

            with open(f"data/plany_lekcji/{class_team.name}.txt", "w", encoding="UTF-8") as file:
                file.write(str(total_lessons))
                # json.dump(total_lessons, file, skipkeys=True, indent=4)

        # query = DatabaseTools.databaseModify(self, f"INSERT INTO `plan_lekcji` (`Klasa`, `GodzinaLekcyjna`, `Poniedzialek`, `Wtorek`, `Sroda`, `Czwartek`, `Piatek`) VALUES ('{class_team.name}', '{lesson_hour}', 'x', 'x', 'x', 'x', 'x');", Generator)

        print("Zakończono generowanie planu lekcji.")

class GeneratorTools():
    def __init__(self):
        self.self = self

    def get_data(self, assigned_teachers = False, timetable = False):
        """
        Pobiera dane z bazy danych i zwraca je w postaci odpowiedniej dataclassy.
        \n
        Parametry:
            self - referencja do obiektu\n
            assigned_teachers - czy pobierać dodatkowo dane o przypisanych nauczycielach\n
            timetable - czy pobierać dane o wygenerowanym planie lekcji\n
        \n
        Zwraca:
            data - dane w postaci dataclassy podzielonej na kategorie danych, każda z nich zawierająca dane w odpowiedniej dataclassie\n
                lesson_hours: List[LessonHour]
                classroom_types: List[ClassroomType]
                classrooms: List[Classroom]
                subjects: List[Subject]
                teachers: List[Teacher]
                classes: List[ClassTeam]
                timetables: List[Timetable]
        """
        data = DataPack(
            lesson_hours = [],
            classroom_types = [],
            classrooms = [],
            subjects = [],
            teachers = [],
            classes = [],
            assigned_teachers = [],
            timetables = []
        )

        # Lesson hours
        sql = DatabaseTools.databaseQuery(self, "SELECT * FROM godziny_lekcyjne")
        if sql:
            for i, element in enumerate(sql):
                sql[i] = LessonHour(
                    lp = element[0], 
                    start = element[1], 
                    end = element[2]
                )
            data.lesson_hours = sql

        # Classroom types
        sql = DatabaseTools.databaseQuery(self, "SELECT * FROM sale_rodzaje")
        if sql:
            for i, element in enumerate(sql):
                sql[i] = ClassroomType(
                    name = element[0],
                )
            data.classroom_types = sql

        # Classrooms
        sql = DatabaseTools.databaseQuery(self, "SELECT * FROM sale")
        if sql:
            for i, element in enumerate(sql):
                sql[i] = Classroom(
                    name = element[0],
                    classroom_type = MiscTools.find(self, lambda ClassroomType: ClassroomType.name == element[1], data.classroom_types),
                    max_students = element[2]
                )
            data.classrooms = sql

        # Subjects
        sql = DatabaseTools.databaseQuery(self, "SELECT * FROM przedmioty")
        if sql:
            for i, element in enumerate(sql):
                sql[i] = Subject(
                    name = element[0], 
                    classroom_type = MiscTools.find(self, lambda ClassroomType: ClassroomType.name == element[1], data.classroom_types), 
                    teacher_preference = element[2], 
                    first_class_hr = element[3], 
                    second_class_hr = element[4], 
                    third_class_hr = element[5]
                )
            data.subjects = sql

        # Teachers
        sql = DatabaseTools.databaseQuery(self, "SELECT * FROM nauczyciele")
        if sql:
            for i, element in enumerate(sql):
                sql[i] = Teacher(
                    short_name = element[0], 
                    name = element[1], 
                    subject = MiscTools.find(self, lambda Subject: Subject.name == element[1], data.subjects), 
                    headteacher = element[3], 
                    hours = element[4]
                )
            data.teachers = sql

        # Classes
        sql = DatabaseTools.databaseQuery(self, "SELECT * FROM klasy")
        if sql:
            for i, element in enumerate(sql):
                sql[i] = ClassTeam(
                    name = element[0],
                    students = element[1],
                    headteacher = MiscTools.find(self, lambda Teacher: Teacher.name == element[2], data.teachers),
                    classroom = MiscTools.find(self, lambda Classroom: Classroom.name == element[3], data.classrooms)
                )
            data.classes = sql

        if assigned_teachers:
            sql = DatabaseTools.databaseQuery(self, "SELECT * FROM przydzieleni_nauczyciele")
            if sql:
                for i, element in enumerate(sql):
                    sql[i] = AssignedTeacher(
                        lp = element[0],
                        subject = MiscTools.find(self, lambda Subject: Subject.name == element[1], data.subjects),
                        teacher = MiscTools.find(self, lambda Teacher: Teacher.name == element[2], data.teachers),
                        assigned_class = MiscTools.find(self, lambda ClassTeam: ClassTeam.name == element[3], data.classes),
                    )
                data.assigned_teachers = sql

        if timetable:
            data.timetables = []
            # TODO DataPack.timetables     

        return data

    def calculate_hours(self, subject, school_class):
        if school_class.name[0] == "1":
            total = subject.first_class_hr
        elif school_class.name[0] == "2":
            total = subject.second_class_hr
        elif school_class.name[0] == "3":
            total = subject.third_class_hr

        return total
        # TODO Couple hours in a row, aka blocks

    def calculate_average_hours(self, subjects, school_class):
        hours = 0
        for subject in subjects:
            hours += GeneratorTools.calculate_hours(self, subject, school_class)
        return ceil(hours / 5) # math.ceil - Round only up, never down

    def get_assigned_teacher(self, teachers, subject, school_class):
        for teacher in teachers:
            if teacher.subject == subject and teacher.assigned_class == school_class:
                return teacher
        return None

    def teacher_availability(self, teacher, day, hour):
        lessons = DatabaseTools.databaseQuery(self, f"SELECT {day[1]} FROM `plan_lekcji` WHERE `GodzinaLekcyjna` = '{hour}' LIMIT 0, 50", Generator)
        if not lessons:
            LoggingTools.log(self, f"[Generator Tools | teacher_availability] Nie zwrocono żadnych danych o zajęciach na godzinę {hour} dnia {day}.", "info", _getframe().f_lineno)
            return True
        else:
            for lesson in lessons:
                if lesson[1] == teacher.short_name:
                    return False
            return True

    def classroom_availability(self, classroom, day, hour):
        lessons = DatabaseTools.databaseQuery(self, f"SELECT {day[1]} FROM `plan_lekcji` WHERE `GodzinaLekcyjna` = '{hour}' LIMIT 0, 50", Generator)
        if not lessons:
            LoggingTools.log(self, f"[Generator Tools | classroom_availability] Nie zwrocono żadnych danych o zajęciach na godzinę {hour} dnia {day}.", "info", _getframe().f_lineno)
            return True
        else:
            for lesson in lessons:
                if lesson == classroom[1]:
                    return False
            return True

    def find_classroom(self, subject_type, day, hour):
        classrooms = DatabaseTools.databaseQuery(self, f"SELECT * FROM `sale` WHERE `Rodzaj` = '{subject_type.name}' LIMIT 0, 50", Generator)

        if not classrooms:
            LoggingTools.log(self, f"[Generator Tools | find_classroom] Nie znaleziono żadnej sali o typie {subject_type.name}.", "info", _getframe().f_lineno)
            return None
        else:
            for classroom in classrooms:
                if GeneratorTools.classroom_availability(self, classroom, day, hour):
                    return classroom
            return None

