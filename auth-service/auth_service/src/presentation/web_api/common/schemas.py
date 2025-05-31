from pydantic import BaseModel


class PaginationData(BaseModel):
    after_id: int = 0
    page_size: int = 10
