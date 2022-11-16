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
    teacher_preference: int # 0 - any subject teacher, 1 - headteacher
    first_class_hr: int
    second_class_hr: int
    third_class_hr: int

@dataclass
class Teacher:
    name: str
    short_name: str
    subjects: str
    headteacher: int # 0 - nope, 1 - can be / is
    hours: int

@dataclass
class Class:
    name: str
    students: int
    headteacher: str
    # subjects: List[Subject]
    # teachers: List[Union[Subject, str]]
    # hour_flags: List[Flags]
    # classroom: str

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