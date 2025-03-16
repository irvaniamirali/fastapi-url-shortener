from pydantic import BaseModel, constr


class Key(BaseModel):
    key: constr(min_length=6, max_length=6, pattern=r'^[a-zA-Z0-9]+$')
