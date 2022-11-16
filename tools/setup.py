# Database Setup

# Przydzieleni nauczyciele
# CREATE TABLE `przydzieleni_nauczyciele` (
#  `Lp` int(11) NOT NULL AUTO_INCREMENT,
#  `Przedmiot` varchar(255) NOT NULL,
#  `Nauczyciel` varchar(255) NOT NULL,
#  `Klasa` varchar(255) NOT NULL,
#  PRIMARY KEY (`Lp`),
#  KEY `przedmioty` (`Przedmiot`),
#  KEY `nauczyciele` (`Nauczyciel`),
#  KEY `klasy` (`Klasa`) USING BTREE,
#  CONSTRAINT `klasy` FOREIGN KEY (`Klasa`) REFERENCES `klasy` (`Klasa`) ON UPDATE CASCADE,
#  CONSTRAINT `nauczyciele` FOREIGN KEY (`Nauczyciel`) REFERENCES `nauczyciele` (`ImieNazwisko`) ON UPDATE CASCADE,
#  CONSTRAINT `przedmioty` FOREIGN KEY (`Przedmiot`) REFERENCES `przedmioty` (`Nazwa`) ON UPDATE CASCADE
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4