from  pydantic import BaseModel, Field, validator
from typing import Optional
import json
from datetime import date

class prompt(BaseModel):
    role: str
    message: str

class UserInput(BaseModel):
    role: str = Field(..., description="Agent 的角色")
    message: str = Field(..., description="使用者的訊息")
    zodiac_sign: Optional[str] = Field(None, description="使用者的星座")
    age: Optional[int] = Field(None, ge=0, description="使用者的年齡")
    query_date: Optional[date] = Field(None, description="查詢的日期")

    @validator('zodiac_sign')
    def validate_zodiac(cls, v):
        zodiac_signs = [
            "白羊座", "金牛座", "雙子座", "巨蟹座", "獅子座", "處女座",
            "天秤座", "天蠍座", "射手座", "摩羯座", "水瓶座", "雙魚座"
        ]
        if v and v not in zodiac_signs:
            raise ValueError('無效的星座')
        return v

class AgentResponse(BaseModel):
    role: str
    message: str
    suggestions: Optional[str] = None
    horoscope: Optional[str] = None
