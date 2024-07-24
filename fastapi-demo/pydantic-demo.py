from pydantic import BaseModel

data = {
    "name": "John Doe",
    "age": 32,
    "is_student": False
    "marks": [90, 80, 70]
}

class Student(BaseModel):
    name: str
    age: int
    is_student: bool
    marks: list[int] = []

student = Student(**data)
print(f"Student: {student}")