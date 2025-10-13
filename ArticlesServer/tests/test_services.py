import inspect
import pytest
import uuid


def test_article_service_exists_and_is_class():
    """Verifica que exista `ArticleService` en `ArticlesServer.services` y que sea una clase.

    - Si no se puede importar el módulo, el test falla con el error de importación.
    - Si el nombre no existe en el módulo, el test falla indicando que falta.
    - Si existe pero no es una clase, el test falla indicando el tipo encontrado.
    """
    try:
        from ArticlesServer import services
    except Exception as e:
        pytest.fail(f"No se pudo importar ArticlesServer.services: {e}")

    if not hasattr(services, 'ArticleService'):
        pytest.fail("ArticleService no encontrado en ArticlesServer.services")

    ArticleService = getattr(services, 'ArticleService')
    assert inspect.isclass(ArticleService), (
        f"ArticleService existe pero no es una clase (tipo: {type(ArticleService).__name__})"
    )


def test_article_service_get_article():
    """Verifica que `ArticleService` tenga un método `get_article` que acepte un parámetro `article_id`.

    - Si `ArticleService` no existe, el test falla.
    - Si `get_article` no existe, el test falla.
    - Si existe pero no es un método, el test falla.
    - Si el método no acepta `article_id`, el test falla.
    """
    try:
        from ArticlesServer import services
        ArticleService = getattr(services, 'ArticleService')
    except Exception as e:
        pytest.fail(f"No se pudo importar ArticlesServer.services o ArticleService: {e}")

    if not hasattr(ArticleService, 'get_article'):
        pytest.fail("get_article no encontrado en ArticleService")

    get_article = getattr(ArticleService, 'get_article')
    if not inspect.isfunction(get_article) and not inspect.ismethod(get_article):
        pytest.fail(f"get_article existe pero no es un método (tipo: {type(get_article).__name__})")

    sig = inspect.signature(get_article)
    if 'article_id' not in sig.parameters:
        pytest.fail("get_article no acepta un parámetro 'article_id'")


@pytest.mark.django_db
def test_article_service_get_article_returns_error():
    """Verifica que `get_article` devuelva un error o lance una excepción cuando se le pasa un ID no existente.

    - Usamos un UUID válido pero que no debería existir en la BD.
    """
    from ArticlesServer import services

    service = services.ArticleService()

    non_existent_id = uuid.UUID('00000000-0000-0000-0000-000000000000')  # UUID que no debería existir
    result = service.get_article(non_existent_id)
    assert result.err() is not None, "get_article debería devolver un error para un ID no existente"


@pytest.mark.django_db
def test_get_article_invalid_uuid_returns_error():
    """Verifica que `get_article` produzca un error si el id no es un UUID válido.

    - El servicio actual devuelve Err con un mensaje indicando el problema.
    """
    from ArticlesServer import services

    service = services.ArticleService()
    invalid_id = 'not-a-uuid'  # Any para evitar advertencia de tipo estático

    result = service.get_article(invalid_id)
    assert result.err() is not None, "get_article debería devolver un error para un ID no válido"
    assert "Invalid UUID" in result.err(), (
        "El error devuelto debería indicar que el UUID es inválido"
    )


@pytest.mark.django_db
def test_get_article_returns_existing_article_ok():
    """Crea un Article y verifica que get_article lo devuelve correctamente como DTO en Ok.

    - Debe retornar Ok con un ArticleDTO.
    - Los campos id, title, content y created_at deben coincidir con el modelo creado.
    """
    from ArticlesServer.models import Article
    from ArticlesServer import services

    service = services.ArticleService()

    auto_title = "Test Article"
    auto_content = "Lorem ipsum dolor sit amet"
    auto_author = "Tester"

    obj = Article.objects.create(title=auto_title, content=auto_content, author=auto_author)

    result = service.get_article(obj.id)

    # Debe ser éxito (Ok)
    assert result.err() is None, f"No se esperaba error, pero se obtuvo: {result.err()}"
    dto = result.ok()
    assert dto is not None, "Se esperaba un DTO en Ok()"

    assert dto.id == obj.id
    assert dto.title == obj.title
    assert dto.content == obj.content
    assert dto.created_at == obj.created_at

@pytest.mark.django_db
def test_get_articles_returns_all():
    """Verifica que el servicio devuelva todos los artículos creados.

    - Crea varios artículos en la base de datos.
    - Llama al método del servicio para obtener todos los artículos.
    - Verifica que la cantidad y los datos coincidan.
    """
    from ArticlesServer.models import Article
    from ArticlesServer import services

    service = services.ArticleService()

    articles_data = [
        {"title": "Article 1", "content": "Content 1", "author": "Author 1"},
        {"title": "Article 2", "content": "Content 2", "author": "Author 2"},
        {"title": "Article 3", "content": "Content 3", "author": "Author 3"},
    ]

    created_articles = [Article.objects.create(**data) for data in articles_data]

    result = service.get_articles()

    assert result.err() is None, f"No se esperaba error, pero se obtuvo: {result.err()}"
    dtos = result.ok()
    assert dtos is not None, "Se esperaba una lista de DTOs en Ok()"
    assert len(dtos) == len(created_articles), (
        f"Se esperaban {len(created_articles)} artículos, pero se obtuvieron {len(dtos)}"
    )

    for dto, article in zip(dtos, created_articles):
        assert dto.id == article.id
        assert dto.title == article.title
        assert dto.content == article.content
