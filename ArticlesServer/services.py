import uuid

from result import Result, Err, Ok

from ArticlesServer.models import Article
from ArticlesServer.repository import ArticleDTO


class ArticleService:
    @staticmethod
    def get_article(article_id: uuid.UUID) -> Result[ArticleDTO, str]:
        if not isinstance(article_id, uuid.UUID):
            return Err("Invalid UUID: article_id must be a UUID")
        if not Article.objects.filter(id=article_id).exists():
            return Err("Invalid UUID: article_id does not exist")

        article: ArticleDTO = Article.objects.get(id=article_id).to_dto(ArticleDTO)
        return Ok(article)
