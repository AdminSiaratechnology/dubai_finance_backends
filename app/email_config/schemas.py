# schemas/email_config.py

from pydantic import BaseModel

class EmailConfigBase(BaseModel):
    smtp_user: str
    smtp_password: str


class EmailConfigCreate(EmailConfigBase):
    pass


class EmailConfigOut(EmailConfigBase):
    id: int

    class Config:
        from_attributes = True