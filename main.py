from bs4 import BeautifulSoup
from data.dataclasses import LessonHour, Classroom, Subject, Teacher, Class, Lesson, Timetable 

def ReadData():
    with open('data/Classes.xml', 'r') as f:
        data = f.read()

    fileData = BeautifulSoup(data, "xml")
    
    # Finding all instances of tag
    # `Class`
    classes = fileData.find_all('Class')
    print(classes)
    
    # Using find() to extract attributes
    # of the first instance of the tag
    class_ = fileData.find('Class', {'name':'1TI1'})
    print(class_)
    
    # Extracting the data stored in a
    # specific attribute of the
    # `child` tag
    attribute = class_.get('students')
    print(attribute)

ReadData()