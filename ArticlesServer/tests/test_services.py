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
