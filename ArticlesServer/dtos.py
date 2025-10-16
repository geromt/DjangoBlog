import uuid
from datetime import datetime
import dataclasses


@dataclasses.dataclass
class ArticleDTO:
    id: uuid.UUID
    title: str
    content: str
    author: str
    created_at: datetime
