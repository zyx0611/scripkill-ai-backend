from bson.int64 import Int64
from pydantic import BaseModel
from typing import Optional, List


class GirlRequest(BaseModel):
    is_show: Optional[bool] = None
    is_open: Optional[bool] = None


class GoodsResponse(BaseModel):
    name: str
    uuid: str
    pic: str
    is_show: bool
    is_open: bool
    open_if: str
    open_number: int

class GirlResponse(BaseModel):
    uuid: str
    name: str
    age: int
    height: int
    job: str
    level: int
    pic: str
    is_show: bool
    is_open: bool
    open_if: str
    open_number: int
    upgrade_value: int
    current_upgrade_value: int
    clothes: List[GoodsResponse]
    jewelrys: List[GoodsResponse]
    others: List[GoodsResponse]
    dances: List[GoodsResponse]