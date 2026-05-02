from pydantic import BaseModel, Field


class StudentModel(BaseModel):
    student_id: str = Field(min_length=3, max_length=30)
    student_name: str = Field(min_length=2, max_length=80)
    attendance: float = Field(ge=0, le=100)
    cgpa: float = Field(ge=0, le=10)
    past_marks: float = Field(ge=0, le=100)
