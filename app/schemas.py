from pydantic import BaseModel, Field, ConfigDict


class TaskBase(BaseModel):
    title: str
    completed: bool = False


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    completed: bool | None = None


class Task(TaskBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)