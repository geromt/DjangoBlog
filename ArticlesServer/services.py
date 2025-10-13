import uuid

from result import Result, Err

from ArticlesServer.repository import ArticleDTO


class ArticleService:
    @staticmethod
    def get_article(article_id: uuid.UUID) -> Result[ArticleDTO, str]:
        if not isinstance(article_id, uuid.UUID):
            return Err("Invalid UUID: article_id must be a UUID")
        return Err("Not implemented yet")
