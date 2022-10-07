# from bs4 import BeautifulSoup
import dataclasses
import json
from data.dataclasses import Flags, LessonHour, Classroom, Subject, Teacher, Class, Lesson, Timetable 


def FlagsExample():
    data = Flags()
    print(data)
    data = json.dumps(dataclasses.asdict(data), indent=4)
    with open('data/examples/Flags.json', 'w') as f:
        f.write(data)
FlagsExample()

def LessonHourExample():
    data = LessonHour("8:00", "8:45", [Flags(early=True)])
    print(data)
    data = json.dumps(dataclasses.asdict(data), indent=4)
    with open('data/examples/LessonHour.json', 'w') as f:
        f.write(data)
LessonHourExample()

def ClassroomExample():
    data = Classroom(name="1", type="normal", max_students=30)
    print(data)
    data = json.dumps(dataclasses.asdict(data), indent=4)
    with open('data/examples/Classroom.json', 'w') as f:
        f.write(data)
ClassroomExample()

def SubjectExample():
    data = Subject(name="Math", groups=False, classroom_type="normal")
    print(data)
    data = json.dumps(dataclasses.asdict(data), indent=4)
    with open('data/examples/Subject.json', 'w') as f:
        f.write(data)
SubjectExample()

def TeacherExample():
    data = Teacher(name="John Doe", subjects=[Subject(name="Math", groups=False, classroom_type="normal")])
    print(data)
    data = json.dumps(dataclasses.asdict(data), indent=4)
    with open('data/examples/Teacher.json', 'w') as f:
        f.write(data)
TeacherExample()

def ClassExample():
    data = Class(name="1TI1", students=30, subjects=[Subject(name="Math", groups=False, classroom_type="normal")], teachers=[Teacher(name="John Doe", subjects=[Subject(name="Math", groups=False, classroom_type="normal")])], hour_flags=[Flags(early=True)], classroom="1")
    print(data)
    data = json.dumps(dataclasses.asdict(data), indent=4)
    with open('data/examples/Class.json', 'w') as f:
        f.write(data)
ClassExample()

def LessonExample():
    data = Lesson(hour=LessonHour("8:00", "8:45", [Flags(early=True)]), classroom=Classroom(name="1", type="normal", max_students=30), subject=Subject(name="Math", groups=False, classroom_type="normal"), teacher=Teacher(name="John Doe", subjects=[Subject(name="Math", groups=False, classroom_type="normal")]), class_=Class(name="1TI1", students=30, subjects=[Subject(name="Math", groups=False, classroom_type="normal")], teachers=[Teacher(name="John Doe", subjects=[Subject(name="Math", groups=False, classroom_type="normal")])], hour_flags=[Flags(early=True)], classroom="1"))
    print(data)
    data = json.dumps(dataclasses.asdict(data), indent=4)
    with open('data/examples/Lesson.json', 'w') as f:
        f.write(data)
LessonExample()

def TimetableExample():
    data = Timetable(class_=Class(name="1TI1", students=30, subjects=[Subject(name="Math", groups=False, classroom_type="normal")], teachers=[Teacher(name="John Doe", subjects=[Subject(name="Math", groups=False, classroom_type="normal")])], hour_flags=[Flags(early=True)], classroom="1"), monday=[Lesson(hour=LessonHour("8:00", "8:45", [Flags(early=True)]), classroom=Classroom(name="1", type="normal", max_students=30), subject=Subject(name="Math", groups=False, classroom_type="normal"), teacher=Teacher(name="John Doe", subjects=[Subject(name="Math", groups=False, classroom_type="normal")]), class_=Class(name="1TI1", students=30, subjects=[Subject(name="Math", groups=False, classroom_type="normal")], teachers=[Teacher(name="John Doe", subjects=[Subject(name="Math", groups=False, classroom_type="normal")])], hour_flags=[Flags(early=True)], classroom="1"))], tuesday=[], wednesday=[], thursday=[], friday=[])
    print(data)
    data = json.dumps(dataclasses.asdict(data), indent=4)
    with open('data/examples/Timetable.json', 'w') as f:
        f.write(data)
TimetableExample()