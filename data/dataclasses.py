from dataclasses import dataclass
from typing import List, Union

# LessonHour, Classroom, Subject, Teacher, Class, Lesson, Timetable
@dataclass
class LessonHour:
    lp: int
    start: str
    end: str

@dataclass
class ClassroomType:
    name: str

@dataclass
class Classroom:
    name: str
    classroom_type: ClassroomType
    max_students: int


@dataclass
class Subject:
    name: str
    classroom_type: ClassroomType
    teacher_preference: int # 0 - any subject teacher, 1 - headteacher
    first_class_hr: int
    second_class_hr: int
    third_class_hr: int

@dataclass
class Teacher:
    short_name: str
    name: str
    subject: Subject
    headteacher: int # 0 - nope, 1 - can be / is
    hours: int

@dataclass
class ClassTeam:
    name: str
    students: int
    headteacher: Teacher
    classroom: Classroom

@dataclass
class AssignedTeacher:
    lp: int
    subject: Subject
    teacher: Teacher
    assigned_class: ClassTeam

@dataclass
class Lesson: # format lekcji w bazie danych - [przedmiot, nauczyciel, sala]
    assigned_class: ClassTeam
    hour: LessonHour
    classroom: Classroom
    subject: Subject
    teacher: Teacher

@dataclass
class Timetable:
    assigned_class: ClassTeam
    lesson_hour: LessonHour
    monday: List[Lesson]
    tuesday: List[Lesson]
    wednesday: List[Lesson]
    thursday: List[Lesson]
    friday: List[Lesson]

@dataclass
class DataPack:
    lesson_hours: List[LessonHour]
    classroom_types: List[ClassroomType]
    classrooms: List[Classroom]
    subjects: List[Subject]
    teachers: List[Teacher]
    classes: List[ClassTeam]
    assigned_teachers: List[AssignedTeacher]
    timetables: List[Timetable]