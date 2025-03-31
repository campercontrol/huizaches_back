
from fastapi import Query

from schema.pagination.pagination_schema import SortEnum, Pagination,PaginationOut

def pagination_params(
    page: int = Query(ge=1, required=False, default=1, le=500000),
    per_page: int = Query(ge=1, required=False, default=10, le=100),
    order: SortEnum = SortEnum.DESC
):
    offset = page - 1 if page == 1 else (page - 1) * per_page    
    return PaginationOut(perPage=per_page, page=page, order=order.value, offset=offset)

def get_number_of_pages(pages_count: int, per_page: int) -> int:
    rest = pages_count % per_page
    quotient = pages_count // per_page
    return quotient if not rest else quotient + 1