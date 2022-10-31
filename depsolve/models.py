from pydantic import BaseModel, validator


class Dependency(BaseModel):
    name: str
    depends_on: set[str] = {}

    def __hash__(self):
        return self.name.__hash__()

    @validator('depends_on', pre=True)
    def convert_depends_to_set(cls, depends_on_raw):
        if isinstance(depends_on_raw, list):
            return set(depends_on_raw)
        return depends_on_raw
