from datetime import time
from enum import Enum
from typing import List

from pydantic import BaseModel, validator


class DayOfWeek(str, Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class OperatingHoursResponse(BaseModel):
    day_of_week: DayOfWeek
    opening_time: time
    closing_time: time


class OperatingHoursCreate(BaseModel):
    day_of_week: DayOfWeek
    opening_time: time
    closing_time: time

    @validator("closing_time")
    def closing_after_opening(cls, v, values):
        if "opening_time" in values and v <= values["opening_time"]:
            raise ValueError("closing_time must be after opening_time")
        return v


class OperatingHoursBulkCreate(BaseModel):
    operating_hours: List[OperatingHoursCreate]