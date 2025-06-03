from typing import Optional, List

from pydantic import BaseModel, Field


class TableBase(BaseModel):
    capacity: int = Field(..., gt=0)
    table_number: str
    is_active: bool = True


class TableCreate(TableBase):
    pass


class TableBulkCreate(BaseModel):  # Add this new class
    tables: List[TableCreate]


class TableUpdate(BaseModel):
    capacity: Optional[int] = Field(None, gt=0)
    table_number: Optional[str] = None
    is_active: Optional[bool] = None


class TableResponse(TableBase):
    table_id: int
    restaurant_id: int

    class Config:
        from_attributes = True
