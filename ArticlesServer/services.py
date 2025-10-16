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

    def create_article(self, title: str, content: str, author: str) -> Result[ArticleDTO, str]:
        if not title:
            return Err("Title cannot be empty")
        if not content:
            return Err("Content cannot be empty")
        if not author:
            return Err("Author cannot be empty")

        article = self.repository.create(title=title, content=content, author=author)
        dto = article.to_dto(ArticleDTO)
        return Ok(dto)

    def update_article(self, article_id: uuid.UUID, title: str = None, content: str = None, author: str = None) -> Result[ArticleDTO, str]:
        if not article_id:
            return Err("article_id is required")
        if not isinstance(article_id, uuid.UUID):
            return Err("Invalid UUID: article_id must be a UUID")
        if not self.repository.get_by_id(article_id):
            return Err("Invalid UUID: article_id does not exist")

        article = self.repository.update(article_id, title=title, content=content, author=author)
        dto = article.to_dto(ArticleDTO)
        return Ok(dto)
