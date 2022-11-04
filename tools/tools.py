import os

# DatabaseTool
import json
import mysql.connector
from mysql.connector import errorcode
from sys import _getframe

# LoggingHandler
import logging
from datetime import datetime
from pathlib import Path

with open("config.json", "r") as config: 
    data = json.load(config)
    debug = data["debug"]

class MiscTools():
    def __init__(self):
        self.self = self

    def cls():
        os.system('cls' if os.name=='nt' else 'clear')

class DatabaseTools():
    def __init__(self):
        self.self = self

    def databaseGet(self):
        with open("config.json", "r") as config: 
            data = json.load(config)
            db_ip = data["db_ip"]
            db_user = data["db_user"]
            db_pass = data["db_pass"]
            db_database = data["db_database"]

        try:
            database = mysql.connector.connect(
                host = db_ip,
                user = db_user,
                password = db_pass,
                database = db_database,
            )
        except mysql.connector.Error as err:
            # print("Error Code:", err.errno)
            # print("SQLSTATE", err.sqlstate)
            # print("Message", err.msg)
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Błędne hasło lub login.")
                # TODO: Sprawdzić czy podano hasło i zmieniono wartości
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Baza danych nie istnieje.")
                # TODO: Uzupełnić błąd
            else:
                print(err)

    
        LoggingTools.log(self, "Połączono z bazą danych.")


        # database.close()
        return database

    def databaseValidate(self):
        """
        Sprawdza poprawność bazy danych, tj. wypełnienie tabelek, połączenie, itp.

        Parametry:
            self - referencja do obiektu

        Zwraca:
            True - jeśli dane są poprawne
            False - jeśli dane są niepoprawne
        """

        query = DatabaseTools.databaseQuery(self, "SELECT * FROM klasy")
        #TODO: Walidacja bazy danych



    def databaseQuery(self, query, on_fail = None):
        """
        Zwraca wartość zwróconą przez zapytanie SQL, tzw. kwerenda.

        Parametry:
            self - referencja do obiektu
            query - zapytanie SQL
            on_fail - klasa funkcji, która ma być wywołana w przypadku błędu.

        Zwraca:
            return - wartość zwróconą przez zapytanie SQL
        """
        database = DatabaseTools.databaseGet(self)
        cursor = database.cursor()

        try:
            cursor.execute(query)
            result = cursor.fetchall()
        except mysql.connector.Error as err:
            # TODO: Wypełnić błędy
            if debug:
                print("Error Code:", err.errno)
                print("SQLSTATE", err.sqlstate)
                print("Message", err.msg)
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Błędne hasło lub login.")
                LoggingTools.log(self, "Błędne hasło lub login.", "crash", _getframe().f_lineno)
            elif err.errno == errorcode.ER_BAD_FIELD_ERROR: # Error code - 1054 aka Unknown column
                print("Nie znaleziono wyników zgodnych z podanym filtrem.")
                LoggingTools.log(self, f"Nie znaleziono klasy zgodnej z podanym filtrem.", "debug")
                input("Naciśnij Enter, aby wrócić do menu głównego.")
            else:
                print("Wystąpił nieznany błąd. Odpowiednia treść została zapisana w logu.")
                LoggingTools.log(self, f"Wystąpił nieznany błąd: \nKod - {err.errno} \nTreść - {err.msg} \nSQL State - {err.sqlstate} \nCałość - {err}", "error", _getframe().f_lineno)
                input("Naciśnij Enter, aby wrócić do menu głównego.")
            
            if on_fail != None:
                on_fail.main(self)
                

        if result == []:
            print("Wynik jest pusty. Sprawdź poprawność zapytania.")
            result = False

        return result

    def databaseClose(self, database):
        database.close()
        LoggingTools.log(self, "Zamknięto połączenie z bazą danych.")

    
class LoggingTools():
    def __init__(self):
        self.self = self

    def initialize_logging():
        with open("config.json", "r") as config: 
            data = json.load(config)
            debug = data["debug"]

        now = datetime.now().strftime('%d-%m-%Y %H-%M-%S')
        logs_dir = Path("./logs")
        if (logs_dir.exists() == False) or (logs_dir.is_dir() == False):
            logs_dir.mkdir()

        timetable_logs = logging.getLogger('timetable_logs')
        if debug:
            timetable_logs.setLevel(logging.DEBUG)
        else:
            timetable_logs.setLevel(logging.INFO)
        timetable_logs_handler = logging.FileHandler(filename=f"logs/[Logs] {str(now)}.log", encoding='utf-8', mode='w')
        timetable_logs_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        timetable_logs.addHandler(timetable_logs_handler)
        # print("[Logging] Aktywne.")
        timetable_logs.info("[Logging] Aktywne.")

    def log(self, message, log_type = "info", line = ""):
        """
        Zapisuje wiadomość do pliku logów.

        Parametry:
            self - referencja do obiektu\n
            messege - treść wiadomości\n
            log_type - typ wiadomości (debug, info, error, crash/critical)\n
                crash/critical - wywołuje zamknięcie programu.\n
            line - linia, z której została wywołana funkcja   
        """
        with open("config.json", "r") as config: 
            data = json.load(config)
            debug = data["debug"]

        timetable_logs = logging.getLogger('timetable_logs')
        now = datetime.now().strftime('%d-%m-%Y %H-%M-%S')

        if line:
            line = f"[Linia {line}]"

        if debug and (log_type == "debug"):
            timetable_logs.debug(f"{message} {line}")
        elif log_type == "info":
            timetable_logs.info(f"{message} {line}")
        elif log_type == "error":
            timetable_logs.error(f"{message} {line}")
        elif log_type in ["crash", "critical"]:
            with open (f"logs/[Crash] {now}.log", "w") as crash_log:
                crash_log.write(f"""
                ---------------------------
                Timetable Planner Crash Log
                {now}
                ---------------------------
                {message} 
                {line}""")
                crash_log.write(f"{message} {line}")
            timetable_logs.critical(f"{message} {line}")
            exit()


        

        
