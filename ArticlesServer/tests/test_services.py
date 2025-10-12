import inspect
import pytest


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

def test_article_service_get_article_returns_error():
    """Verifica que `get_article` devuelva None o lance una excepción cuando se le pasa un ID no existente.

    - Si `get_article` no maneja IDs no existentes adecuadamente, el test falla.
    """
    from ArticlesServer import services

    articles_service = services.ArticleService

    non_existent_id = '00000000-0000-0000-0000-000000000000'  # UUID que no debería existir
    result = articles_service.get_article(non_existent_id)
    assert result.err() is not None, "get_article debería devolver un error para un ID no existente"
