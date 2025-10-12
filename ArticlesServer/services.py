import uuid

from result import Result, Err

from ArticlesServer.repository import ArticleDTO


class ArticleService:
    @staticmethod
    def get_article(article_id: uuid.UUID) -> Result[ArticleDTO, str]:
        return Err("Not implemented yet")
