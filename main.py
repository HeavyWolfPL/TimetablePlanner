# Main Tools
from tools.setup import Setup
from tools.generator import Generator
from tools.viewer import Viewer

# Misc Tools
from tools.tools import LoggingTools
from tools.tools import MiscTools

class Program():
    def __init__(self):
        self.self = self

    def main_menu(self):
        MiscTools.cls()

        print("""
        __________                 _        _     _      _____  _                             
        |__   __(_)               | |      | |   | |    |  __ \| |                            
            | |   _ _ __ ___   ___| |_ __ _| |__ | | ___| |__) | | __ _ _ __  _ __   ___ _ __ 
            | |  | | '_ ` _ \ / _ \ __/ _` | '_ \| |/ _ \  ___/| |/ _` | '_ \| '_ \ / _ \ '__|
            | |  | | | | | | |  __/ || (_| | |_) | |  __/ |    | | (_| | | | | | | |  __/ |   
            |_|  |_|_| |_| |_|\___|\__\__,_|_.__/|_|\___|_|    |_|\__,_|_| |_|_| |_|\___|_|   
        
        
        Work in Progress - v0.1
        """)
        
        temp = ""
        while temp.lower() not in ["0", "1", "2", "3", "e", "exit", "4"]:
            temp = input("""
    Wybierz tryb działania programu, wpisz odpowiedni znak i zatwierdź klawiszem Enter. 

    0 - Konfigurator danych
    1 - Generator
    2 - Przegląd danych
    E(xit) - Wyjście z programu.
        
    Wybór: """)

        if temp == "0":
            Setup.main(self)
        elif temp == "1":
            Generator.main(self)
        elif temp == "2":
            Viewer.main(self)
        elif temp == "3":
            Testing.test(self)
        elif temp.lower() in ["e", "exit", "q", "quit"]:
            exit()


### Testing ###
from tools.tools import DatabaseTools
from tools.generator import GeneratorTools
import json
from alive_progress import alive_bar
import time
class Testing():
    def __init__(self):
        self.self = self

    def main(self):
        print("Funkcja testowa")

    def compute():
        for i in range(100):
            time.sleep(0.05)
            yield

    def test(self):
        # result = DatabaseTools.databaseModify(self, "INSERT INTO `przydzieleni_nauczyciele` (`Przedmiot`, `Nauczyciel`, `Klasa`) VALUES ('Edukacja wczesnoszkolna', 'Pamela Gieldud', '1D')", Testing)
        with alive_bar(100) as bar: # TODO: https://github.com/rsalmei/alive-progress
            for i in Testing.compute():
                bar()
        Testing.compute()
        print("Koniec funkcji testowej")
### Testing ###



class Restart():
    def __init__(self):
        self.self = self

    def rerun():
        App = Program()
        App.main_menu()


## 

if __name__ == "__main__":
    LoggingTools.initialize_logging()
    LoggingTools.cleanup()
    App = Program()
    App.main_menu()

# TODO On Exit
# import atexit
# atexit.register(print, 'goodbye.')