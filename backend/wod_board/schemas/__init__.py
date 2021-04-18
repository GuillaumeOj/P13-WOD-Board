import pydantic
import sqlalchemy.orm


# From https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-679207580
class OrmBase(pydantic.BaseModel):
    # Pre-processing validator that evaluates lazy relationships before any
    # other validation
    @pydantic.validator("*", pre=True)
    def evaluate_lazy_columns(cls, v):
        if isinstance(v, sqlalchemy.orm.Query):
            return v.all()
        return v

    class Config:
        orm_mode = True
