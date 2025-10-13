from ArticlesServer.models import Article


class ArticleRepository:
    def __init__(self):
        self.queryset = Article.objects.all()

    def get_by_id(self, id):
        return self.queryset.filter(id=id).first()

    def get(self):
        return self.queryset.all()

    def create(self, **kwargs):
        article = Article.objects.create(**kwargs)
        return article

    def update(self, id, **kwargs):
        article = self.get_by_id(id)
        if article:
            for key, value in kwargs.items():
                setattr(article, key, value)
            article.save()
        return article

    def delete(self, id):
        article = self.get_by_id(id)
        if article:
            article.delete()
        return article

    def filter(self, **kwargs):
        return self.queryset.filter(**kwargs)

    def save(self, article):
        article.save()
        return article
