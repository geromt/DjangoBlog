import uuid

from result import Result, Err, Ok

from ArticlesServer.dtos import ArticleDTO
from ArticlesServer.repository import ArticleRepository


class ArticleService:
    def __init__(self):
        self.repository = ArticleRepository()

    def get_article(self, article_id: uuid.UUID) -> Result[ArticleDTO, str]:
        if not isinstance(article_id, uuid.UUID):
            return Err("Invalid UUID: article_id must be a UUID")
        if not self.repository.get_by_id(article_id):
            return Err("Invalid UUID: article_id does not exist")

        article: ArticleDTO = self.repository.get_by_id(article_id).to_dto(ArticleDTO)
        return Ok(article)

    def get_articles(self) -> Result[list[ArticleDTO], str]:
        articles = self.repository.get()
        dtos = [article.to_dto(ArticleDTO) for article in articles]
        return Ok(dtos)
