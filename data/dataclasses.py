from dataclasses import dataclass
from typing import List, Union

# LessonHour, Classroom, Subject, Teacher, Class, Lesson, Timetable

@dataclass
class Flags:
    early: bool = False
    late: bool = False

@dataclass
class LessonHour:
    start: str
    end: str
    hour_flags: List[Flags]

@dataclass
class Classroom:
    name: str
    type: str
    max_students: int

@dataclass
class Subject:
    name: str
    groups: bool
    classroom_type: str

@dataclass
class Teacher:
    name: str
    subjects: List[Subject]

@dataclass
class Class:
    name: str
    students: int
    subjects: List[Subject]
    teachers: List[Union[Subject, str]]
    hour_flags: List[Flags]
    classroom: str

@dataclass
class Lesson:
    hour: LessonHour
    classroom: Classroom
    subject: Subject
    teacher: Teacher
    class_: Class

@dataclass
class Timetable:
    class_: Class
    monday: List[Lesson]
    tuesday: List[Lesson]
    wednesday: List[Lesson]
    thursday: List[Lesson]
    friday: List[Lesson]