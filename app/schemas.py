from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    completed: bool = False

class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class Task(TaskBase):
    id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str
    password: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    email: str

    class Config:
        from_attributes = True