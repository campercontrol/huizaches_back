from pydantic import BaseModel, Field
from enum import Enum

class SortEnum(Enum):
    ASC = 'asc'
    DESC = 'desc'
    
class Pagination(BaseModel):
    perPage: int
    page: int
    order: SortEnum
    
class PaginationOut(BaseModel):
    perPage: int
    page: int
    offset: int
    order: SortEnum

    