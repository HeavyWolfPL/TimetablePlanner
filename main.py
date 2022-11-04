# Main Tools
from tools.generator import Generator
from tools.editor import Editor
from tools.viewer import Viewer

# Misc Tools
from tools.tools import LoggingTools

class Program():
    def __init__(self):
        self.self = self

    def main_menu(self):

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
        while temp.lower() not in ["1", "2", "3", "e", "exit", "4"]:
            temp = input("""
    Wybierz tryb działania programu, wpisz odpowiedni znak i zatwierdź klawiszem Enter. 

    1 - Generator
    2 - Edytor Danych
    3 - Przegląd danych
    4 - Funkcja testowa
    E(xit) - Wyjście z programu.
        
    Wybór: """)

        
        if temp == "1":
            Generator.main(self)
        elif temp == "2":
            Editor.main(self)
        elif temp == "3":
            Viewer.main(self)
        elif temp == "4":
            Testing.test(self)
        elif temp.lower() in ["e", "exit", "q", "quit"]:
            exit()


### Testing ###
from tools.tools import DatabaseTools
class Testing():
    def __init__(self):
        self.self = self

    def test(self):
        result = DatabaseTools.databaseQuery(self, "SELECT * FROM klasy WHERE klasa = '5A'")
        print(result)
        if result == []:
            print("Nie znaleziono klasy")
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
    App = Program()
    App.main_menu()