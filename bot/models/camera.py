from pydantic import BaseModel


class Camera(BaseModel):
    id: int | None = None
    num: int
    name: str
    camera_url: str | None = None
