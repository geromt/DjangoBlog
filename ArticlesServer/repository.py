import uuid
from datetime import datetime
import dataclasses


@dataclasses.dataclass
class ArticleDTO:
    id: uuid.UUID
    title: str
    content: str
    created_at: datetime
