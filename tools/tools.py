#############
# MiscTools #
#############
import os # cls 

################
# DatabaseTool #
################
import json
import mysql.connector
from mysql.connector import errorcode
from sys import _getframe

##################
# LoggingHandler #
##################
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

    def find(self, filtr, data):
        """Return first item in sequence where f(item) == True."""
        # classroom_type = find(lambda ClassroomType: ClassroomType.name == 'Uniwersalna', sale_rodzaje)
        for item in data:
            if filtr(item):
                return item        

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
            if debug:
                print("Error Code:", err.errno)
                print("SQLSTATE:", err.sqlstate)
                print("Message:", err.msg)
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                if db_ip == "IP_GOES_HERE":
                    print("Nie podano adresu IP serwera bazy danych.")
                    LoggingTools.log(self, "Błędny adres bazy danych.", "crash")
                if db_user == "USER_GOES_HERE":
                    print("Nie podano nazwy użytkownika bazy danych.")
                    LoggingTools.log(self, "Błędna nazwa użytkownika bazy danych.", "crash")
                if db_pass == "PASS_GOES_HERE":
                    print("Nie podano hasła bazy danych.")
                    LoggingTools.log(self, "Błędne hasło użytkownika bazy danych.", "crash")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Baza danych nie istnieje.")
                LoggingTools.log(self, "Błędna nazwa bazy danych.", "crash")
            else:
                LoggingTools.log(self, f"Wystąpił nieznany błąd: \nKod - {err.errno} \nTreść - {err.msg} \nSQL State - {err.sqlstate} \nCałość - {err}", "error", _getframe().f_lineno)

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
        #TODO Walidacja bazy danych
        # Sprawdzić czy każda tabelka ma jakieś linijki

    # MariaDB Error Codes
    # https://mariadb.com/kb/en/mariadb-error-codes/

    def databaseQuery(self, query, on_fail = None):
        """
        Zwraca wartość zwróconą przez zapytanie SQL, tzw. kwerenda.

        Parametry:
            self - referencja do obiektu
            query - zapytanie SQL
            on_fail - klasa funkcji, która ma być wywołana w przypadku błędu.

        Zwraca:
            result - wartość zwróconą przez zapytanie SQL lub False
        """
        database = DatabaseTools.databaseGet(self)
        cursor = database.cursor()

        try:
            cursor.execute(query)
            result = cursor.fetchall()
        except mysql.connector.Error as err:
            if debug:
                print("Error Code:", err.errno)
                print("SQLSTATE:", err.sqlstate)
                print("Message:", err.msg)
                print("Query:", query)
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Błędne hasło lub login.")
                LoggingTools.log(self, "Błędne hasło lub login.", "crash", _getframe().f_lineno)
            elif err.errno == errorcode.ER_BAD_FIELD_ERROR: # Error code - 1054 aka Unknown column
                print("Nie znaleziono wyników zgodnych z podanym filtrem.")
                LoggingTools.log(self, f"Nie znaleziono klasy zgodnej z podanym filtrem.", "debug")
                input("Naciśnij Enter, aby wrócić do menu głównego.")
            else:
                print("Wystąpił nieznany błąd. Odpowiednia treść została zapisana w logu.")
                LoggingTools.log(self, f"Wystąpił nieznany błąd: \nSQL - {query} \nKod - {err.errno} \nTreść - {err.msg} \nSQL State - {err.sqlstate} \nCałość - {err}", "error", _getframe().f_lineno)
                input("Naciśnij Enter, aby wrócić do menu głównego.")
            
            if on_fail != None:
                on_fail.main(self)
                

        if result == []:
            result = False

        LoggingTools.log(self, f'Zapytanie SQL: "{query}" \nZwrócono: "{result}"', "debug")
        return result

    def databaseModify(self, command, on_fail = None, multiple_statements = False, rollback_on_error = False):
        """
        Wykonuje polecenie SQL, tzw. komenda.

        Parametry:
            self - referencja do obiektu\n
            command - polecenie SQL\n
            on_fail - klasa funkcji, która ma być wywołana w przypadku błędu\n
            multiple_statements - więcej niż jedno polecenie SQL w wywołaniu funkcji\n
            rollback_on_error - cofanie zmian w przypadku błędu\n

        Zwraca:
            int - wartość dodanych/zmienionych wierszy
        """
        database = DatabaseTools.databaseGet(self)
        cursor = database.cursor()

        if not multiple_statements:
            try:
                cursor.execute(command)
                database.commit()
            except mysql.connector.Error as err:
                if debug:
                    print("Error Code:", err.errno)
                    print("SQLSTATE", err.sqlstate)
                    print("Message", err.msg)
                    print("Query:", command)
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Błędne hasło lub login.")
                    LoggingTools.log(self, "Błędne hasło lub login.", "crash", _getframe().f_lineno)
                elif err.errno == errorcode.ER_BAD_FIELD_ERROR: # Error code - 1054 aka Unknown column '%s' in '%s'
                    print("Nie znaleziono wyników zgodnych z podanym filtrem.")
                    LoggingTools.log(self, f"Nie znaleziono klasy zgodnej z podanym filtrem.", "debug")
                    input("Naciśnij Enter, aby wrócić do menu głównego.")
                elif err.errno == errorcode.ER_DUP_ENTRY: # Error code - 1062 aka Duplicate entry
                    print("Wprowadzona wartość już istnieje w bazie danych.")
                    LoggingTools.log(self, f'Wprowadzona wartość już istnieje w bazie danych. \nZapytanie SQL: "{command}"', "debug")
                    input("Naciśnij Enter, aby wrócić do menu głównego.")
                else:
                    print("Wystąpił nieznany błąd. Odpowiednia treść została zapisana w logu.")
                    LoggingTools.log(self, f"Wystąpił nieznany błąd: \nSQL - {command} \nKod - {err.errno} \nTreść - {err.msg} \nSQL State - {err.sqlstate} \nCałość - {err}", "error", _getframe().f_lineno)
                    input("Naciśnij Enter, aby wrócić do menu głównego.")
                
                if on_fail != None:
                    on_fail.main(self)

        if multiple_statements:
            try:
                for statement in command:
                    cursor.execute(statement)
                    if not rollback_on_error:
                        database.commit() # commit po każdym poleceniu by móc wycofać zmiany w przypadku błędu
                        result += cursor.rowcount
            except Exception as e:
                if rollback_on_error:
                    database.rollback()
                    LoggingTools.log(self, f'Błąd podczas modyfikowania wierszy! \nZapytanie SQL: "{command}" \nZmodyfikowane wiersze: "{result}"', "error")
                raise
            else:
                if rollback_on_error:
                    database.commit()
                    result += cursor.rowcount
        else:
            result = cursor.rowcount
        
        if result == []:
            result = False

        LoggingTools.log(self, f'Zapytanie SQL: "{command}" \nZmodyfikowane wiersze: "{result}"', "debug")
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
            message - treść wiadomości\n
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
            with open (f"logs/[Crash] {now}.log", "w", encoding="UTF-8") as crash_log:
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

    def cleanup():
        """
        Czyści określoną ilość plików zawierających logi, w zależności od trybu.\n
        Funkcja nie usuwa tzw. crash logów.

        Parametry:
            self - referencja do obiektu\n
            mode - tryb czyszczenia logów\n
                days - usuwa logi starsze niż podana ilość dni\n
                number - pozostawia najnowszą ilość logów, a resztę usuwa\n
            amount - ilość logów
        """
        with open("config.json", "r") as config: 
            data = json.load(config)
            mode = data["log_cleanup_mode"]
            amount = data["log_cleanup_amount"]
        self = None

        to_be_removed = []

        if mode == "days":
            now = datetime.now()
            for log in os.listdir("./logs"):
                if log.endswith(".log") and not log.startswith("[Crash]"):
                    log_date = datetime.strptime(log[7:26], '%d-%m-%Y %H-%M-%S') # [7:26] - date inside file name
                    if (now - log_date).days > amount:
                        to_be_removed.append(log)

        elif mode == "number":
            for log in os.listdir("./logs"):
                if log.endswith(".log") and not log.startswith("[Crash]"):
                    to_be_removed.append(log)
            to_be_removed.sort(reverse=True)
            to_be_removed = to_be_removed[amount:]


        LoggingTools.log(self, f"Rozpoczynanie usuwania logów. Do usunięcia - {len(to_be_removed)}. Tryb - {mode}, ilość - {amount}", "debug")
        for log in to_be_removed:
            os.remove(f"./logs/{log}")
            LoggingTools.log(self, f"Usunięto log: {log}", "debug")



        

        
